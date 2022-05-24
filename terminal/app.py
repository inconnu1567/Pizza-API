import string
import traceback

from flask import Flask, request, render_template, make_response
import uuid
from datetime import datetime, timedelta
from flask import session
from flask import g

import json
app=Flask(__name__)
order_id=range(1,100)
index=0

@app.route("/pizza", methods=["GET"])
def get_all_pizzas():
    file=open(r"C:\Users\Lenovo\IdeaProjects\Pizza API\Pizzas.json")
    data=json.load(file)
    file.close()
    return data

#http://127.0.0.1:5000/order?pizzas=[1,2,2,4]
@app.route("/order", methods=["POST"])
def submit_new_order():

    INVALID_MESSAGE="The format of the object is not valid"

    try:
        webreq = request.get_json()
        pizzas = webreq["pizza"]
        takeaway = webreq["takeaway"]
        payment_type = webreq["payment_type"]
        customer_id = webreq["customer_id"]
        note = webreq["note"]
        delivery_adress = webreq["delivery_address"]
        now=datetime.now()
        deliverytime = now + timedelta(minutes=20)

        file=open(r"C:\Users\Lenovo\IdeaProjects\Pizza API\Pizzas.json")
        pizzadata = json.load(file)
        pizzalist = []


        for id in pizzas:
            for pizza in pizzadata["pizza"]:
                if id == pizza["pizza_id"]:
                    pizzalist.append(pizza)



        jsonfile= {"order":
                             {"order_id": order_id[index],
                              "customer_id": customer_id,
                              "status": "In progress",
                              "ordered_at": now,
                              "note": note, "takeaway": takeaway, "payment_type": payment_type,
                              "delivery_adress": delivery_adress,
                              "pizzas": pizzalist},
                   "ordered_at": now,
                   "delivery_time" : deliverytime}

        file.close()
        return make_response(jsonfile,200)

    except:
        traceback.print_exc()
        return make_response({"message":INVALID_MESSAGE}, 400)



@app.route("/order/<order_id>", methods=["GET"])
def get_order_by_id(order_id:int):
    file=open(r"C:\Users\Lenovo\IdeaProjects\Pizza API\OrderExample.json")
    orderData = json.load(file)
    NOT_FOUND="Order_id not found"
    INVALID_ID="Invalid ID supplied"
    file.close()

    try:
        for order in orderData["order"]:
            if (int(order_id) == int(order["order_id"])):
                return make_response(order,200)
        return make_response({"message":NOT_FOUND}, 404)
    except:
        return make_response({"message":INVALID_ID},400)


def main():
    get_all_pizzas()

if __name__ == "__main__":
    main()

