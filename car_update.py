import time

from Auto24Scraper import Auto24Scraper
from utilities import excel_utils

if __name__ == "__main__":
    auto24 = Auto24Scraper()
    print("Initialized scraper, starting to scrape...")
    start_time = time.time()
    res = auto24.get_vehicles_from_pages(pages=1000, category=101)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Scrape successful, total time taken: {elapsed_time} seconds")

    # print("Starting to save to Excel...")
    # start_time = time.time()
    # excel_utils.save_vehicles_to_excel(vehicles=res, filename="all_cars_multithread.xlsx", images=False)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Initial file save completed, elapsed time: {elapsed_time} seconds")

    start_time = time.time()
    excel_utils.update_excel_with_new_data(vehicles=res, filename="all_cars_multithread.xlsx")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Excel updated with new data, elapsed time: {elapsed_time} seconds")

    print(f"Successful run. Scraped a total of {len(res)} vehicles out of {auto24.total_vehicles_count}.")
