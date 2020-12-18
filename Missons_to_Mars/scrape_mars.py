from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pprint
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Program Files (x86)/Chrome Driver/chromedriver.exe"}
    return Browser("chrome", executable_path, headless=False)

def scrape():
    ############ defining the urls needed

    ####---------------------------------------
    ##url for the Nasa news site
    nasa_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    ####---------------------------------------
    ##urls for the jpl site

    #base url for jpl site
    jpl_base_url="https://www.jpl.nasa.gov"

    #url for "Mars" search for jpl
    jpl_mars_url=jpl_base_url+"/spaceimages/?search=&category=Mars"

    ####---------------------------------------
    ##url for space facts page
    mars_facts_url="https://space-facts.com/mars/"

    ####---------------------------------------
    ##urls for hemisphere data

    #base url for hemisphere site
    hem_base_url="https://astrogeology.usgs.gov"

    #page we'll use to access each hemisphere page
    hem_url=hem_base_url+"/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    #using splinter since requests is only returning partial results
    executable_path = {'executable_path': "C:/Program Files (x86)/Chrome Driver/chromedriver.exe"}

    browser = Browser('chrome', executable_path, headless=False)

    ########### in this block, we're going to try to run all the browser.visit(x) and html=browser.html statements so we can close the the browser out more quickly

    #opening browser to the nasa news website
    browser.visit(nasa_news_url)
    time.sleep(2)
    #extracting html from the nasa news website
    nasa_news_html=browser.html



    #opening browser to jpl site 
    browser.visit(jpl_mars_url)
    time.sleep(2)
    #extracting html
    jpl_html=browser.html
    # browser.quit()


    #visiting mars facts page and grabbing html
    browser.visit(mars_facts_url)
    time.sleep(2)
    ### defining the html
    mars_facts_html=browser.html

    ####------------------------------------------------------------------------------
    ####visiting the mars hemispheres site and grabbing the html

    browser.visit(hem_url)
    time.sleep(2)
    hem_html=browser.html

    #parsing hemisphere site
    hem_soup=bs(hem_html,'html.parser')

    ### get the image url string, hemisphere title containing the hemispher name

    ##a results set that contain the links to each hemisphere
    hem_items=hem_soup.find_all(class_="item")

    hem_list=[]

    ### visit each hemisphere page and...
    for result in hem_items:
        print("--------")

        #opens to the browser to the current hemisphere page
        browser.visit(hem_base_url+result.a["href"])
        time.sleep(1)

        ##opening the image to view it full size
        browser.find_link_by_text("Open").first.click()
        time.sleep(1)

        #defines the current html 
        current_html=browser.html
        cur_soup=bs(current_html,'html.parser')
        
        # # adds to the dictionary. The key is the hemisphere title and the value is the image link

        current_dict={}
        current_dict["title"]=cur_soup.find('title').text
        current_dict["img_url"]=hem_base_url+cur_soup.find('img',class_="wide-image")['src']

        hem_list.append(current_dict)


    browser.quit()

    #parsing the html
    nasa_news_soup=bs(nasa_news_html,'html.parser')

    #finds the list in the html which contains the article titles and paragraphs we seek

    first_art=nasa_news_soup.find(class_="item_list")

    # print(first_art.text)

    ## gets the articles title
    first_art.find(class_="content_title").text
    first_art.find(class_="article_teaser_body").text

    art_dict={
        "news_title":first_art.find(class_="content_title").text,
        "news_p":first_art.find(class_="article_teaser_body").text
    }

    #parsing the html for the jpl site
    jpl_soup=bs(jpl_html,'html.parser')

    ## finds the partial url for the first image
    partial_jpl_image_url=jpl_soup.find(class_="slide").a["data-fancybox-href"]

    ## joins the partial url to the initial url to get the full image url
    featured_image_url=jpl_base_url+partial_jpl_image_url

    #grabbing the first table from the mars facts html and turning it into a dataframe

    fact_df=pd.read_html(mars_facts_html)[0]
    fact_df

    fact_table=fact_df.to_html(header=False,index=False)

    ##final dictionary
    final_dict={
        "Hemispheres":hem_list,
        "Articles":art_dict,
        "FeaturedImage":featured_image_url,
        "Facts":fact_table
    }
    print("scraping done")
    return final_dict
    #### END OF SCRAPING SECTION ##########

