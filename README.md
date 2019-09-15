# Drugs-at-FDA-mab-scraper
This is a preliminary web scraper project using Scrapy and based on a Scrapy Tutorial from the Scrapy Documentation.
The purpose of the project is to scrape particular categories of data for monoclonal antibody drugs from the Drugs@FDA website

## Extracted data

This project extracts generic name, brand name, drug subclass, pH, concentration, and formulation details of monoclonal antibody drugs in Drugs@FDA website

## Spider

The spider used in this project uses the OpenFDA API to extract the above data

## Running the spider

You can run the spider using the `scrapy crawl` command, such as:

    $ scrapy crawl api

If you want to save the scraped data to a file, you can pass the `-o` option:

    $ scrapy crawl api -o data.json