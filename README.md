# 🚗 auto24Scraper

A selenium-based web scraper for Auto24.ee, a popular Estonian vehicle sales website.

Mainly uploading this to let others find weird-acting sellers who scheme with car prices.
And because the auto24 developers seem to be hell-bent on making the website bot-unfriendly while also not providing an API for public use, shame shame shame.
Now I will waste your precious bandwidth with my bot that downloads images too, but you could just give it to me in JSON format.

## ✨ Features

- Scrape vehicle listings from Auto24.ee (support for any category, but does cars and motorcycles out of the box)
- Save the listings to an Excel file
- Update the Excel file with new listings, keeping track of price changes and appending new listings
- WIP: save thumbnail image of listings to the Excel file (works, but not very useful)


## 📋 How to use

Main logic is in `Auto24Scraper.py`, with examples of using it being shown in `car_update.py` and `motorcycle_update.py`.

This scraper uses the Selenium browser automation library to scrape the Auto24 website for vehicle listings.

Excel table row structure is defined in `Vehicle.py` under the `to_dict` method.

Excel file manipulation is done in `utilities/excel_utils.py`. Also image saving, but let's not talk about that, not very clean code.

Dependencies are outlined in `requirements.txt`. But what you really need is (hopefully exhaustive list):
`pip install selenium openpyxl beautifulsoup4 pandas pillow`. 

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

## 🐞 Known bugs

- The scraper is not very robust and will likely break if the Auto24 website changes its layout (not much to do here, just update the scraper)
- Auction vehicles will just update the current auction price at the time of data retrieval
- Exception handling is not very robust, so if the scraper breaks, it will likely just crash (more of a TODO for you)

## 📜 License
< Super funny gag about driving licenses >

But in reality, just a hobby project.
Practicing selenium, excel file manipulation, workflows that incorporate AI and multithreading in Python.
Use it however you like. Just don't use it for evil, please.

