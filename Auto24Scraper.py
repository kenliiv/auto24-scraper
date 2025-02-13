import re
import threading

from bs4 import BeautifulSoup, Tag
from selenium import webdriver

from models.Vehicle import Vehicle


class Auto24Scraper:
    """
    TODO
    """

    def __init__(self):
        self._category = 101  # cars, 109 is motorcycles
        self._total_vehicles_count = 0

    @property
    def total_vehicles_count(self):
        return self._total_vehicles_count

    def get_vehicles_from_pages(self, pages: int, category: int = 101) -> list[Vehicle]:
        """
        101 is cars, 109 is motorcycles
        """
        if pages < 1:
            raise ValueError("Pages to scrape must be at least 1")

        if category not in [101, 109]:
            raise ValueError("Invalid category. Must be 101 (cars) or 109 (motorcycles). "
                             "Can be left empty to default to cars.")

        self._category = category
        self.update_total_vehicles_count()

        result_list: list[Vehicle] = []
        pages_max = (self.total_vehicles_count // 100) + 1  # if too many pages given, limit to max scrapeable
        if pages > pages_max:
            pages = pages_max
        lock = threading.Lock()

        def worker(page_range, worker_num):
            nonlocal result_list
            local_driver = self.build_driver()
            for page_being_processed in page_range:
                print(f"W{str(worker_num)}: Scraping page {page_being_processed}")
                try:
                    html = self.scrape_selenium(page=page_being_processed, driver=local_driver)
                except OverflowError as e:
                    print("Reached overflow when scraping: " + repr(e))
                    break
                soup = BeautifulSoup(html, "html.parser")

                results_on_page = soup.find_all("div", class_=re.compile("result-row", re.IGNORECASE))
                local_results = []
                for result in results_on_page:
                    new_vehicle = self.resolve_fields(result)
                    local_results.append(new_vehicle)
                with lock:
                    result_list.extend(local_results)
            local_driver.quit()

        # Divide pages among threads
        num_threads = 4
        pages_per_thread = pages // num_threads
        threads = []
        for i in range(num_threads):
            start_page = i * pages_per_thread + 1
            end_page = (i + 1) * pages_per_thread if i != num_threads - 1 else pages
            thread = threading.Thread(target=worker, args=(range(start_page, end_page + 1), i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return result_list

    def scrape_selenium(self, page: int, driver: webdriver):
        if page == 0:
            raise ValueError("Page number cannot be 0")

        page = page - 1
        how_many_on_page = 100
        start_num = page * how_many_on_page
        if self.total_vehicles_count != 0 and start_num >= self.total_vehicles_count:
            raise OverflowError("Cannot scrape more pages than there are vehicles")

        url = self.build_base_url(how_many_on_page=how_many_on_page, start=start_num)
        driver.get(url)
        page_html = driver.page_source

        return page_html

    def resolve_fields(self, vehicle_html: Tag) -> Vehicle:
        if self._category == 101:
            vehicle_type = "car"
        elif self._category == 109:
            vehicle_type = "motorcycle"
        else:
            vehicle_type = "unknown"

        vehicle = Vehicle(vehicle_type)
        vehicle.id = vehicle_html.find("a", class_="main").get("href").split("/")[-1]
        vehicle.link = self.build_vehicle_link(vehicle.id)
        vehicle.is_auction = self.check_for_auction(vehicle_html)
        vehicle.make = vehicle_html.find("div", class_="title").findChild("span").text.replace("'", "").strip()
        vehicle.model = self.get_html_text_by_class(vehicle_html, "span", "model")
        vehicle.price = self.get_formatted_price(self.get_html_text_by_class(vehicle_html, "span", "price"))
        vehicle.year = self.get_html_text_by_class(vehicle_html, "span", "year")
        vehicle.mileage = self.get_html_text_by_class(vehicle_html, "span", "mileage")
        vehicle.fuel = self.get_html_text_by_class(vehicle_html, "span", "fuel")
        vehicle.transmission = self.get_html_text_by_class(vehicle_html, "span", "transmission")
        vehicle.bodytype = self.get_html_text_by_class(vehicle_html, "span", "bodytype")
        vehicle.drive = self.get_html_text_by_class(vehicle_html, "span", "drive")

        # scrape img from inline css
        scraped_style = vehicle_html.find("span", class_="thumb")["style"]
        if scraped_style is not None:
            vehicle.image_url = scraped_style.split("url('")[1].split("')")[0]

        return vehicle

    def get_html_text_by_class(self, html: Tag, element_name: str, class_name: str) -> str:
        found_element = html.find(element_name, class_=class_name)
        if found_element is None:
            return ""

        return found_element.text

    def get_formatted_price(self, price: str) -> int:
        if price is None or price == "":
            return 0

        return int(
            price.replace("€", "")
            .strip()
            .replace(" ", "")
            .replace(u'\xa0', u'')
        )

    @staticmethod
    def check_for_auction(vehicle_html: Tag) -> bool:
        has_auction_found = vehicle_html.find("img", src=re.compile("auction", re.IGNORECASE))
        if has_auction_found:
            return True
        return False

    @staticmethod
    def build_vehicle_link(vehicle_id: str) -> str:
        return f"https://www.auto24.ee/soidukid/{vehicle_id}"

    def update_total_vehicles_count(self):
        driver = self.build_driver()
        html = self.scrape_selenium(page=1, driver=driver)
        page_soup = BeautifulSoup(html, "html.parser")
        self._total_vehicles_count = int(page_soup.find("div", class_="paginator__rangeCurrent")
                                         .findChild("strong").text)
        driver.quit()
        print("Total vehicles count updated to: " + str(self._total_vehicles_count))

    def build_base_url(self, how_many_on_page: int = 100, start: int = 0) -> str:
        return f"https://www.auto24.ee/kasutatud/nimekiri.php?bn=2&a={self._category}&ae=2&af={how_many_on_page}&ag=1&otsi=otsi&ak={start}"

    def build_driver(self):
        # Headless would be nice, but the site will start blocking. Can do with Options() and add_argument("--headless")
        driver = webdriver.Firefox()  # can also do Chrome, but was slower
        return driver
