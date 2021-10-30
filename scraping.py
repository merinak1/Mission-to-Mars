# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
 

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images 
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
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
       
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
 
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap  
    # added table bordered and table hover      
    return df.to_html(classes="table table-striped table-bordered table-hover")

#Challenge 10 Deliverable 1 Code
def hemisphere(browser):
          
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.description', wait_time=1)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #3. Write code to retrieve the image urls and titles for each hemisphere.  
    html = browser.html
    url_soup = soup(html, 'html.parser')
    urls = url_soup.find_all('div', class_='description')

    # print(urls)
    #get all the urls in url_ls list
    url_ls=[]

    for url in urls:
        title = url.a.h3.text
        
        #print(title)
        #print(url.a['href'])
        
        #Get image url
        partial_link= url.a['href'] 
        url_ls.append(f'https://marshemispheres.com/{partial_link}')
    
        full_image_elem = browser.find_by_tag('a')[1]
        #full_image_elem.click()
        #print(full_image_elem) 
                    
        #browser.back()  
    
    title_ls =[]
    img_url_ls =[]

    for x in url_ls:
        hemispheres = {}
        #print(x)
        
        #visit the browser
        browser.visit(x)
        html = browser.html
        title_img_soup = soup(html, 'html.parser')
        
        # get the title 
        title = title_img_soup.h2.text
        title_ls.append(title)
        
        #Get the img link
        img_url = title_img_soup.find_all('li')[0].a['href']
        
        # Use the base url to create an absolute url
        img_full_url = f"https://marshemispheres.com/{img_url}"
        img_url_ls.append(img_full_url)
        
        hemispheres = {'img_url':img_full_url , 'title': title}
        hemisphere_image_urls.append(hemispheres)
        # print(img_url)

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())