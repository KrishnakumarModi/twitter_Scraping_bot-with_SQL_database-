from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

# Environment variable
my_Pass=str(os.getenv("my_Pass"))        
twitter_User_key=str(os.getenv("twitter_User_key"))
twitter_Password_key=str(os.getenv("twitter_Password_key"))


# Establish a connection to the MySQL database
try:
    conn = mysql.connector.connect(
    host='localhost',       
    user='root',        
    password=my_Pass,
    database='twitter_Database'
)
    if conn.is_connected():
        print("Successfully connected to MySQL database")
except Exception as e:
    print("Not connected")

# Setup the browser
service = Service(executable_path="chromedriver.exe")
browser = webdriver.Chrome(service=service)


# Function to log into Twitter
def login_To_twitter(username, password):
    browser.get("https://twitter.com/login")
    time.sleep(2)
    
    # Find and fill the login form
    username_Input = browser.find_element(By.XPATH, '//input[@name="text"]')
    username_Input.send_keys(username)
    username_Input.send_keys(Keys.RETURN)
    time.sleep(2)
    
    password_Input =browser.find_element(By.XPATH, '//input[@name="password"]')
    password_Input.send_keys(password)
    password_Input.send_keys(Keys.RETURN)
    time.sleep(2)

# Function to scrape user profile
def scrape_User_profile(user_handle):
    browser.get(f"https://twitter.com/{user_handle}")
    time.sleep(2)
    
    # Scrape user data
    try:
        bio =browser.find_element(By.XPATH, '//div[@data-testid="UserDescription"]').text.strip()       
    except Exception as e:
        bio = 'Not available'

    try:
        followers_Count =browser.find_element(By.XPATH, '//a[@href="/' + user_handle + '/verified_followers"]//span').text.strip()          
    except Exception as e:
        followers_count = 'Not available'
    
    try:
        following_Count =browser.find_element(By.XPATH, '//a[@href="/' + user_handle + '/following"]//span').text.strip()            
    except Exception as e:
        following_count = 'Not available'
    
    try:
        location =browser.find_element(By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]//span[@style="text-overflow: unset;"]//span[@style="text-overflow: unset;"]').text.strip()     
    except Exception as e:
        location = 'Not available'

    try:
        website =browser.find_element(By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]//a[contains(@href, "http")]').get_attribute('href')
    except Exception as e:
        website = 'Not available'
    
    # List to store the twitter data
    data = []
    # Append the scraped data
    data.append({
        "Bio": bio ,
        "Followers": followers_Count,
        "Following": following_Count,
        "Location": location,
        "Website": website
        })

    # Convert the data list into a pandas DataFrame
    df = pd.DataFrame(data)

    # Print the collected data
    print(df)

    
    # Prepare the cursor object
    cursor = conn.cursor()

    # create a table 
    try:
        cursor.execute(
            "CREATE TABLE twitter_data (Bio VARCHAR(300),"
            "Followers VARCHAR(300),"
            "Following VARCHAR(300),"
            "Location VARCHAR(300),"
            "Website VARCHAR(300))"
        )
    except Exception as e:
        print("Fail to create or already exist")

    # Convert DataFrame to list of tuples
    data_tuples = [tuple(x) for x in df.to_records(index=False)]

    # Prepare insert query
    insert_query = "INSERT INTO twitter_data (Bio, Followers, Following, Location, Website ) VALUES (%s, %s, %s, %s, %s)"

    # Insert data into the table
    cursor.executemany(insert_query, data_tuples)

    # Commit the transaction
    conn.commit()


    # Close cursor and connection
    cursor.close()
    conn.close()

  
# Main function
if __name__ == "__main__":
    # Login credentials
    twitter_Username = twitter_User_key
    twitter_Password = twitter_Password_key
    
    # Log in to Twitter
    login_To_twitter(twitter_Username, twitter_Password)
    
    # Scrape profile info for a user
    scrape_User_profile("GTNUK1")  

    # Close the browser
    browser.quit

