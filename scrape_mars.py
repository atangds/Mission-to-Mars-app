from splinter import Browser
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

browser = Browser("chrome", executable_path="chromedriver.exe", headless=False)

url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
url3 = "https://twitter.com/marswxreport"
url4 = "https://space-facts.com/mars"
url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

def scrape():
    result_dict = {}

    # NASA Mars News
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")
    result_dict["news_title"] = soup.find("div", class_="content_title").a.text.strip()

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml") # repeat these 3 lines, otherwise the next line returns None
    result_dict["news_p"] = soup.find("div", class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image
    browser.visit(url2)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3) # added to avoid not finding the "more info" button
    browser.click_link_by_partial_text("more info")

    result_dict["featured_image_url"] = browser.find_by_tag("figure").first.find_by_tag("a")["href"]

    # Mars Weather
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "lxml")

    result_dict["mars_weather"] = soup3.find("p", class_="tweet-text", text=re.compile("Sol")).text

    # Mars Facts
    df = pd.read_html(url4, index_col=0)[0]
    df.index.name = None
    df.columns = [""]
    # html4 = df.to_html()
    # soup4 = BeautifulSoup(html4, "lxml")

    # result_dict["mars_facts"] = soup4.find("table")
    result_dict["mars_facts"] = df.to_html()

    # Mars Hemispheres
    browser.visit(url5)
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "lxml")

    hemisphere_image_urls = []
    for _ in soup5.find_all("h3"):
        d = {"title": " ".join(_.text.split(" ")[:-1])}
        browser.click_link_by_partial_text(_.text)
        d["img_url"] = browser.find_by_css("img[class='wide-image']").first["src"]
        hemisphere_image_urls.append(d)
        browser.click_link_by_partial_text("Back")
    result_dict["hemisphere_image_urls"] = hemisphere_image_urls

    # results
    return result_dict
