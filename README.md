# auto24Scraper

A selenium-based web scraper for Auto24.ee, a popular Estonian car sales website.
Used to get data about listings and save it to an Excel file, with support for initial file creation and appending to existing files.

Currently only supports retrieving data from the search result pages, not the individual car pages.


## How to use

Main logic and current entry point is in `main.py`.

This scraper uses the Selenium browser automation library to scrape the Auto24 website for vehicle listings.

Excel table row structure is defined in `Vehicle.py` under the `to_dict` method.

Once you get dependencies imported, you can use the scraper like this:

```python
from Auto24Scraper import Auto24Scraper
import utilities.excel_utils as excel_utils

# Initialize the scraper
auto24 = Auto24Scraper()

# Scrape 100 pages of search results (100*100 per page = 10000 cars) from the "Cars" category
res = auto24.get_vehicles_from_pages(pages=100, category=101)

# Save the results to an Excel file "vehicles.xlsx"
excel_utils.save_vehicles_to_excel(vehicles=res, filename="vehicles.xlsx", images=False)

# In case you want to track the price through time, you can scrape the page again at a new point in time and append results
# For this, use the update_excel_with_new_data method, which will add new row for vehicles that are new and add new column for updated vehicles
excel_utils.update_excel_with_new_data(vehicles=res, filename="vehicles.xlsx")
```

An Excel table will be created, where each row is a car and each column is a car attribute. 
The first row is the header row. The images are not saved by default, but can be saved by setting the `images` parameter to `True`.



## License
< Super funny gag about driving licenses >

But in reality, just a hobby project.
Practicing selenium, excel file manipulation, workflows that incorporate AI and multithreading in Python.
Use it however you like. Just don't use it for evil, please.

