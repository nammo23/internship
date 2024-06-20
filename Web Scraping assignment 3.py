#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1
import requests
from bs4 import BeautifulSoup

def get_products(search_query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    url = f'https://www.amazon.in/s?k={search_query.replace(" ", "+")}'

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
        title = item.h2.text.strip() if item.h2 else 'No title'
        link = f"https://www.amazon.in{item.h2.a['href']}" if item.h2 and item.h2.a else 'No link'
        price = item.find('span', 'a-price-whole')
        price = price.text if price else 'No price'

        products.append({
            'title': title,
            'link': link,
            'price': price
        })

    return products

if __name__ == "__main__":
    search_query = input("Enter the product to search: ")
    products = get_products(search_query)

    if products:
        for idx, product in enumerate(products, 1):
            print(f"{idx}. {product['title']}\n   Price: {product['price']}\n   Link: {product['link']}\n")
    else:
        print("No products found.")


# In[2]:


#2
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_products(search_query, pages=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    products = []

    for page in range(1, pages + 1):
        url = f'https://www.amazon.in/s?k={search_query.replace(" ", "+")}&page={page}'

        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve search results for page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
            title = item.h2.text.strip() if item.h2 else '-'
            link = f"https://www.amazon.in{item.h2.a['href']}" if item.h2 and item.h2.a else '-'
            price = item.find('span', 'a-price-whole')
            price = price.text if price else '-'
            brand = item.find('span', 'a-size-base-plus')
            brand = brand.text.strip() if brand else '-'
            return_exchange = '-'
            expected_delivery = '-'
            availability = '-'
            
            if link != '-':
                product_response = requests.get(link, headers=headers)
                product_soup = BeautifulSoup(product_response.content, 'html.parser')

                return_exchange_tag = product_soup.find('a', {'id': 'RETURNS_POLICY'})
                return_exchange = return_exchange_tag.text.strip() if return_exchange_tag else '-'

                expected_delivery_tag = product_soup.find('div', {'id': 'ddmDeliveryMessage'})
                expected_delivery = expected_delivery_tag.text.strip() if expected_delivery_tag else '-'

                availability_tag = product_soup.find('div', {'id': 'availability'})
                availability = availability_tag.text.strip() if availability_tag else '-'

            products.append({
                'Brand Name': brand,
                'Name of the Product': title,
                'Price': price,
                'Return/Exchange': return_exchange,
                'Expected Delivery': expected_delivery,
                'Availability': availability,
                'Product URL': link
            })
            
        time.sleep(2)

    return products

if __name__ == "__main__":
    search_query = input("Enter the product to search: ")
    products = get_products(search_query)

    if products:
        df = pd.DataFrame(products)
        df.to_csv(f"{search_query}_amazon_products.csv", index=False)
        print(f"Data has been saved to {search_query}_amazon_products.csv")
    else:
        print("No products found.")


# In[ ]:


#3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def search_images(driver, query):
    driver.get('https://images.google.com/')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  
    return driver.page_source

def scrape_urls(html, num_images):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img', {'class': 'rg_i'}, limit=num_images)
    urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    return urls

def save_images(urls, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    for i, url in enumerate(urls):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, f'image_{i + 1}.jpg'), 'wb') as file:
                file.write(response.content)

def main():
    driver = setup_driver()
    keywords = ['fruits', 'cars', 'Machine Learning', 'Guitar', 'Cakes']
    num_images = 10
    
    for keyword in keywords:
        html = search_images(driver, keyword)
        image_urls = scrape_urls(html, num_images)
        save_images(image_urls, keyword)
    
    driver.quit()

if __name__ == "__main__":
    main()


# In[ ]:


#4
pip install selenium beautifulsoup4 pandas requests webdriver-manager
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def search_flipkart(driver, query):
    driver.get('https://www.flipkart.com/')
    time.sleep(2)
    close_login_popup(driver)
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  
    return driver.page_source

def close_login_popup(driver):
    try:
        close_button = driver.find_element(By.XPATH, '//button[contains(text(),"✕")]')
        close_button.click()
    except:
        pass

def scrape_phone_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    for item in soup.find_all('div', {'class': '_1AtVbE'}):
        title_tag = item.find('a', {'class': 'IRpwTa'})
        if not title_tag:
            continue

        title = title_tag.text
        link = f"https://www.flipkart.com{title_tag['href']}"
        details = item.find('div', {'class': '_3k-BhJ'})
        price = item.find('div', {'class': '_30jeq3 _1_WHN1'})
        price = price.text if price else '-'
        
        details_text = details.text if details else ''
        brand_name = title.split()[0]
        
        product_details = {
            'Brand Name': brand_name,
            'Phone name': title,
            'Colour': extract_detail(details_text, 'Color'),
            'RAM': extract_detail(details_text, 'RAM'),
            'Storage(ROM)': extract_detail(details_text, 'Storage'),
            'Primary Camera': extract_detail(details_text, 'Primary Camera'),
            'Secondary Camera': extract_detail(details_text, 'Secondary Camera'),
            'Display Size': extract_detail(details_text, 'Display Size'),
            'Battery Capacity': extract_detail(details_text, 'Battery Capacity'),
            'Price': price,
            'Product URL': link
        }
        products.append(product_details)

    return products

def extract_detail(details_text, keyword):
    detail_parts = details_text.split('|')
    for part in detail_parts:
        if keyword in part:
            return part.split(':')[1].strip()
    return '-'

def main():
    driver = setup_driver()
    search_query = input("Enter the phone to search: ")
    html = search_flipkart(driver, search_query)
    driver.quit()
    
    products = scrape_phone_details(html)
    
    df = pd.DataFrame(products)
    df.to_csv(f"{search_query}_flipkart_phones.csv", index=False)
    print(f"Data has been saved to {search_query}_flipkart_phones.csv")

if __name__ == "__main__":
    main()


# In[ ]:


#5
pip install selenium webdriver-manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_coordinates(city):
    driver = setup_driver()
    driver.get('https://maps.google.com')
    time.sleep(2)

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(city)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  

    url = driver.current_url
    driver.quit()
    
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match:
        latitude, longitude = match.groups()
        return float(latitude), float(longitude)
    else:
        return None, None

if __name__ == "__main__":
    city = input("Enter the place to search: ")
    latitude, longitude = get_coordinates(city)
    if latitude and longitude:
        print(f"Coordinates of {city}: Latitude = {latitude}, Longitude = {longitude}")
    else:
        print("Could not find coordinates for the specified city.")


# In[ ]:


#6
pip install requests beautifulsoup4 pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_gaming_laptops():
    url = 'https://www.digit.in/top-products/best-gaming-laptops-40.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    laptops = []

    laptop_listings = soup.find_all('div', class_='TopNumbeHeading')
    
    for listing in laptop_listings:
        details = listing.find_next('div', class_='Section-center').text.strip().split('\n')
        laptop_details = {
            'Name': listing.h2.text.strip() if listing.h2 else '-',
            'Specs': ' '.join(details).replace('Read More', '').strip(),
        }
        laptops.append(laptop_details)
    
    return laptops

def main():
    laptops = get_gaming_laptops()
    
    if laptops:
        df = pd.DataFrame(laptops)
        df.to_csv("gaming_laptops.csv", index=False)
        print("Data has been saved to gaming_laptops.csv")
    else:
        print("No data found.")

if __name__ == "__main__":
    main()


# In[ ]:


#8
pip install google-api-python-client
from googleapiclient.discovery import build
import pandas as pd

API_KEY = 'YOUR_API_KEY'
VIDEO_ID = 'YOUR_VIDEO_ID'

def get_comments(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        textFormat='plainText'
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'Comment': comment['textDisplay'],
                'Upvotes': comment['likeCount'],
                'Time Posted': comment['publishedAt']
            })

        if 'nextPage' in response:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=response['nextPage'],
                maxResults=100,
                textFormat='plainText'
            )
        else:
            request = None

        if len(comments) >= 500:
            break

    return comments[:500]

def main():
    comments = get_comments(API_KEY, VIDEO_ID)
    
    if comments:
        df = pd.DataFrame(comments)
        df.to_csv("youtube_comments.csv", index=False)
        print("Data has been saved to youtube_comments.csv")
    else:
        print("No comments found.")

if __name__ == "__main__":
    main()

