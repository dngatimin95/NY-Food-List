import re
import requests
import json
import pandas as pd
import numpy as np
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def get_site(url):
    """Get the content at `url` by making HTTP GET request.If content-type
    of response is HTML/XML, return the text content, else return None."""
    url.strip()
    try:
        with closing(get(url, stream = True)) as resp:
            if check_response(resp):
                return resp.content
            else:
                return None
    except RequestException as RE:
        print_error("Error encountered during requests to {0} : {1}".format(url, str(RE)))
        print("\nPlease try again once you have a stable internet connection.\n")
        exit
        #return None

def check_response(resp):
    """Returns True if the response seems to be HTML, False otherwise."""
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200 and content_type is not None
           and content_type.find('html') > -1)

def print_error(RE):
    """Function that prints error."""
    print(RE)

###########################################################
best_eater_url = 'https://ny.eater.com/maps/best-new-york-restaurants-38-map'
hottest_eater_url = 'https://ny.eater.com/maps/best-new-nyc-restaurants-heatmap'
best_infa_url = 'https://www.theinfatuation.com/new-york/guides/best-new-new-york-restaurants-hit-list'
hottest_infa_url = 'https://www.theinfatuation.com/new-york/guides/best-new-new-york-restaurants-hit-list'
###########################################################

def heading_eater_title(html, f_list):
    """"""
    fluff = ["Essential Restaurants", "Related Maps", "Hottest Restaurants"]

    for titles in html.findAll('h1'):
        rest_name = titles.get_text()
        if not(any(f in rest_name for f in fluff)):
            rest_name = re.sub('[0-9.\n]+', '', rest_name)
            rest_name = ' '.join(rest_name.split())
            if rest_name not in f_list:
                f_list.append(rest_name)
    return

def heading_infa_title(html,f_list):
    """Similar to previous function, except this one uses the infatuation website"""
    for  header in html.findAll('h3', class_= False):
        rest_name = header.get_text()
        rest_name = re.sub('[\n]+', '', rest_name)
        rest_name.strip()
        if rest_name not in f_list:
            f_list.append(rest_name)
    return

def food_list():
    url_list = [best_eater_url, hottest_eater_url, best_infa_url, hottest_infa_url]
    f_list = []
    
    for x in url_list:
        rest_link = get_site(x)
        rest_html = BeautifulSoup(rest_link, 'html.parser')
        if 'eater' in x:
            heading_eater_title(rest_html, f_list)
        elif 'infa' in x:
            heading_infa_title(rest_html, f_list)
    return f_list

def yelp_details(rest_name):
    """Uses yelp api to search up restaurant name to find the details including
        category, address, phone number and rating as well as number of reviews and
        stores it all into a list"""
    
    api_key = '******'
    headers = {'Authorization': 'Bearer %s' % api_key}
    d_list = []
    cat_list = []

    yelp_url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term':rest_name, 'location':'New York City'}
    rest_req = requests.get(yelp_url, params = params, headers = headers)

    if (rest_req.status_code == 200):
        rest_info = json.loads(rest_req.text)
        details = rest_info["businesses"]

        for y in details:
            cat = y["categories"]
            for i in cat: 
                cat_list.append(i["title"])
    
            d_list.append(", ".join(cat_list))
            d_list.append(" ".join(y["location"]["display_address"]))
            d_list.append(y["phone"])
            d_list.append(y["url"])
            #d_list.append(y["price"])
            d_list.append(y["rating"])
            d_list.append(y["review_count"])
            break

        return d_list
    else:
        return

def create_food_df():
    """Stores all details into a dataframe and returns a table with all restaurants"""
    rest_dict = {}

    for rest in food_list():
        details = yelp_details(rest)
        rest_dict[rest] = details

    df = pd.DataFrame.from_dict(rest_dict, orient = 'index')
    df.columns = ['Categories', 'Address', 'Phone No.', 'Website', 'Rating', 'No. of Reviews']
    return df

def update_df(i):
    old_df = pd.read_excel('C:\\Users\\****\\Documents\\GitHub\\New-Food-List\\Food_Scrap.xlsx')
    new_df = pd.concat([old_df,i])
    return new_df

def convert_to_csv(df, x):
    """Converts dataframe to csv file for easier access"""
    if x == True:
        df = update_df(df)
        return df.to_excel('C:\\Users\\****\\Documents\\GitHub\\New-Food-List\\Food_Scrap.xlsx')
    else:
        return df.to_excel('C:\\Users\\****\\Documents\\GitHub\\New-Food-List\\Monthly_Food_Scrap.xlsx')

def sort(df):
    df.sort_values(by=['Rating', 'No. of Reviews'])
    cat_count = {}
    for c in df['Categories']:
        if "," in c:
            c = c.split(",")
            for x in c:
                x = x.strip()
                if x not in cat_count.keys():
                    cat_count[x] = 1
                else:
                    cat_count[x] = cat_count[x]+1
        elif c not in cat_count.keys():
            cat_count[c] = 1
        else:
            cat_count[c] = cat_count[c]+1

    cat_count = sorted(cat_count.items(), key = lambda item:item[1], reverse = True)        
    return cat_count

def send_email(cat_count):
    pop_cat = cat_count[0][0]
    
    fromaddr = "******"
    toaddr = "******"
   
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
      
    msg['Subject'] = "Popular Restaurants this Month!"
    body = "Hey there,\n\nTry out some of these hot places! The most popular category this month seems to be " + str(pop_cat) + ". Looks good to try!"
    msg.attach(MIMEText(body, 'plain')) 
      
    filename = "Food_Scrap.xlsx"
    attachment = open("C:\\Users\\****\\Documents\\GitHub\\New-Food-List\\Monthly_Food_Scrap.xlsx", "rb") 
      
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
      
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()  
    s.login(fromaddr, "*****") 
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 

#ANALYSIS OF TOP FOOD, WHAT IS MOST TRENDING CATEGORY and predict next top spots (count category, knn)

new_df = create_food_df()
cat = sort(new_df)
convert_to_csv(new_df, False)
#convert_to_csv(new_df, True)
send_email(cat)


