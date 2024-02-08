
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

paused = False
categories = []
names = []
companies = []
ratings = []
downloads = []
reviews = []
price = []
updatedDates = []

def ScrapeApp(appPageUrl, updatedDates, reviews, price, downloads, categories):
    driver.get(appPageUrl)
    appContent = driver.page_source
    appSoup = BeautifulSoup(appContent, features="html.parser")
    date = appSoup.find('p', attrs={"class": "date"})
    if date != None:
        updatedDates.append(date.text.strip())
    else:
        updatedDates.append("Not available")

    reviewsCount = soup.find('a', attrs={'class': 'details_score icon'})
    if reviewsCount:
        reviews.append(reviewsCount.text.strip())
    else:
        reviews.append("0")

    appPrice = soup.find('span', attrs={'class': 'price'})
    if appPrice:
        price.append(appPrice.text.strip())
    else:
        price.append("0")

    downloadCount = soup.find('span', attrs={'class': 'share-counter'})

    if downloadCount:
        downloads.append(downloadCount.text.strip())
    else:
        downloads.append("0")

    info = appSoup.findAll('p', attrs={'class': 'additional-info'})

    if info:
        category = info[4].text.strip()
        if category != None:
            categories.append(category)
        else:
            categories.append("Not Available")

    else:
        reviews.append("0")
        downloads.append("0")
        price.append("Free")
        categories.append("Not Available")
def ScrapeNextPage(url,names, companies, ratings, updatedDates, reviews, downloads, price, categories):
    driver.get(url)
    nextContent = driver.page_source
    nextSoup = BeautifulSoup(nextContent, features="html.parser")
    #Get all data on the page of one category
    while True:

        for a in nextSoup.findAll('div', attrs={'class': "grid-row"}):
            company = a.find('p', attrs={'class': 'grid-item-developer'})

            if company:
                companies.append(company.text.strip())
            else:
                companies.append("Not Available")

            rating = a.find('p', attrs={'class': 'grid-item-score'})
            if rating and len(rating)>0:
                ratings.append(rating.text.strip())
            else:
                ratings.append("0")

            name = a.find('a', attrs={'class': 'grid-item-title'})
            if name:

                nextHref = name.get('href')
                appPageUrl = 'https://m.apkpure.com'+nextHref
                ScrapeApp(appPageUrl, updatedDates, reviews, price, downloads, categories)
                names.append(name.text.strip())
            else:
                names.append("Not Available")
                reviews.append("0")
                updatedDates.append("Not Available")
                price.append("Free")
                downloads.append("0")
                categories.append("Not Available")
            SaveDataInFile()

        next_page = nextSoup.find('a', attrs={'class': 'show-more'})
        #If there is next page then move to next page otherwise break the while loop
        if next_page:
            nextPageHref = next_page.get('href')
            driver.get('https://m.apkpure.com'+nextPageHref)
            nextContent = driver.page_source
            nextSoup = BeautifulSoup(nextContent, features="html.parser")
        else:
            break


# Initialize the web driver and start the scraping
def start_scraping():
    try:
        global paused
        global soup
        global driver

        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://m.apkpure.com/app"
        driver.get(url)
        
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        # Find the div element with class 'apk-name-list' within the current page
        div = soup.find('div', class_='apk-name-list')
    
        
        
        count = 0

        
        for a in div.findAll('a')[22:23]:
            if paused:
                while paused:
                    time.sleep(1)
                    print("Web scraping paused. Waiting for resume...")

            href = a.get('href')
            nextUrl = "https://m.apkpure.com" + href
            ScrapeNextPage(nextUrl, names, companies, ratings, updatedDates, reviews, downloads, price, categories)
            
            if count == 23:
                break
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

def SaveDataInFile():
    
    # Create a DataFrame with the corrected column names
    df = pd.DataFrame({'Name': names, 'Company': companies, 'Rating': ratings, 'Reviews': reviews,
                    'Downloads': downloads, 'Price': price, 'Updated Date': updatedDates, 'Category': categories})
    # Replace empty strings in the column of rating if there is no rating available
    df['Rating'] = df['Rating'].replace('', '0')
    df.to_csv('ScrapedData.csv', index=False, encoding='utf-8')

def pause_scraping():
    global paused
    paused = True
    


def resume_scraping():
    global paused
    paused = False
    

def stop_scraping():
    global driver
    try:
        driver.quit()
    except Exception as e:
        print(str(e))