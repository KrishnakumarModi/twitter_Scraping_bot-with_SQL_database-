# twitter_Scraping_bot(with_SQL_database)

## Overview

This project is a web scraping application built in Python that extracts data from twitter. The primary goal is to get data from website and export it into mySQL database which contain bio, followers, following, location and website.

## Features

- **Data Extraction**: Efficiently scrape data from twitter.
- **Data Storage**: Stores the extracted data in mySQL database.
- **Proxy Support**:proxy is not added.

## Requirements

- Python 3.12
- `selenium` library 
- `pandas` library
- `mySQL` database

## Working logic

The scraper uses Selenium to load the page, render any JavaScript, and extract the content dynamically. Here's a breakdown of the main steps in the scraper:

- **Launch Browser**: The script opens a Chrome browser window (or another browser) using Selenium’s WebDriver.
- **Navigate to Profile**: For each user in the input list, the bot navigates to their Twitter profile.
- **Extract Data**: It uses Selenium to extract the following details from the profile:
    - **Bio**: The description in the user’s bio section.
    - **Followers Count**: The number of followers listed on the profile.
    - **Following Count**: The number of people the user is following.
    - **Website URL**: If the user has provided a website URL in their profile.
    - **Location**: The location (if provided) in the profile.