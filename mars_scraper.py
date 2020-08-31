from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
  executable_path = {'executable_path': 'chromedriver.exe'}
  return Browser('chrome', **executable_path)


def scrape():
  
  browser = init_browser()

  # Visit Mars News site 
  browser.visit('https://mars.nasa.gov/news/')

  html_news = browser.html

  soup = BeautifulSoup(html_news, 'html.parser')

  title_results = soup.find_all('div', class_='content_title')
  news_title = title_results[1].text

  para_results = soup.find_all('div', class_='article_teaser_body')

  time.sleep(2)

  news_para = para_results[0].text

  # Visit JPL site for featured Mars image
  browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

  html_featured = browser.html

  soup_featured = BeautifulSoup(html_featured, 'html.parser')

  img_results = soup_featured.find_all('div',class_='img')
  img_url = img_results[0].img['src']

  featured_image_url = 'https://www.jpl.nasa.gov' + img_url


  # Scrape Mars Space Facts
  url = 'https://space-facts.com/mars/'

  tables = pd.read_html(url)
  tables

  mars_table_df = tables [0]

  mars_table_df.columns = ['Description','Mars']

  mars_table_df.set_index('Description', inplace=True)

  html_table = mars_table_df.to_html()

  # Visit USGS Astrogeology Site
  browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

  html_hemisphere = browser.html
  soup_hemisphere = BeautifulSoup(html_hemisphere, 'html.parser')

  mars_hemisphere = soup_hemisphere.find_all('div', class_='item')

  hemisphere_image_urls = []

  hemispheres_main_url = 'https://astrogeology.usgs.gov'

  for mars in mars_hemisphere:
    
    title = mars.find('h3').text
    
    hemisphere_url = mars.find('a', class_='itemLink product-item')['href']
    
    browser.visit(hemispheres_main_url + hemisphere_url)
    
    # HTML Object
    html_hemisphere = browser.html

    # Parse HTML with Beautiful Soup
    html_featured = BeautifulSoup(html_hemisphere, 'html.parser')
    
    img_url = hemispheres_main_url + html_featured.find('img', class_='wide-image')['src']
    
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
  # Store data in a dictionary
  mars_data = {
      "news_title": news_title,
      "news_paragraph": news_para,
      "featured_image": featured_image_url,
      "mars_facts": html_table,
      "hemispheres": hemisphere_image_urls
  }
  # Close the browser after scraping
  browser.quit()

  # Return results
  return mars_data