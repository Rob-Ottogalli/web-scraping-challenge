# Import dependencies
import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def nasa_mars_news():
    # Set variable to hold URL
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Retrieve page with the requests module
    response = requests.get(nasa_url)

    # Create BeautifulSoup object; parse with 'html'
    soup = bs(response.text, 'html')

    # Retrieve the parent div for the grid containing the article titles
    results = soup.find_all('div', class_='grid_layout')[1]
    # Scrape data to get title
    div = results.find("div", class_="content_title")
    a = div.a

    # Set variable to hold title
    title = div.a.text

    # Scrape data to get paragraph teaser
    divp = results.find("div", class_="rollover_description_inner")
    # Set variable to hold paragraph teaser
    paragraph = divp.text
 
    # Store data in a dictionary
    nasa_dict = {
        "Nasa_title": title,
        "Nasa_teaser": paragraph
    }

    # Return results
    return nasa_dict

def JPL_mars_images():
    # Initialize Browser
    browser = init_browser()

    # Set variable to hold URL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Visit URL
    browser.visit(jpl_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the element containing the main image
    results = soup.find_all("div", class_="carousel_items")[0]

    # Use Beautiful Soup's find() method to retrieve attribute of image URL
    article = results.find("article")
    # Grab style attribute within article tag
    style = article["style"]

    # Trim Style attribute to isolate the href image URL
    trimmed_style = style.split("'")

    # Save trimmed URL as a variable
    href = trimmed_style[1]

    # Store image URL to a variable
    featured_image_url = f"https://www.jpl.nasa.gov{href}"

    # Close the browser after scraping
    browser.quit()

    # Return results
    return featured_image_url

def mars_weather():
    # Set variable to hold URL
    mars_url = "https://twitter.com/marswxreport?lang=en"

    # Retrieve page with the requests module
    response = requests.get(mars_url)

    # Create BeautifulSoup object; parse with 'html'
    soup = bs(response.text, 'html')

    # Retrieve the parent div for the paragraph containing the most recent weather Tweet
    results = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0]

    # Set variable to hold title
    weather = results.text

    # Return results
    return weather

def mars_facts():
    # Store URL
    facts_url = "https://space-facts.com/mars/"

    #Read table
    tables = pd.read_html(facts_url)

    # Create dataframe by selecting row from table
    mars_df = tables[0]

    # Rename Columns
    mars_df = mars_df.rename(columns={
                            0: "Category",
                            1: "Fact"
                            })

    # Convert table to HTML string
    mars_html_table = mars_df.to_html(index=False)

    # Return results
    return mars_html_table

def find_img_dict(hemisphere):
    # Initialize Browser
    browser = init_browser()
    
    # Set variable to hold URL
    url = f"https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemisphere}_enhanced"
    
    # visit URL
    browser.visit(url)
    
    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve element that contains URL download link
    link_element = soup.find_all('div', class_='downloads')[0]

    # Use Beautiful Soup's find() method to navigate and save to IMG URL variable
    ul = link_element.find("ul")
    li = ul.find("li")
    a = li.find("a")
    img_url = a["href"]

    # Retrieve element that contains hemisphere name
    h2 = soup.find_all('h2', class_='title')[0]
    
    # Find name of hemisphere
    text=h2.text
    # Isolate string name of hemisphere. Split to remove word "Enhanced"
    hemi_string = text.split("Enhanced")
    # Save hemisphere name as variable
    hemi_name = hemi_string[0]
    
    # Save hemisphere name and URL as a dictionary
    Dict = {
        "hemi_title": hemi_name, 
        "img_url": img_url
    }
    # Close the browser after scraping
    browser.quit()
    
    # Return dictionary
    return Dict

def mars_hemispheres():
    # Set list of strings to hold hemisphere names
    hemi_list = ["cerberus", "schiaparelli", "syrtis_major", "valles_marineris"]

    # Set list to hold dictionary data for each hemisphere
    hemi_data_list = []

    # Loop through all 4 hemispheres in list
    for hemi in hemi_list:
        # Set variable to hold data for a single hemisphere
        dictionary = find_img_dict(hemi)
        
        # Append that hemisphere's data to the list
        hemi_data_list.append(dictionary)
    
    # Return resulsts
    return hemi_data_list

def scrape_info():
    nasa = nasa_mars_news()
    mars_images = JPL_mars_images()
    weather_report = mars_weather()
    mars_table = mars_facts()
    hemi_data = mars_hemispheres()

    # Store data in a dictionary
    mars_data = {
        "NASA_Headlines": nasa,
        "Mars_Images": mars_images,
        "Mars_Weather": weather_report,
        "Mars_Facts": mars_table,
        "Mars_Hemispheres": hemi_data
    }

    # Return dictionary
    return mars_data