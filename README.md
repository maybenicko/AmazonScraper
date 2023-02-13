# AmazonScraper

This Python script scrapes product pages on Amazon and checks for price decreases. If the price decreases below a given price filter, a webhook is sent to a specified Discord channel.

# Requirements

The following Python packages are required to run the script:

- requests
- csv
- time
- termcolor
- datetime
- dhooks
- bs4
- lxml
- threading

# Usage

- Create a CSV file named 'scrape.csv' with the following format: url, price, delay
- Run the 'start' function to start the scraper.

# Disclaimer 

This script is intended for educational purposes only. Please use responsibly and do not use it to spam Amazon or violate Amazon's terms of service.
