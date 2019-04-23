#!/usr/bin/env python3


import os
import time
import sqlite3
import cv2
import tensorflow as tf

from flask import Flask, render_template, request, url_for, redirect, session
from datetime import datetime
from werkzeug.utils import secure_filename

from .controllers.public  import elekid as public_buzz
from .controllers.private import elekid as private_buzz
from .models.model import User,ShoeView,Sneaker,ShoeRec
from .extensions.loaders import display_rand_shoes,date_to_unix,brander,shoeValues,search_terms,color_list

UPLOAD_FOLDER = '/Users/ahn.ch/Projects/shoe_data/run/src/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
CATEGORIES = ['adidas', 'jordan', 'nike']

electabuzz = Flask(__name__)

electabuzz.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
electabuzz.secret_key = 'SUPER-DUPER-SECRET'

electabuzz.register_blueprint(public_buzz)
electabuzz.register_blueprint(private_buzz)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare(filepath):
    IMG_SIZE = 80
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def get_current_date():
    ts = time.time() 
    new_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    date = new_time.split(' ')[0]
    return date

def ages():
    age = []
    for x in range(18,80):
        age.append(x)
    return age

def disp_nums():
    nums = ['All',24,48,96,192,384]
    return nums

@electabuzz.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        #FIXME if logged in already go to adex
        return render_template('public/index-vk.html')
    elif request.method == 'POST':
        if request.form['post_button'] == 'Login':
            """ 
            --------------------
                    LOGIN
            --------------------
            """
            try:
                with User(username=request.form['username'],password=request.form['password']) as un:
                    if un.login(request.form['password']):
                        session['username'] = un.username
                        session['pk']       = un.pk
                        session['age']      = un.age
                        session['gender']   = un.gender
                        return redirect('p/adex')
                    else:
                        return redirect('/',message='Username/Password not recognized...try again!')
            except TypeError:
                return render_template('public/index-vk.html',message="Are you sure that's correct?")
        else:
            search_terms = request.form['post_button']
            return redirect('/search/'+search_terms)
    else:
        pass

@electabuzz.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect('/')
    elif request.method == 'POST':
        pass
    else:
        pass

@electabuzz.route('/nike',methods=['GET','POST'])
def nike():
    brand = 'nike'
    if request.method == 'GET':
        sneaker      = Sneaker()
        shoe_list    = display_rand_shoes(brand,27)
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        return render_template('public/brand.html',
                                display_nums=display_nums,
                                shoe_list=shoe_list, 
                                type_list=type_list,
                                brand=brand)
    elif request.method == 'POST':
        sneaker      = Sneaker()
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        black        = request.form.get('black')
        white        = request.form.get('white')
        red          = request.form.get('red')
        orange       = request.form.get('orange')
        yellow       = request.form.get('yellow')
        green        = request.form.get('green')
        blue         = request.form.get('blue')
        purple       = request.form.get('purple')
        colorList    = [black,white,red,orange,yellow,green,blue,purple]
        l = len(colorList)
        for x in range(l-1,-1,-1):
            if colorList[x] is None:
                colorList.pop(x)
        try:
            num = request.form['num']
        except KeyError:
            num = '24'
        try:
            _type = request.form['type']
        except KeyError:
            _type = 'None'

        print([num,_type])
        if request.form['post_button'] == 'Value':
            value = 'Value'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Sales':
            value = 'Sales'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Premium':
            value = 'Premium'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Shuffle':
            return redirect('/nike')
        else:
            pass 
    else:
        pass

@electabuzz.route('/adidas',methods=['GET','POST'])
def adidas():
    brand = 'adidas'
    if request.method == 'GET':
        sneaker      = Sneaker()
        shoe_list    = display_rand_shoes(brand,26)
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        return render_template('public/brand.html',
                                display_nums=display_nums,
                                shoe_list=shoe_list, 
                                type_list=type_list,
                                brand=brand)
    elif request.method == 'POST':
        sneaker      = Sneaker()
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        black        = request.form.get('black')
        white        = request.form.get('white')
        red          = request.form.get('red')
        orange       = request.form.get('orange')
        yellow       = request.form.get('yellow')
        green        = request.form.get('green')
        blue         = request.form.get('blue')
        purple       = request.form.get('purple')
        colorList    = [black,white,red,orange,yellow,green,blue,purple]
        l = len(colorList)
        for x in range(l-1,-1,-1):
            if colorList[x] is None:
                colorList.pop(x)
        try:
            num = request.form['num']
        except KeyError:
            num = '24'
        try:
            _type = request.form['type']
        except KeyError:
            _type = 'None'
        if request.form['post_button'] == 'Value':
            value = 'Value'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Sales':
            value = 'Sales'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Premium':
            value = 'Premium'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Shuffle':
            return redirect('/adidas')
        else:
            pass 
    else:
        pass

@electabuzz.route('/jordan',methods=['GET','POST'])
def jordan():
    brand = 'jordan'
    if request.method == 'GET':
        sneaker      = Sneaker()
        shoe_list    = display_rand_shoes(brand,27)
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        return render_template('public/brand.html',
                                display_nums=display_nums,
                                shoe_list=shoe_list, 
                                type_list=type_list,
                                brand=brand)
    elif request.method == 'POST':
        sneaker      = Sneaker()
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        black        = request.form.get('black')
        white        = request.form.get('white')
        red          = request.form.get('red')
        orange       = request.form.get('orange')
        yellow       = request.form.get('yellow')
        green        = request.form.get('green')
        blue         = request.form.get('blue')
        purple       = request.form.get('purple')
        colorList    = [black,white,red,orange,yellow,green,blue,purple]
        l = len(colorList)
        for x in range(l-1,-1,-1):
            if colorList[x] is None:
                colorList.pop(x)
        try:
            num = request.form['num']
        except KeyError:
            num = '24'
        try:
            _type = request.form['type']
        except KeyError:
            _type = 'None'
        if request.form['post_button'] == 'Value':
            value = 'Value'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Sales':
            value = 'Sales'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Premium':
            value = 'Premium'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Shuffle':
            return redirect('/jordan')
        else:
            pass 
    else:
        pass

@electabuzz.route('/other',methods=['GET','POST'])
def other():
    brand = 'other'
    if request.method == 'GET':
        sneaker      = Sneaker()
        shoe_list    = display_rand_shoes(brand,24)
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        return render_template('public/brand.html',
                                display_nums=display_nums,
                                shoe_list=shoe_list, 
                                type_list=type_list,
                                brand=brand)
    elif request.method == 'POST':
        sneaker      = Sneaker()
        display_nums = disp_nums()
        type_list    = sneaker.get_types(brand)
        black        = request.form.get('black')
        white        = request.form.get('white')
        red          = request.form.get('red')
        orange       = request.form.get('orange')
        yellow       = request.form.get('yellow')
        green        = request.form.get('green')
        blue         = request.form.get('blue')
        purple       = request.form.get('purple')
        colorList    = [black,white,red,orange,yellow,green,blue,purple]
        l = len(colorList)
        for x in range(l-1,-1,-1):
            if colorList[x] is None:
                colorList.pop(x)
        try:
            num = request.form['num']
        except KeyError:
            num = '24'
        try:
            _type = request.form['type']
        except KeyError:
            _type = 'None'
        if request.form['post_button'] == 'Value':
            value = 'Value'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Sales':
            value = 'Sales'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Premium':
            value = 'Premium'
            shoe_list = sneaker.filter_by(brand, _type, value, num, colorlist=colorList)
            return render_template('public/brand.html',
                                    display_nums=display_nums,
                                    shoe_list=shoe_list,
                                    type_list=type_list,
                                    brand=brand)
        elif request.form['post_button'] == 'Shuffle':
            return redirect('/other')
        else:
            pass 
    else:
        pass

@electabuzz.route('/register',methods=['GET','POST'])
def register():
    age_list = ages()
    if request.method == 'GET':
        return render_template('public/register-vk.html',age_list=age_list)
    elif request.method == 'POST':
        with User(username=request.form['username'],password=request.form['password']) as un:
            """ 
            -----------------------
            REGISTRATION CONDITIONS
            1. Username Exists
            2. Matching Passwords
            3. Unchecked Gender/State/Age
            -----------------------
            """
            if un.check_un(request.form['username']):
                return render_template('public/register-vk.html', 
                                        age_list = age_list, 
                                        message  ='Username Exists')
            elif request.form['password'] != request.form['conf_password']:
                age_list = ages()
                return render_template('public/register.html',
                                        age_list = age_list, 
                                        message  = "Password's Do Not Match")
            elif request.form['gender'] == None:
                age_list = ages()
                return render_template('public/register.html', 
                                        age_list = age_list,  
                                        message  = "Select Gender")
                """ 
                -------------------
                ONCE MET, REGISTER
                -------------------
                """ 
            else:
                age_list = ages()
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                session['age']      = request.form['age']
                session['email']    = request.form['email']
                session['state']    = request.form['state']
                session['gender']   = request.form['gender']
                return redirect('/'+username+'/pref')       
    else:
        pass

@electabuzz.route('/<username>/pref',methods=['GET','POST'])
def user_preferences(username):
    user = User({'username': username})
    if request.method == 'GET':
        message = 'Pick your preferences.'
        return render_template('public/preferences-vk.html', username=user.username)
    elif request.method == 'POST':

        """ 
        -------------------
        RETURN BRAND VALUES
        -------------------
        """

        nike   = request.form.get('nike')
        adidas = request.form.get('adidas')
        jordan = request.form.get('jordan')
        other  = request.form.get('other')
        userBrandList = [nike,adidas,jordan,other]

        """ 
        ----------------------------
        POP NONETYPE FROM BRAND LIST
        ----------------------------
        """

        l = len(userBrandList)
        for x in range(l-1,-1,-1):
            if userBrandList[x] is None:
                userBrandList.pop(x)

        """ 
        -------------------
        RETURN COLOR VALUES
        -------------------
        """

        black  = request.form.get('black')
        white  = request.form.get('white')
        red    = request.form.get('red')
        orange = request.form.get('orange')
        yellow = request.form.get('yellow')
        green  = request.form.get('green')
        blue   = request.form.get('blue')
        purple = request.form.get('purple')
        userColorList = [black,white,red,orange,yellow,green,blue,purple]

        """ 
        ----------------------------
        POP NONETYPE FROM COLOR LIST
        ----------------------------
        """

        l = len(userColorList)
        for x in range(l-1,-1,-1):
            if userColorList[x] is None:
                userColorList.pop(x)

        userBrands = '-'.join(userBrandList)
        userColors = '-'.join(userColorList)
        userPK     = user.get_pk(user.username)

        """ 
        -----------------------------
        INSERT TO USER_PREFERENCES DB
                     ex.
             'nke-ads-jrd-otb'
         'red-blue-green-white-black'
        -----------------------------
        """
        #Create User
        user.insert_preferences( userBrands,
                                 userColors,
                                 userPK )
        user.create_user( session['username'],
                          session['password'],
                          session['age'],
                          session['gender'], 
                          session['email'],
                          session['state'] )
         
        return redirect('/'+user.username+'/success') 
    else:
        pass

@electabuzz.route('/<username>/success',methods=['GET','POST'])
def user_success(username):
    if request.method == 'GET':
        return render_template('public/success.html')
    elif request.method == "POST":
        pass
    else:
        pass

@electabuzz.route('/chartzard',methods=['GET','POST'])
def data_visualization():
    if request.method == 'GET':
        """ 
        -------------------------------
        DATA VISUALIZATIONS FROM PLOTLY
        -------------------------------
        """
        return render_template('public/chart.html')
    elif request.method == "POST":
        pass
    else:
        pass

@electabuzz.route('/finder',methods=['GET','POST'])
def finder():
    user = User({'username': session['username']})
    brand_list = ['nike','adidas','jordan','Other']
    type_list = ['Premium','Value']
    color_list = ['Black','White','Red','Orange','Yellow','Green','Blue','Purple']
    if request.method == 'GET':
        return render_template('private/finder.html',
                                brand_list=brand_list,
                                type_list=type_list,
                                color_list=color_list)
    elif request.method == "POST":
        price_min = request.form['min'].strip('$')
        price_max = request.form['max'].strip('$')

        int_min = int(price_min)
        int_max = int(price_max)

        try: 
            brand = request.form['brand']
        except KeyError:
            brand = 'None'
        try:
            _type = request.form['type']
        except KeyError:
            _type = 'None'
        try:
            color = request.form['color']
        except KeyError:
            color = 'None'

        session['brand'] = brand
        session['_type'] = _type
        session['color'] = color
        session['price_min'] = int_min
        session['price_max'] = int_max
        
        if (   brand == 'None'
            or _type == 'None'
            or color == 'None' ):
            message = 'Fill out filters.'
            return render_template('private/finder.html',
                                    brand_list = brand_list,
                                    type_list  = type_list,
                                    color_list = color_list,
                                    message    = message)
        else:
            return redirect('/find-res')
        
    else:
        pass

@electabuzz.route('/find-res',methods=['GET','POST'])
def finder_results():
    user = User({'username': session['username'],'pk': session['pk']})
    if request.method == 'GET':
        int_min = session.get('price_min', None)
        int_max = session.get('price_max', None)
        brand   = session.get('brand', None)
        color   = session.get('color', None)
        _type   = session.get('_type', None)
        no_list = user.get_dislikes(user.get_pk(user.username))
        print("User Dislike List:")
        print(no_list)
        sneaker = Sneaker()
        print(brand)
        shoe_list = sneaker.finder(int_min, int_max, brand, _type, color)
        shoeData = {}
        for shoe in shoe_list:
            s = Sneaker(name=shoe)
            shoeData[shoe] = {
                'value': s.avg_sale_price,
                'premium': s.premium
            }
        for name in no_list:
            if name in shoe_list:
                shoe_list.remove(name)
        return render_template('private/found_shoes.html', shoe_list=shoe_list[:16], shoeData=shoeData)
    elif request.method == 'POST':
        if request.form['post_button'] == 'Return':
            return redirect('/finder')
        else:
            check = request.form.get('post_button').split('~')[0]
            shoe  = request.form.get('post_button').split('~')[1]
            if check == 'dislike':
                rec          = ShoeRec()
                rec.shoename = shoe
                rec.result   = 'NO'
                rec.user_pk  = user.get_pk(user.username)
                rec.save()
                return redirect('/find-res')
            elif check == 'like':
                rec          = ShoeRec()
                rec.shoename = shoe
                rec.result   = 'YES'
                rec.user_pk  = user.get_pk(user.username)
                rec.save()
                user.favoriteShoe(shoe,user.pk)
                return redirect('/find-res')

@electabuzz.errorhandler(404)
def not_found(error):
    return render_template('public/404.html')
