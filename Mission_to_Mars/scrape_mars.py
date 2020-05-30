from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time


# initiate chromebrowser
browser = Browser('chrome', executable_path='chromedriver.exe',headless=False)

def scrape():


    # # NASA Mars News

    # use browser to visit NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # delay 1 second for loading the page
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=5)

    html = browser.html
    soup = bs(html, 'html.parser')

    # search for news titles
    title_results = soup.find_all('div', class_='content_title')

    # search for paragraph text under news titles
    p_results = soup.find_all('div', class_='article_teaser_body')

    # extract first title and paragraph, and assign to variables
    news_title = title_results[0].text
    news_p = p_results[0].text

    #print(news_title)
    #print(news_p)

    # # JPL Mars Space Images - Featured Image

        # open browser to JPL Featured Image
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')


    # click through to find full image
    browser.click_link_by_partial_text('FULL IMAGE')



    # click again for full large image
    time.sleep(5)
    browser.click_link_by_partial_text('more info')


    html = browser.html
    soup = bs(html, 'html.parser')

    # search for image source
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img_url = 'https://www.jpl.nasa.gov' + relative_img_path

    #print(featured_img_url)


    # #  Mars Weather

   
    # open browser to Mars Weather Twitter Account
    browser.visit('https://twitter.com/marswxreport?lang=en')



    # HTML Object 
    html_weather = browser.html

    # parse HTML with bs
    soup = bs(html_weather, 'html.parser')

    # find all elements that contain tweets
    latest_tweets = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    #latest_tweets = latest_tweets.to_html
    # find first tweet with "sol" 
    mars_weather = None
    for tweet in latest_tweets:
        mars_weather = tweet.text
        if mars_weather.find("InSight sol 534") != -1:
            print(mars_weather)
            break
        else:
            print(mars_weather)
            continue
        


    # # Mars Facts

   
    # use Pandas to scrape data
    tables = pd.read_html('https://space-facts.com/mars/')

    # take first table for Mars facts
    df_mars_facts = tables[0]

    # rename columns and set index
    df_mars_facts.columns=['description', 'value']
    df_mars_facts.set_index('description', inplace=True)



    # save df to html in resources folder
    df_mars_facts.to_html('Resources/mars_facts.html')



    # convert to HTML string
    mars_facts = df_mars_facts.to_html(header=True, index=True)
    
    #print(mars_facts)


    # # Mars Hemispheres


    # open browser to USGS Astrogeology site
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')



    html = browser.html
    soup = bs(html, 'html.parser')

    hemi_names = []

    # search for the names of all four hemispheres
    results = soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    # get text and store in list
    for name in hemispheres:
        hemi_names.append(name.text)

    hemi_names


    # search for thumbnail links to get full sized image
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
        
        # if the thumbnail element has an image
        if (thumbnail.img):
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            thumbnail_links.append(thumbnail_url)

    thumbnail_links


    full_imgs = []

    for url in thumbnail_links:
        
        # click through each thumbanil link
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
        
        # combine the relative image path for full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
        
        # add full image links to a list
        full_imgs.append(img_link)

    #full_imgs


    # use zip to make list of hemisphere names and hemisphere image links
    mars_hemi_zip = zip(hemi_names, full_imgs)

    hemisphere_image_urls = []

    # iterate through the zipped object for dict
    for title, img in mars_hemi_zip:
        
        mars_hemi_dict = {}
        
        # add hemisphere title to dictionary
        mars_hemi_dict['title'] = title
        
        # add image url to dictionary
        mars_hemi_dict['img_url'] = img
        
        # apend the list with dictionaries
        hemisphere_image_urls.append(mars_hemi_dict)

    #hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img_url,
        "weather": mars_weather,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_image_urls
    }
    # Return results
    return mars_data

    # Close the browser after scraping
    browser.quit()
    #browser.close()

