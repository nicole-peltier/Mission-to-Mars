# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tage and save it as a 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for hemisphere in range(0,4):

   hemispheres = {}

   html = browser.html
   hemi_soup = soup(html, 'html.parser')
   hemi_click = browser.links.find_by_partial_text('Hemisphere')[hemisphere]
   hemi_click.click()

   # Find .jpg image
   html = browser.html
   full_img_soup = soup(html, 'html.parser')
   img_jpg = full_img_soup.find('img', class_='wide-image').get('src')
   full_img_url = f"https://marshemispheres.com/{img_jpg}"

   # Find the image title and set hemisphere dictionary
   title = full_img_soup.find('h2', class_='title').get_text()
   hemispheres = {'full_img_url': full_img_url, 'title': title}

   # Add Dictionary to list
   hemisphere_image_urls.append(hemispheres)

   # Go back to main page
   browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

browser.quit()