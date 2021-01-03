from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Mars title and paragraph
    news_url = 'https://mars.nasa.gov/news/'

    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #news title and news_paragraph
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = soup.find('div', class_='article_teaser_body').text

    #print title & text
    #print(f'Title: {news_title}')
    #print(f'Paragraph: {news_p}')

    #--------------------------------------

    # Image Url
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(1)

    browser.click_link_by_partial_text("more info")
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #image info
    image = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + image

    #print
    #print(featured_image_url)

    #--------------------------------------

    # Mars Facts Table
    table_url = "https://space-facts.com/mars/"
    browser.visit(table_url)
    html = browser.html

    tables = pd.read_html(table_url)
    mars_info = tables[0]

    mars_info.columns = ['Index', 'Info']
    mars_info = mars_info.set_index('Index')

    # Mars HTML table
    mars_info = mars_info.to_html(classes="table table-striped")

    #--------------------------------------

    # Mars Hemisphere

    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_image_urls = []

    results = soup.find("div", class_="result-list")
    hemispheres = results.find("div", class_="item")

    for result in hemispheres:
    
        title = result.find('h3').text
        title = title.replace("Enhanced", "")
        end_link = result.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link 

        browser.visit(image_link)
        html = browser.html
        soup= BeautifulSoup(html, "html.parser")
        
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
    
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    #print hemisphere title and image_url
    #print(hemisphere_image_urls)

    #--------------------------------------

    # Mars Data Dictionary 

    mars_data = {
        'news_title' : news_title,
        'news_paragraph' : news_p,
        'featured_image' : featured_image_url,
        'mars_facts' : mars_info,
        'hemp_urls' : hemisphere_image_urls
    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()