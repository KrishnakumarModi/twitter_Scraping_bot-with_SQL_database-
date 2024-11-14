from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

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

    # Save the data to a CSV file
    df.to_csv('twitter_Data.csv', index=False)
    
# Main function
if __name__ == "__main__":
    # Login credentials
    twitter_Username = "testsubjec11196"
    twitter_Password = "Abcd@1234"
    
    # Log in to Twitter
    login_To_twitter(twitter_Username, twitter_Password)
    
    # Scrape profile info for a user
    scrape_User_profile("GTNUK1")  

    # Close the browser
    browser.quit()