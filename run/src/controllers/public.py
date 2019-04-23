#!/usr/bin/env python3


import os
import json
import codecs
import requests
import time
import random

from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename

from flask import Blueprint,render_template,request,session,redirect,url_for

from ..extensions.loaders import tsplit, shoes_like_list
from ..models.model import User,ShoeView,ShoeBox,Sneaker

UPLOAD_FOLDER = '/Users/ahn.ch/Projects/shoe_data/run/src/static'

elekid = Blueprint('public',__name__)

"""INACTIVE"""

# @elekid.route('/finder',methods=['GET','POST'])
# def finder():
#     if request.method == 'GET':

#         return render_template('public/finder.html')
#     elif request.method == "POST":

#         if request.form['post_button'] == 'Submit':

#             file = request.files['file']
#             print(file)
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(electabuzz.config['UPLOAD_FOLDER'+'/user_inputs'], filename))

#                 model = tf.keras.models.load_model("/Users/ahn.ch/Projects/shoe_data/run/src/32x3-CNN.model")
#                 prediction = model.predict([prepare('/Users/ahn.ch/Projects/shoe_data/run/src/static/{}'.format(filename))])
#                 brand = CATEGORIES[int(prediction[0][0])]
#                 print(brand)

#             price_min = request.form['min'].strip('$')
#             price_max = request.form['max'].strip('$')

#             int_min = int(price_min)
#             int_max = int(price_max)

#             premium  = request.form.get('premium')
#             value = request.form.get('value')

#             black  = request.form.get('black')
#             white  = request.form.get('white')
#             red    = request.form.get('red')
#             orange = request.form.get('orange')
#             yellow = request.form.get('yellow')
#             green  = request.form.get('green')
#             blue   = request.form.get('blue')
#             purple = request.form.get('purple')

#             colorList = [black,white,red,orange,yellow,green,blue,purple]
#             valueList = [premium,value]

#             l = len(colorList)
#             for x in range(l-1,-1,-1):
#                 if colorList[x] is None:
#                     colorList.pop(x)
            
#             l = len(valueList)
#             for x in range(l-1,-1,-1):
#                 if valueList[x] is None:
#                     valueList.pop(x)

#             print(colorList)
#             print(valueList)

#             brand = 'Nike'

#             sneaker = Sneaker()

#             shoeList = sneaker.finder(int_min, int_max, brand, valueList, colorList)

#             shoeData = {}
#             for shoe in shoeList:
#                 s = Sneaker(name=shoe)
#                 shoeData[shoe] = {
#                     'value': s.avg_sale_price,
#                     'premium': s.premium
#                 }
                
#             print(shoeData)

#             return render_template('public/found_shoes.html', shoeList=shoeList, shoeData=shoeData)
#         else:
#             image_button = request.form['post_button']
#             print(image_button)

#             price_min = request.form['min'].strip('$')
#             price_max = request.form['max'].strip('$')

#             int_min = int(price_min)
#             int_max = int(price_max)

#             premium  = request.form.get('premium')
#             value = request.form.get('value')

#             black  = request.form.get('black')
#             white  = request.form.get('white')
#             red    = request.form.get('red')
#             orange = request.form.get('orange')
#             yellow = request.form.get('yellow')
#             green  = request.form.get('green')
#             blue   = request.form.get('blue')
#             purple = request.form.get('purple')

#             colorList = [black,white,red,orange,yellow,green,blue,purple]
#             valueList = [premium,value]

#             l = len(colorList)
#             for x in range(l-1,-1,-1):
#                 if colorList[x] is None:
#                     colorList.pop(x)
            
#             l = len(valueList)
#             for x in range(l-1,-1,-1):
#                 if valueList[x] is None:
#                     valueList.pop(x)

#             print(colorList)
#             print(valueList)

#             brand = 'Nike'

#             sneaker = Sneaker()

#             shoeList = sneaker.finder(int_min, int_max, brand, valueList, colorList)

#             shoeData = {}
#             for shoe in shoeList:
#                 s = Sneaker(name=shoe)
#                 shoeData[shoe] = {
#                     'value': s.avg_sale_price,
#                     'premium': s.premium
#                 }
#             print(shoeData)

#             return render_template('public/found_shoes.html', shoeList=shoeList, shoeData=shoeData)
#     else:
#         pass