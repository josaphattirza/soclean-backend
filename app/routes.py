import ast
import json
from datetime import date
import datetime

from bson import json_util
from flask import render_template, request, session, jsonify
from sqlalchemy import Table

import flask_pymongo
from flask_pymongo import PyMongo

from app import app, mongo1, mongo2
from .order import Order

from bson.objectid import ObjectId

from flask_cors import CORS, cross_origin


# ERROR = TypeError: Object of type ObjectId is not JSON serializable
# parse_json is used to convert ObjectId into JSON serializable
def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route('/')
@app.route('/index')
@cross_origin()
def index():
    return render_template('base.html')


@app.route("/api/get_schedule", methods=['GET', 'POST'])
@cross_origin()
# Maybe add cross_origin here?
def get_schedule():
    # Initialize response data structure
    response = dict()
    response["schedules"] = dict()

    requestArgs = request.get_json()

    areaAddress = requestArgs["areaAddress"]
    workerAmount = requestArgs["workerAmount"]

    schedules_collection = mongo1.db.schedules

    today = date.today()
    # print(today.day)
    # print(today.month)
    # print(today)

    all_schedules = schedules_collection.find()
    for schedule in all_schedules:
        array = []
        i = 9
        for available_worker_in_hour in schedule["availableWorkers"][areaAddress]:
            # print(available_worker_in_hour)
            if len(available_worker_in_hour) >= int(workerAmount):
                array.append(i)
            i += 1

        if len(array) > 0:
            response["schedules"][schedule["date"]] = array

    return response


@app.route("/api/use_schedule", methods=['GET', 'POST'])
@cross_origin()
# Maybe add cross_origin here?
def use_schedule():
    # Initialize response data structure
    response = dict()
    response["workerIds"] = []

    requestArgs = request.get_json()

    areaAddress = requestArgs["areaAddress"]
    workersAmount = requestArgs["workersAmount"]
    request_date = requestArgs["date"]
    startingHour = requestArgs["startingHour"]
    endingHour = requestArgs["endingHour"]

    schedules_collection = mongo1.db.schedules

    chosen_schedule = schedules_collection.find_one({"date":request_date})
    for _ in range(workersAmount):
        for i in range(int(startingHour-9), int(endingHour-9)+1):

            popped_id = chosen_schedule["availableWorkers"][areaAddress][i].pop()
            new_array = chosen_schedule["availableWorkers"][areaAddress][i]
            edited_string = "availableWorkers"+"."+areaAddress+"."+str(i)
            schedules_collection.update_one({
                "date":request_date},
                {
                    "$set":{
                        edited_string : new_array
                    }
                }
            )

        print(popped_id)
        response["workerIds"].append(parse_json(popped_id))

    return response


@app.route("/api/update_schedule", methods=['GET', 'POST'])
@cross_origin()
# Maybe add cross_origin here?
def update_schedule():
    schedules_collection = mongo1.db.schedules

    today = date.today()
    # print(today.day)
    # print(today.month)
    # print(today)

    for _ in range(30):
        print(today.strftime("%Y/%m/%d"))
        repeatable_check = schedules_collection.find({"date": today.strftime("%Y/%m/%d")})
        if repeatable_check.count() != 0:
            today += datetime.timedelta(days=1)
            continue

        document = dict()

        today_available_workers = dict()
        today_available_workers["Beitou"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Daan"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Datong"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Nangang"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Neihu"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Shilin"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Songshan"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Wanhua"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Wenshan"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Xinyi"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Zhongshan"] = [[], [], [], [], [], [], [], [], [], [], [], []]
        today_available_workers["Zhongzheng"] = [[], [], [], [], [], [], [], [], [], [], [], []]

        # Name of collection -> workers
        data = mongo1.db.workers.find()
        # print(type(data))
        # print(data.count())
        for x in data:
            # print(x["availableHour"])
            # print(x["areaAddress"])
            worker_availableHour = x["availableHour"][today.strftime("%A").lower()]
            # print(worker_availableHour)
            worker_areaAddress = x["areaAddress"]

            for hour in worker_availableHour:
                today_available_workers[worker_areaAddress][hour - 9].append(x["_id"])
                print(today_available_workers)

        # print(today_available_workers)
        document["date"] = today.strftime("%Y/%m/%d")
        document["availableWorkers"] = today_available_workers
        # print(document)

        schedules_collection.insert(document)
        today += datetime.timedelta(days=1)

        # document["_id"] = parse_json(document["_id"])
        # response["schedules"].append(document)

    return "schedules updated"


@app.route("/api/delete_all_schedules", methods=['GET', 'POST'])
@cross_origin()
# maybe add cross_origin here?
def delete_all_schedules():
    schedules_collection = mongo1.db.schedules

    x = schedules_collection.delete_many({})

    return "all schedules deleted"


@app.route("/api/add_order", methods=['GET', 'POST'])
@cross_origin()
# maybe add cross_origin here?
def add_order():
    with app.app_context():
        rq = request.get_json()

        customer_id = rq["customerId"]
        customer_name = rq["customerName"]
        workers_amount = rq["workersAmount"]
        price = rq["price"]
        date = rq["date"]
        shift = rq["shift"]
        customer_phone = rq["customerPhone"]
        customer_email = rq["customerEmail"]
        address = rq["address"]
        area = rq["area"]
        payment_method = rq["paymentMethod"]
        manhour = rq["manhour"]
        workerIds = rq["workerIds"]
        order_status = "unfinished"

        o = Order(customerId=customer_id, customer_name=customer_name,
                  address=address, area=area, workers_amount=workers_amount, price=price,
                  payment_method=payment_method, date=date, shift=shift,
                  customer_phone=customer_phone, customer_email=customer_email,
                  manhour=manhour, workerIds=workerIds, order_status=order_status)

        # toString
        text_to_show = str(o)

        orders = mongo1.db.orders

        # Inserting order into the database
        # REMEMBER THAT this function directly adds the _id into the dictionary
        # therefore the _id (an ObjectId) must be made serializable using parse_json(_id)
        orders.insert(o.__dict__)

        o.__dict__["_id"] = parse_json(o.__dict__["_id"])

        # json to basically respond with __str__ of the class
        response = jsonify(o.__dict__)

    return response


# Query an order using its _id
@app.route("/api/get_order", methods=['GET', 'POST'])
@cross_origin()
# maybe add cross_origin here?
def get_order():
    # data = name of collection
    order_id = request.get_json()

    id = order_id["orderId"]

    order_id = ObjectId(id)

    requested_order = mongo1.db.orders.find_one({"_id": order_id})

    requested_order["_id"] = parse_json(requested_order["_id"])

    response = requested_order

    return response


# Return all attributes related to ordered workers, except their password and availableHours
@app.route("/api/get_worker", methods=['GET', 'POST'])
@cross_origin()
# Maybe add cross_origin here?
def get_worker():
    # # Sample of request array
    # {
    #     "workerIds": [
    #         "606da19602df7f0199993d80",
    #         "60965d295705288eb363eebf",
    #         "609660c15705288eb363eec0"
    #     ]
    # }

    # Initialize response data structures
    response = dict()
    response["workers"] = []
    worker_data = []

    with app.app_context():
        worker_ids = request.get_json()

        workers = worker_ids["workerIds"]

        for id in workers:
            # Convert worker_id to an ObjectId for query
            worker_id = ObjectId(id)

            # Name of collection -> workers
            data = mongo1.db.workers.find_one({"_id": worker_id})

            # Return all attributes related to ordered workers, except their password and availableHours
            worker_data.append(
                # Pymongo provides json_util - you can use that one instead to handle BSON types
                # because _id is an ObjectId
                {"_id": parse_json(data["_id"]),
                 "name": data["name"],
                 "areaAddress": data["areaAddress"],
                 "email": data["email"],
                 "phoneNumber": data["phoneNumber"]
                 }
            )

        # Insert worker_data array into response JSON
        response["workers"] = worker_data
        response = jsonify(response)

    return response


# Query all unfinished orders related to a workerId
@app.route("/api/worker/get_unfinished_order", methods=['GET', 'POST'])
@cross_origin()
# maybe add cross_origin here?
def worker_get_unfinished_order():
    # # Sample of request array
    # {
    #     "workerId": "606da19602df7f0199993d80"
    # }

    # Initialize response data structures
    response = dict()
    response["orders"] = []
    orders_data = []

    with app.app_context():
        request_params = request.get_json()

        worker_id = request_params["workerId"]

        # Name of collection -> workers
        datas = mongo1.db.orders.find({"workerIds": worker_id, "order_status": "unfinished"})

        for data in datas:

            # Return all unfinished orders related to a workerId
            orders_data.append(
                # Pymongo provides json_util - you can use that one instead to handle BSON types
                # because _id is an ObjectId
                {"_id": parse_json(data["_id"]),
                 "customer_name": data["customer_name"],
                 "customer_phone": data["customer_phone"],
                 "customer_email": data["customer_email"],
                 "address": data["address"],
                 "area": data["area"],
                 "payment_method": data["address"],
                 "shift": data["payment_method"],
                 "date": data["date"],
                 "order_status": data["order_status"]
                 }
            )

        # Insert order_data array into response JSON
        response["orders"] = orders_data
        response = jsonify(response)

    return response


# Query all finished orders related to a workerId
@app.route("/api/worker/get_finished_order", methods=['GET', 'POST'])
@cross_origin()
# maybe add cross_origin here?
def worker_get_finished_order():
    # # Sample of request array
    # {
    #     "workerId": "606da19602df7f0199993d80"
    # }

    # Initialize response data structures
    response = dict()
    response["orders"] = []
    orders_data = []

    with app.app_context():
        request_params = request.get_json()

        worker_id = request_params["workerId"]

        # Name of collection -> workers
        datas = mongo1.db.orders.find({"workerIds": worker_id, "order_status": "finished"})

        for data in datas:

            # Return all finished orders related to a workerId
            orders_data.append(
                # Pymongo provides json_util - you can use that one instead to handle BSON types
                # because _id is an ObjectId
                {"_id": parse_json(data["_id"]),
                 "customer_name": data["customer_name"],
                 "customer_phone": data["customer_phone"],
                 "customer_email": data["customer_email"],
                 "address": data["address"],
                 "area": data["area"],
                 "payment_method": data["address"],
                 "shift": data["payment_method"],
                 "date": data["date"],
                 "order_status": data["order_status"]
                 }
            )

        # Insert order_data array into response JSON
        response["orders"] = orders_data
        response = jsonify(response)

    return response
