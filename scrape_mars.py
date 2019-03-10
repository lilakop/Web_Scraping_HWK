from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

## create functions called scrap that will execute all scraping code and return on python dictionary containing
##all of the scraped data


def init_browser():
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)

def scrape():
	browser = init_browser()

	mars_data = {}


	##NASA MARS DATA
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	news_title = soup.find('div', class_='content_title').find('a').text
	news_p = soup.find('div', class_='article_teaser_body').text
	mars_data["news_title"] = news_title
	mars_data["news_p"] = news_p

	## JPL MARS SPACE IMAGES
	image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url_featured)
	html_image = browser.html
	soup = bs(html_image, 'html.parser')
	image_url =  soup.find("img", class_="thumb")["src"]
	featured_image_url = "https://jpl.nasa.gov"+image_url
	mars_data["featured_image_url"] = featured_image_url

	##MARS WEATHER
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(weather_url)
	html_weather = browser.html
	soup = bs(html_weather, 'html.parser')
	mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
	mars_data["mars_weather"] = mars_weather

	##MARS FACTS
	facts_url = "https://space-facts.com/mars/"
	mars_facts = pd.read_html(facts_url)
	mars_df = mars_facts[0]
	mars_df.columns = ['Description','Value']
	mars_df.set_index('Description', inplace=True)
	mars_data_html = mars_df.to_html()
	mars_data["weather_tweet"] = mars_data_html

	## MARS HEMISPHERES
	hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemispheres_url)

	html_hemispheres = browser.html
	soup = bs(html_hemispheres, 'html.parser')
	items = soup.find_all('div', class_='item')
	hemisphere_image_urls= []

	for i in items:
	    title = i.find('h3').text
	    partial_url = i.find('a', class_='itemLink product-item')['href']
	    browser.visit('https://astrogeology.usgs.gov' + partial_url)
	    partial_img_html = browser.html
	    soup = bs(partial_img_html, 'html.parser')
	    img_url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
	    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

	mars_data['hemisphere_image_urls'] = hemisphere_image_urls
	return mars_data

