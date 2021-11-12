from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
def starbrowser():
    executable_path = {'executable_path': 'C:/Users/dylan/Downloads/chromedriver_win32/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)






def scrape():
    # NASA Mars News
    browser = starbrowser()
    mars_dict = {}
    response = requests.get('https://mars.nasa.gov/news/')
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_name = soup.find('div', class_='content_title').find('a').text
    articles_teaser = soup.find('div', class_='rollover_description_inner').text
    mars_dict.update({'article_name' : articles_name})
    mars_dict.update({'article_teaser': articles_teaser})
    
    # JPL Mars Space Images - Featured Image
    browser = starbrowser()
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    site_url = 'https://www.jpl.nasa.gov'
    img = soup.select_one("figure.lede a img").get('src')
    featured_image_url = site_url + img
    mars_dict.update({'JPL_link': featured_image_url})

    # Mars Hemispheres
    browser = starbrowser()
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    pic_names = []
    for x in soup.find_all('h3'):
        pic_names.append(x.text)
    img_url = 'https://astrogeology.usgs.gov'
    img_info = []
    for x in pic_names:
        browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
        browser.click_link_by_partial_text(x)
        browser.click_link_by_partial_text('Open')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_info.append({'title': x , 'img_url': img_url+soup.select_one("div.wide-image-wrapper img.wide-image").get('src')})
        mars_dict.update({'img_info': img_info})

    tables = pd.read_html('https://space-facts.com/mars/')
    df = tables[0]
    df.columns = ['', 'Data']
    df = df.set_index('')
    table_html = df.to_html()
    mars_dict.update({'table_html': table_html})
    
    return mars_dict





    