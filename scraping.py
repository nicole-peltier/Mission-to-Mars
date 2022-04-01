# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_data(browser),
        "last_modified": dt.datetime.now()

    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p
    

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    facts = df.to_html()

    # Convert dataframe into HTML format, add bootstrap
    return facts


## Mars Hemisphere Data
def hemisphere_data(browser):
    # Visit the hemisphere site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create list to hold images and titles
    hemisphere_image_urls = []

    # For Loop to Retrieve image URLS and titles for each hemisphere
    for hemisphere in range(0,4):

        hemispheres = {}

        hemi_click = browser.links.find_by_partial_text('Hemisphere')[hemisphere]
        hemi_click.click()

        # Find .jpg image
        html = browser.html
        full_img_soup = soup(html, 'html.parser')
        img_jpg = full_img_soup.find('img', class_='wide-image').get('src')
        full_img_url = f"https://marshemispheres.com/{img_jpg}"

        # Find the image title and set hemisphere dictionary
        title = full_img_soup.find('h2', class_='title').get_text()
        hemisphere = {'full_img_url': full_img_url, 'title': title}

        # Add Dictionary to list
        hemisphere_image_urls.append(hemisphere)

        # Go back to main page
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scaped data
    print(scrape_all())