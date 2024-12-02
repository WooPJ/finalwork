import sqlite3
import json
from datetime import datetime  # datetime 삽입
from flask import Flask, render_template, request, redirect, jsonify  

app = Flask(__name__)  


@app.route('/')
def mainorder():
    return render_template('mainorder.html')

@app.route('/meals')
def meals():
    return render_template('meals.html')

@app.route('/drink')
def drink():
    return render_template('drink.html')

@app.route('/ordercol')
def ordercol():
    return render_template('ordercol.html')

@app.route('/drinkorder')
def drinkorder():
    return render_template('drinkorder.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')


#ordercol.html주문 api {post방식}
@app.route('/api/order', methods=['POST'])
def select_menu():
    menu = request.form["menu"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    totalPrice = request.form["totalPrice"]
    con = sqlite3.connect('orderData.db')
    cursor = con.cursor()
    
    order_list = (None, menu, quantity,price,totalPrice)
    cursor.execute("INSERT INTO orderList VALUES(?,?,?,?,?);", order_list)
    con.commit()
    con.close()
    return "Success"

@app.route('/order')
def order():
    con = sqlite3.connect('orderData.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM orderList")
    order_list = cursor.fetchall()
    return render_template('ordercol.html', order_list = order_list)

@app.route('/bill')
def bill():
    con = sqlite3.connect('orderData.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM orderList ORDER BY orderNum")
    order_list = cursor.fetchall()
    return render_template('bill.html', order_list = order_list)

@app.route('//api/totalSum')
def totalSum():
    totalPrice = request.form["sumPrice"]
    
    con = sqlite3.connect('orderData.db')
    cursor = con.cursor()
    cursor.execute("SELECT sum(sumPrice) AS total_sum FROM orderList")
    con.commit()
    return "계산할 총액입니다."


@app.route('/api/billremove', methods=['POST'])
def api_remove():
    remove_num = request.form["orderNum"]

    con = sqlite3.connect('orderData.db')
    cursor = con.cursor()
    query = "DELETE FROM orderList WHERE orderNum=?"
    cursor.execute(query, (remove_num,))
    con.commit()

    return "메뉴를 삭제했습니다."


@app.route('/edit/<idx>')
def edit(idx):
    conn = sqlite3.connect('postData.db')  # postdb 연결
    cursor = conn.cursor()
    query = "SELECT * FROM T_Board WHERE boardIdx = '{}'".format(idx)
    data_list = cursor.execute(query)
    data_list = cursor.fetchall()

    return render_template("blog_edit.html", title=data_list[0][1], contents=data_list[0][2], index=data_list[0][0]
                           )



if __name__ == "__main__":
    app.run(port=4005, debug=True)
