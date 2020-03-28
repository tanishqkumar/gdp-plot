import requests
import csv
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib import patches as mpatches
import pandas as pd
import numpy as np

def scrape():
    # search the first wiki table to get the gdp of the below countries in the range 1980-89 and write them to a csv file
    country_list = ['Luxembourg', 'Switzerland', 'Norway', 'Ireland', 'Qatar', 'Iceland', 'United States', 'Singapore', 'Denmark', 'Australia']
    # get the HTML response back from a web request
    website_url = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projected_GDP_(nominal)_per_capita').text
    # use bs4 to parse the response into readable HTML
    site_html = BeautifulSoup(website_url, 'html.parser')
    # 2 is for the 80-89 table
    table1 = site_html.select('table')[2]
    table2 = site_html.select('table')[5]
    table3 = site_html.select('table')[8]
    table4 = site_html.select('table')[11]
    tables = [table1, table2, table3, table4]
    l1 = table1.find_all('a')
    countries = [link.get('title') for link in l1]
    # this list holds the positions of the countries in country_list within the actual table
    positions = []
    for i in range(10):
        for j in range(193):
            if country_list[i] == countries[j]: positions.append(j)

    # current structural error is that you can't read each table and then write row, you have to collect info about
    # a country across all 4 tables, store it somehow, and then write to the CSV file just once
    with open("/Users/tanishqkumar/desktop/exp.csv", mode='w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        nums = []
        countryInfo = []
        # create year columns for countries to slot into
        for i in range(1980, 2020):
            nums.append(i)
        writer.writerow(['Country Name'] + nums)
        # for each position of a member of country_list in the wiki table
        for i in positions:
            # gives 0->3
            for j in range(4):
                # go through each table and create a cells variable then append its data for that table to countryInfo
                # go to that row in the table to extract the data about that country we want, with +1 for adjustment
                rows = tables[j].find_all('tr')[i+1]
                # store the data from that row in that table in cells variable
                cells = rows.find_all('td')
                title = cells[0].find('a').get('title')
                # create a list with the title of the country, and the VALUES (by stripping our cells) of gdp associated with that from that table
                if j == 0:
                    countryInfo = [title] + [int(cell.text.strip().replace(',', '')) for cell in cells[1:]]
                else:
                    countryInfo = countryInfo + [int(cell.text.strip().replace(',', '')) for cell in cells[1:]]
            writer.writerow(countryInfo)

def plot():
    # plotting the data with pandas, built atop numpy
    df = pd.read_csv('/Users/tanishqkumar/desktop/exp.csv', index_col='Country Name').astype(float).T
    ax = df.plot(legend=True, title="Highest national GDP per-capita incomes over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per capita ($)")
    plt.show()

scrape()
plot()
