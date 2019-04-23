#!/usr/bin/env python3


import json
import random 
import time
import datetime
import codecs
import requests
import os

from bs4 import BeautifulSoup
from collections import Counter
from random import randint
from random import shuffle
from datetime import datetime

from ..models.model import Sneaker, User, ShoeView

path = 'run/src/json/total190120.json'

def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""
    
    delimiters = tuple(delimiters)
    stack = [string,]
    
    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)     
    return stack


def get_current_date():
    ts = time.time() 
    new_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    date = new_time.split(' ')[0]
    return date

def open_shoe_data(shoe):
    with open(path) as file:
        data = json.load(file)
        for k,v in data.items():
            if data[k]['name'] == shoe:
                shoeData = data[k]
                return shoeData

def get_shoeKey(name):
    with open(path) as file:
        data = json.load(file)
        for key,value in data.items():
            if data[key]['name'] == name:
                return key

def price_premium(retail,average):
    if retail == '--' or average == '--':
        return None
    else:
        fltRetail = float(retail)
        fltAvg    = float(average)
        difference = fltAvg - fltRetail
        value = difference/fltRetail
        premium = '{:.2f}'.format(value*100)
        return premium

def color_list():
    sneaker = Sneaker()
    colorlist = sneaker.get_color_list()

def shoes_like_list(shoename):
    """ 
    ----------------------------
    SHOE SIMILAR IN SHOE_ID PAGE
    RANDOM VIEW RESULTS
    ----------------------------
    """
    sneaker = Sneaker()
    shoe_list = sneaker.get_shoes_no_placeholder('all')
    like_list_major, like_list_minor = [], []
    for shoe in shoe_list: 

        """ 
        -------------------------------------------
        IGNORE WORDS THAT WONT PRODUCE GOOD RESULTS
        -------------------------------------------
        """

        ignoreList = [ 'of', 'a', 'the', 'air', 'nike', 'adidas', 'jordan', 'red', 
                       'white', 'black', 'green', 'blue', 'pink', 'gum', 'yellow' ]

        searchShoe = shoename.lower().split(' ')
        likeShoe = shoe.lower().split(' ')

        """ 
        ---------------------------
        CREATE PAIRING STRENGTH (x)
        SPECIFIC CONDITION = TRUE
        ---------------------------
        """
        x = 0
        lessSpecific = True

        """ 
        -----------------------------
        CHECK TERMS IN SEARCHED SHOES
        -----------------------------
        """

        for terms in searchShoe:
            if terms in ignoreList:
                pass
            elif terms in likeShoe:
                x += 1
            else:
                pass

        """ 
        ----------------------------
        IF PAIRING IS GREATER THAN 4
           RETURN >= 4
        ELSE:
           RETURN 1 < x < 4
        ----------------------------
        """

        if x >= 4:
            lessSpecific = False
            like_list_major.append(shoe)
        if 1 < x < 4:
            like_list_minor.append(shoe)

    if lessSpecific: 
        shuffle(like_list_minor)
        return like_list_minor[:6]
    else: 
        shuffle(like_list_major)
        return like_list_major[:6]


def search_terms(string,brand):

    """ 
    -------------------------
    FILTER FOR SEARCH RESULTS
    -------------------------
    """

    relevanceListofOne, relevanceListofMany = [], []
    sneaker = Sneaker() 
    shoes = sneaker.get_shoes(brand)

    """ 
    -----------------------------
    CHECK FOR ONE WORD SIMILARITY
    SINGLE CONDITION = TRUE
    -----------------------------
    """

    single = True
    for shoe in shoes:
        ignoreList = [ 'of', 'a', 'the', 'adidas', 'nike', 'jordan' ]
        searchTerms = string.lower().split(' ')
        searchFor = shoe.lower().split(' ')
        x = 0
        for terms in searchTerms:
            if terms in ignoreList:
                pass
            elif terms in searchFor:
                x += 1
            else:
                pass
        if x == 0:
            pass
        elif x > 1:
            single = False
            relevanceListofMany.append((shoe,x))
        else:
            relevanceListofOne.append((shoe,x))
    
    """ 
    -----------------------------
    IF ONE WORD SIMILARITY ONLY
    ie. "KYRIE" 
        RETURN ONE-LIST
    ELSE:
        RETURN MANY-LIST
    -----------------------------
    """
    
    if single:
        relevanceListofOne = [relevant[0] for relevant in relevanceListofOne]
        return relevanceListofOne
    else:
        relevanceListofMany = sorted(relevanceListofMany, key=lambda x:x[1])[::-1]
        relevanceListofMany = [relevant[0] for relevant in relevanceListofMany]
        return relevanceListofMany

def date_to_unix(date):
    split = date.split("-")
    year,month,day = split[0],split[1],split[2]
    s = day+'/'+month+'/'+year
    time = datetime.datetime.strptime(s, "%d/%m/%Y").timestamp()
    return time
    
def brander(brand):
    if brand.upper() == 'nike'.upper():
        return 'nke'
    elif brand.upper() == 'adidas'.upper():
        return 'ads'
    elif brand.upper() == 'jordan'.upper():
        return 'jrd'
    elif brand.upper() == 'other'.upper():
        return 'otb'
    elif brand.upper() == 'all'.upper():
        return 'all'
    else:
        print('Brand not recognized. Try searching "Others"?')
        return False

def display_rand_shoes(brand,num):

    sneaker = Sneaker() 
    shoe_list = sneaker.get_shoes_no_placeholder(brand)
    shuffle(shoe_list)
    return shoe_list[:int(num)]
    

def shoeValues(list,val,par):
    
    with open(path) as file:
        data = json.load(file)
        val_list = []

        if val == 'avg_sale_price':

            for key,value in data.items():
                for name in list:
                    if data[key]['name'] == name:
                        price = data[key]['avg_sale_price'].replace(',','').split('$')[1]
                        val_list.append(int(price))
        sortedValues = sorted(val_list)
        if par == 'h':
            val_list = sortedValues[::-1]
            return val_list
        else:
            return val_list

"""BS4 CHECKS CURRENT INFO"""
def shoe_info(url):
    """CONTAINERS"""
    shoe_html = requests.get(url).content
    print(url)
    shoe_soup = BeautifulSoup(shoe_html, 'html.parser')
    shoe_container = shoe_soup.find("div", {"class": "product-view"})
    """HISTORICAL"""
    twelve_month_historical = shoe_container.find('div', {'class': 'gauges'}).get_text().strip()
    twelve_data = tsplit(twelve_month_historical,('# of Sales','Price Premium(Over Original Retail Price)','Average Sale Price'))
    total_sales = twelve_data[1]
    price_premium = twelve_data[2]
    avg_sale_price = twelve_data[3]
    newData = { 
                "total_sales" : total_sales,
                "avg_sale_price" : avg_sale_price
        }
    return newData

"""BS4 SCRAPER"""
def update_shoe(name):
    try:
        sneaker                   = Sneaker(name=name)
        updatedData               = shoe_info(sneaker.url)
        premium                   = price_premium(sneaker.retail_price,updatedData['avg_sale_price'].strip('$').replace(',',''))
        sneaker.brand	          = sneaker.brand	
        sneaker.type              = sneaker.type
        sneaker.name              = sneaker.name
        sneaker.colorway          = sneaker.colorway 	
        sneaker.image             = sneaker.image  
        sneaker.image_placeholder = sneaker.image_placeholder
        sneaker.release_date      = sneaker.release_date 
        sneaker.retail_price      = sneaker.retail_price
        sneaker.ticker            = sneaker.ticker 
        sneaker.total_sales       = updatedData['total_sales'].replace(',','')
        sneaker.url               = sneaker.url
        sneaker.avg_sale_price    = updatedData['avg_sale_price'].strip('$').replace(',','')
        sneaker.premium           = premium
        sneaker.save(name)
    except AttributeError:
        update_shoe(name)

def scrape_new_shoe(url):
    try:
        """CONTAINERS"""
        shoe_html = requests.get(url).content
        shoe_soup = BeautifulSoup(shoe_html, 'html.parser')
        shoe_container = shoe_soup.find("div", {"class": "product-view"})
        header_stat = shoe_container.find_all('div', {'class': 'header-stat'})
        """HEADER INFO"""
        name = shoe_container.find('h1').get_text().replace('/','-').strip()
        new_name = name.replace('?','')
        image = shoe_container.find('div', {'class': 'product-media'}).img['src']
        ticker = header_stat[1].get_text().strip().split(' ')[1]
        """PRODUCT INFO"""
        product_info = shoe_container.find('div', {'class': 'product-info'}).get_text().strip()
        product_data = tsplit(product_info,('Style ',' Colorway ',' Retail Price ', ' Release Date '))
        colorway     = product_data[2]
        retail_price = product_data[3]
        release_date = product_data[4][:10]
        """MARKET INFO"""
        market_summary = shoe_container.find('div', {'class': 'product-market-summary'}).get_text().strip()
        market_data    = tsplit(market_summary,('52 Week High ',' | Low ','Trade Range (12 Mos.)','Volatility'))
        year_high      = market_data[1]
        year_low       = market_data[2]
        trade_range    = market_data[3]
        """HISTORICAL"""
        twelve_month_historical = shoe_container.find('div', {'class': 'gauges'}).get_text().strip()
        twelve_data = tsplit(twelve_month_historical,('# of Sales','Price Premium(Over Original Retail Price)','Average Sale Price'))
        total_sales = twelve_data[1]
        avg_sale_price = twelve_data[3]
        """BRAND INFO"""
        trail = shoe_container.find('div', {'class': 'grails-crumbs'}).get_text()
        identifier = trail[12:13]

        if identifier == 'O':
            brand = 'Other'
        elif identifier == 'a':
            brand = 'Adidas'
        elif identifier == 'N':
            brand = 'Nike'
        elif identifier == 'J':
            brand = 'Jordan'
        else:
            brand = 'Other'

        new_totalSales = total_sales.replace(',','')
        
        retailPrice = retail_price.strip('$')
        new_retailPrice = retailPrice.replace(',','')

        avgSalePrice = avg_sale_price.strip('$')
        new_avgSalePrice = avgSalePrice.replace(',','')

        yearHigh = year_high.strip('$')
        new_yearHigh = yearHigh.replace(',','')

        yearLow = year_low.strip('$')
        new_yearLow = yearLow.replace(',','')

        if 'Harden' in name.split(' ') and brand != 'Nike':
            type = 'Harden'
        elif 'Curry' in name.split(' ') and brand != 'Nike':
            type = 'Curry'
        elif 'PG' in name.split(' '):
            type = 'PG'
        elif 'Westbrook' in name.split(' '):
            type = 'Westbrook'
        elif 'Kyrie' in name.split(' '):
            type = 'Kyrie'
        elif 'Dame' in name.split(' '):
            type = 'Dame'
        elif 'React' in name.split(' '):
            type = 'React'
        elif 'Foamposite' in name.split(' '):
            type = 'Foamposite'
        elif 'NMD' in name.split(' '):
            type = 'NMD'
        elif 'Ultra Boost' in name.split(' ') or 'UltraBoost' in name.split(' '):
            type = 'Ultraboost'
        elif 'Air Force' in name.split(' '):
            type = 'Air Force'
        elif 'Air Max' in name.split(' '):
            type = 'Air Max'
        elif 'SB' in name.split(' '):
            type = 'SB'
        elif 'React' in name.split(' '):
            type = 'React'
        elif 'Foamposite' in name.split(' '):
            type = 'Foamposite'
        elif 'KD' in name.split(' '):
            type = 'KD'
        elif 'Lebron' in name.split(' ') or 'UltraBoost' in name.split(' '):
            type = 'Lebron'
        elif 'Kobe' in name.split(' '):
            type = 'Kobe'
        elif 'Yeezy' in name.split(' '):
            type = 'Yeezy'
        elif 'Jordan' in name.split(' ') and '1' in name.split(' '):
            type = '1'
        elif 'Jordan' in name.split(' ') and '2' in name.split(' '):
            type = '2'
        elif 'Jordan' in name.split(' ') and '3' in name.split(' '):
            type = '3'
        elif 'Jordan' in name.split(' ') and '4' in name.split(' '):
            type = '4'
        elif 'Jordan' in name.split(' ') and '5' in name.split(' '):
            type = '5'
        elif 'Jordan' in name.split(' ') and '6' in name.split(' '):
            type = '6'
        else:
            type = 'Other'

        if new_avgSalePrice == '--' or new_retailPrice =='--':
            premium = None
        else:
            value = (float(new_avgSalePrice)-float(new_retailPrice))/float(new_retailPrice)
            premium = '{:.2f}'.format(value*100)

        data = { 
                "name" : new_name,
                "url" : url,
                "brand": brand,
                "type": type,
                "image" : image,
                "image_placeholder" : '--',
                "ticker" : ticker,
                "colorway" : colorway,
                "retail_price" : new_retailPrice,
                "release_date" : release_date,
                "year_high" : new_yearHigh,
                "year_low" : new_yearLow,
                "trade_range" : trade_range,
                "total_sales" : new_totalSales,
                "avg_sale_price" : new_avgSalePrice,
                "premium" : premium
            }

    except AttributeError:
        print('attribute error trying again')
        scrape_new_shoe(url)

    except IndexError:
        print('index error, try a valid url')
        data = {}
    
    return data

def insert_shoe_to_db(data):
    sneaker = Sneaker()
    sneaker.brand	          = data['brand']
    sneaker.type              = data['type']
    sneaker.name              = data['name']
    sneaker.colorway          = data['colorway']	
    sneaker.image             = data['image'] 
    sneaker.image_placeholder = data['image_placeholder'] 
    sneaker.release_date      = data['release_date'] 
    sneaker.retail_price      = data['retail_price']
    sneaker.ticker            = data['ticker']
    sneaker.total_sales       = data['total_sales']
    sneaker.url               = data['url'] 
    sneaker.year_high         = data['year_high']
    sneaker.year_low          = data['year_low']
    sneaker.avg_sale_price    = data['avg_sale_price']
    sneaker.premium           = data['premium']
    sneaker.save(data['name'])

def download_sneaker_img(data):
    img_link = data['image']
    print(img_link)
    name = data['name']
            
    if 'Placeholder' in img_link.split('-'):

        placeholder = open('/Users/ahn.ch/Desktop/sb_placeholder.jpg')
        f = open('run/src/static/{}.jpg'.format(name),'wb')
        f.write(placeholder.read())
        f.close()

        print('Placeholder Added')

    else:
        picture_request = requests.get(img_link)
        if picture_request.status_code == 200:
            with open("run/src/static/{}.jpg".format(name), 'wb') as f:
                f.write(picture_request.content)

def account_pairing_scores(pk):

    user = User()
    account_preferences = user.get_account_preferences(pk)
    other_preferences = user.get_other_account_preferences(pk)

    print(account_preferences)
    print(other_preferences)

    pairing_scores = []
    for key,value in account_preferences.items():

        user_brand = account_preferences[key]['brand']
        user_color = account_preferences[key]['color']
        
        for key, value in other_preferences.items():

            brand_score, color_score = 0, 0

            for brand in other_preferences[key]['brand']:
                if brand in user_brand:
                    brand_score += 18
            for color in other_preferences[key]['color']:
                if color in user_color:
                    color_score += 12
            
            pairing_scores.append((key,(brand_score+color_score)))

    sorted_pairing_scores = sorted(pairing_scores, key=lambda x:x[1])[::-1]
    pk1 = sorted_pairing_scores[0][0]
    pk2 = sorted_pairing_scores[1][0]
    return [pk1,pk2]

def line_graph_labels(box, val):
    date_labels, final_dates, num_labels, values = [], [], [], []
    for key in box.keys():
        if box[key]['date'] not in date_labels:
            date_labels.append(box[key]['date'])
    if val == 'value':
        for key in box.keys():
            for i in range(len(date_labels)):
                if box[key]['date'] == date_labels[i]:
                    if box[key]['type'] != 'SELL':
                        num_labels.append({box[key]['date']: box[key]['{}'.format(val)]})
                    else:
                        num_labels.append({box[key]['date']: 0 })
                else:
                    pass
    elif val == 'profit':
        for key in box.keys():
            for i in range(len(date_labels)):
                if box[key]['date'] == date_labels[i]:
                    num_labels.append({box[key]['date']: box[key]['{}'.format(val)]})
                else:
                    pass
    c = Counter()
    for d in num_labels:
        c.update(d)
    result = [{key: value} for key, value in c.items()]
    for vals in result:
        for key in vals.keys():
            values.append(vals[key])
    final = [sum(values[:i+1]) for i in range(len(values))]
    for date in date_labels:
        date_list = date.split('-')
        date = str(date_list[1]).replace('0','')+'/'+str(date_list[2]).replace('0','')+'/'+str(date_list[0])[-2:]
        final_dates.append(date)
    return [final_dates,final]

def add_dict_total(dict, val):
    """VAL is a parameter to search for price_bought,
       value and profit which are values in shoebox dict"""
    sum_list = []
    for key in dict.keys():
        if val == 'value':
            if dict[key]['type'] != 'SELL':
                sum_list.append(dict[key][val])
        else:
            sum_list.append(dict[key][val])
    return sum(sum_list)