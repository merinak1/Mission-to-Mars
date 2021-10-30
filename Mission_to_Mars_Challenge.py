# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images news_p
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
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit() 

# ## Challenge 10 Deliverable 1

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.item', wait_time=1)

# Convert the browser html to a soup object and then quit the browser  
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.item')
browser.quit()

slide_elem.find('div', class_='description')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='description').h3.get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='description').p.get_text()
news_p

# ### JPL Space Images Featured Image

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

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
    #full_link = f'https://marshemispheres.com/{partial_link}'
    url_ls.append(f'https://marshemispheres.com/{partial_link}')
   
    full_image_elem = browser.find_by_tag('a')[1]
    full_image_elem.click()
    #print(full_image_elem) 
                
    browser.back()   
 
# print url_ls
url_ls

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
hemisphere_image_urls

# 5. Quit the browser
browser.quit()