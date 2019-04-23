#!/usr/bin/env python3


import os
import urllib.request
import requests

from bs4 import BeautifulSoup
from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from time  import gmtime,strftime

from ..models.model import User,ShoeBox,Sneaker,ShoeView,UserFavorites
from ..extensions.loaders import tsplit, search_terms,update_shoe,shoe_info,price_premium,shoes_like_list,get_current_date,account_pairing_scores,line_graph_labels,add_dict_total

elekid = Blueprint('private',__name__,url_prefix='/p')

@elekid.route('/adex',methods=['GET','POST'])
def adex():
    if request.method == 'GET':
        try:
            user = User({'username': session['username'], 
                        'pk': session['pk'], 'age': session['age'], 
                        'gender': session['gender']})
            sneaker        = Sneaker()
            sneaker_total  = '{:,}'.format(sneaker.get_total_sneakers())
            per_sale_value = '{:0.2f}'.format(sneaker.get_total_value()/sneaker.get_total_sales())
            nike_premium   = '{:0.2f}'.format(sneaker.get_total_premium_by_brand('nike'))
            adidas_premium = '{:0.2f}'.format(sneaker.get_total_premium_by_brand('adidas'))
            jordan_premium = '{:0.2f}'.format(sneaker.get_total_premium_by_brand('jordan'))
            other_premium  = '{:0.2f}'.format(sneaker.get_total_premium_by_brand('other'))
            return render_template('private/adex.html',
                                    sneaker_total  = sneaker_total,
                                    per_sale_value = per_sale_value,
                                    nike_premium   = nike_premium,
                                    adidas_premium = adidas_premium,
                                    jordan_premium = jordan_premium,
                                    other_premium  = other_premium )
        except KeyError:
            return redirect('/register')
    elif request.method == 'POST':
        search_terms = request.form['post_button']
        if search_terms == '': 
            return redirect(url_for('private.adex'))
        else:
            return redirect('p/search/'+search_terms)

@elekid.route('/search/<searchterms>',methods=['GET','POST'])
def search_results(searchterms):
    if request.method == 'GET':
        """ 
        ----------------------------
        SEARCH FOR KEYWORD STRENGTH
        INCLUDES ALL BRAND PARAMETER
        ----------------------------
        """
        shoe_list = search_terms(searchterms,'all')
        return render_template('private/search-result.html',
                                shoe_list   = shoe_list,
                                searchterms = searchterms)
    elif request.method == 'POST':
        return redirect('p/search/'+search_terms)
    else:
        pass

@elekid.route('/account',methods=['GET','POST'])
def account():
    if request.method == 'GET':
        try:
            """
            ~~~~~~~~~
            USER INFO
            ~~~~~~~~~
            """
            user    = User({'username': session['username'], 
                            'pk': session['pk'], 'age': session['age'], 
                            'gender': session['gender']})

            shoebox = user.display_shoebox()
            total   = len(shoebox)
            spent   = add_dict_total(shoebox, 'price_bought')
            value   = add_dict_total(shoebox, 'value')
            profit  = add_dict_total(shoebox, 'profit')

            label_list  = line_graph_labels(shoebox, 'value')
            profit_list = line_graph_labels(shoebox, 'profit')

            sneaker    = Sneaker()
            pie_brands = ['nike', 'adidas', 'jordan', 'other']
            pie_values = [0, 0, 0, 0]
            colors = ["rgba(247, 100, 152, 1)","rgba(58, 214, 222, 0.54)","rgba(251, 240, 18, 0.93)","rgba(118, 227, 189, 1)"]

            for key in shoebox.keys():
                box_brand = sneaker.get_brand(shoebox[key]['shoename'])
                for brand in pie_brands:
                    if box_brand == brand and brand == 'nike':
                        pie_values[0] += 1
                    elif box_brand == brand and brand == 'adidas':
                        pie_values[1] += 1
                    elif box_brand == brand and brand == 'jordan':
                        pie_values[2] += 1
                    elif box_brand == brand and brand == 'other':
                        pie_values[3] += 1
            

            date_label   = label_list[0]
            value_label  = label_list[1]
            profit_label = profit_list[1]
            print(date_label)

            return render_template('private/account-vk.html',
                                    shoebox = shoebox,
                                    total   = total,
                                    spent   = spent,
                                    value   = value,
                                    profit  = profit,
                                    max     = max(value_label)+10, 
                                    labels  = date_label, 
                                    values  = value_label,
                                    profits = profit_label,
                                    colors  = colors,
                                    set = zip(pie_values, pie_brands, colors) )
        except KeyError:
            return redirect('/register')
    elif request.method == 'POST':
        if request.form['post_button'].split('-')[0] == 'Update':
            box_pk   = request.form['post_button'].split('-')[1]
            box      = ShoeBox(pk=box_pk)
            shoeName = box.shoename
            return redirect('/p/update-box/'+box_pk+'/'+shoeName)
        elif request.form['post_button'].split('-')[0] == 'Remove':
            box_pk = request.form['post_button'].split('-')[1]
            box    = ShoeBox(pk=box_pk)
            box.remove(box_pk)
            return redirect('/p/account')
    else:
        pass

@elekid.route('/favorites',methods=['GET','POST'])
def favorites():
    if request.method == 'GET':
        try:
            """
            ~~~~~~~~~
            USER INFO
            ~~~~~~~~~
            """
            user    = User({'username': session['username'], 
                            'pk': session['pk'], 'age': session['age'], 
                            'gender': session['gender']})
            favList = user.display_favorites()
            like_account = account_pairing_scores(user.pk)
            pk1 = like_account[0]
            pk2 = like_account[1]
            u = User()
            recList = u.display_reccomendations(pk1,pk2)
            print(favList)
            print(recList)
            return render_template('private/favorites.html',
                                    favList = favList,
                                    recList = recList )
        except KeyError:
            return redirect('/register')
    elif request.method == 'POST':
        print(request.form.get('post_button'))
        fav = UserFavorites()
        fav.remove(request.form.get('post_button'))
        return redirect('/p/favorites')
    else:
        pass

@elekid.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('private/upload.html')
    elif request.method == 'POST':
        name = request.form['name']
        print(name)
        lower_name = name.lower().split(' ')
        print(lower_name)
        join_name = '-'.join(lower_name)
        print(join_name)
        url = 'https://stockx.com/'+str(join_name)
        print(url)
        sneaker = Sneaker()
        shoeData = scrape_new_shoe(url)
        if not sneaker.existing(shoeData['name']):
            download_sneaker_img(shoeData)
            print('DOWNLOADED IMAGE: {}'.format(shoeData['image']))
            insert_shoe_to_db(shoeData)
            print('ADDED SHOE TO DATABASE')
            return redirect('/add/success')
        else:
            return render_template('/private/upload.html', 
                                    message='Shoe Exists Homie!' )
    else:
        pass
    
@elekid.route('/id/<shoeName>',methods=['GET','POST'])
def id(shoeName):
    if request.method == 'GET':
        try:
            user = User({'username': session['username'],'pk': session['pk'],'age': session['age'],'gender': session['gender']})
            update_shoe(shoeName)
            shoeData  = Sneaker(name=shoeName)
            premium   = price_premium(shoeData.retail_price,shoeData.avg_sale_price)
            likeShoes = shoes_like_list(shoeName)
            return render_template('private/shoe_id.html',
                                    shoename  = shoeName, 
                                    shoeData  = shoeData, 
                                    premium   = premium, 
                                    likeShoes = likeShoes )
        except KeyError:
            return redirect('/')
        except AttributeError:
            shoe = ShoeView(shoename=shoeName)
            shoe.save(shoeName)
            update_shoe(shoeName)
            shoeData = Sneaker(name=shoeName)
            premium = price_premium(shoeData.retail_price,shoeData.avg_sale_price)
            likeShoes = shoes_like_list(shoeName)
            return render_template('public/shoe_id.html',
                                   shoename=shoeName, 
                                   shoeData=shoeData,
                                   premium=premium,
                                   likeShoes=likeShoes )
    elif request.method == 'POST':
        if request.form['post_button'] == 'Favorite':
            try:
                user = User({'username': session['username'], 
                             'pk': session['pk'], 'age': session['age'], 
                             'gender': session['gender']})
                shoeData = Sneaker(name=shoeName)
                user.favoriteShoe(shoeName,user.pk)
                premium = price_premium(shoeData.retail_price,shoeData.avg_sale_price)
                likeShoes = shoes_like_list(shoeName)
                return render_template('private/shoe_id.html',
                                        shoename  = shoeName, 
                                        shoeData  = shoeData,
                                        message   = 'This Sneaker Has Been Favorited!',
                                        premium   = premium, 
                                        likeShoes = likeShoes )
            except KeyError:
                return redirect('/')
        elif request.form['post_button'] == 'Add To Shoebox':
            return redirect('/p/add-buy/'+shoeName)
    else:
        pass

@elekid.route('/add-buy/<shoeName>',methods=['GET','POST'])
def add_buy(shoeName):
    if request.method == 'GET':
        try:
            user = User({'username': session['username'], 'pk': session['pk'], 
                        'age': session['age'], 'gender': session['gender']})
            return render_template('private/add_buy.html',
                                    shoeName=shoeName )
        except KeyError:
            return redirect('/')
    elif request.method == 'POST':
        if request.form['post_button'] == 'BUY':
            return ('', 204)
        elif request.form['post_button'] == 'SELL':
            return redirect('/p/add-sell/'+shoeName)
        else:
            try:
                user = User({'username': session['username'], 'pk': session['pk'], 
                        'age': session['age'], 'gender': session['gender']})
                type = 'Buy'
                price_bought = request.form['price'].strip('$')
                new_price = float(price_bought.replace(',',''))
                date = get_current_date()
                profit = 0
                user.add_to_box(type,shoeName,date,new_price,profit,user.pk)
                return redirect(url_for('private.add_success', 
                                         shoeName=shoeName, 
                                         message='added' ))
            except ValueError:
                return render_template('private/add_buy.html',
                                        shoeName = shoeName, 
                                        message  = "Enter a number." )
    else:
        pass

@elekid.route('/add-sell/<shoeName>',methods=['GET','POST'])
def add_sell(shoeName):
    if request.method == 'GET':
        try: 
            user = User({'username': session['username'], 'pk': session['pk'], 
                        'age': session['age'], 'gender': session['gender']})
            return render_template('private/add_sell.html',
                                    shoeName=shoeName )
        except KeyError:
            return redirect('/')
    elif request.method == 'POST':
        if request.form['post_button'] == 'BUY':
            return redirect('/p/add-buy/'+shoeName)
        elif request.form['post_button'] == 'SELL':
            return ('', 204)
        else:
            try:
                sneaker = Sneaker(name=shoeName)
                user = User({'username': session['username'], 'pk': session['pk'], 
                            'age': session['age'], 'gender': session['gender']})
                type = 'Sell'
                price_bought     = request.form['price_bought'].strip('$')
                new_price_bought = price_bought.replace(',','')
                new_price_bought = float(new_price_bought)
                price_sold       = request.form['price_sold'].strip('$')
                new_price_sold   = float(price_sold.replace(',',''))
                profit           = new_price_sold - new_price_bought
                date             = get_current_date()
                user.add_to_box(type,shoeName,date,new_price_bought,profit,user.pk,new_price_sold)
                return redirect(url_for('private.add_success', 
                                         shoeName=shoeName, 
                                         message="added"))
            except ValueError:
                return render_template('private/add_sell.html',
                                        shoeName = shoeName,
                                        message  = "Enter a number." )
    else:
        pass

@elekid.route('/update-box/<box_pk>/<shoeName>',methods=['GET','POST'])
def update_box(shoeName,box_pk):
    shoeName=shoeName
    if request.method == 'GET':
        user = User({'username': session['username'], 'pk': session['pk'], 
                     'age': session['age'], 'gender': session['gender']})
        return render_template('private/update-box.html', 
                                shoeName=shoeName, 
                                box_pk=box_pk )
    elif request.method == 'POST':
        try:
            box = ShoeBox(pk=box_pk)
            user = User({'username': session['username'], 'pk': session['pk'], 
                         'age': session['age'], 'gender': session['gender']})

            price_bought = request.form['price_bought'].strip('$')
            new_price_bought = price_bought.replace(',','')
            new_price_bought = float(new_price_bought)

            price_sold = request.form['price_sold'].strip('$')
            new_price_sold = float(price_sold.replace(',',''))
            type = box.type
            profit = new_price_sold - new_price_bought
            user.update_shoebox(box_pk, type, price_bought, price_sold, profit, user.pk)
            return redirect(url_for('private.add_success', 
                                     shoeName=shoeName, 
                                     message='updated' ))
        except ValueError:
            return render_template('private/add_sell.html',
                                    shoeName = shoeName, 
                                    box_pk   = box_pk,
                                    message  = "Enter a number." )
    else:
        pass

@elekid.route('<message>/<shoeName>/success',methods=['GET','POST'])
def add_success(shoeName, message):
    if request.method == 'GET':
        return render_template('private/success_add.html', 
                                shoeName=shoeName, 
                                message=message )
    elif request.method == "POST":
        pass
    else:
        pass