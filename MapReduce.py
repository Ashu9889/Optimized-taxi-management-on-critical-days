
import pymongo
import json
import datetime
from datetime import date
import calendar


def findDay(date):
    month, day, year = (int(i) for i in date.split('/'))
    born = datetime.date(year, month, day)
    return born.strftime("%A")


def fun1(path):
    mycol = mydb["Uber"]
   # with open(path,'r') as f:
    #   uber=json.load(f)
    #x=mycol.insert_many(uber)
    d = {}
    fl = []
    for i in mycol.find():
        if i["dispatching_base_number"] + " " + findDay(i["date"]) in d.keys():
            d[i["dispatching_base_number"] + " " + findDay(i["date"])] = d[i["dispatching_base_number"] + " " + findDay(
                i["date"])] + i["trips"]
        else:
            d[i["dispatching_base_number"] + " " + findDay(i["date"])] = i["trips"]

    for i in d:
        l = []
        l.extend(i.split(" "))
        l.append(d[i])
        fl.append(l)
    return fl


def fun2():
    mycol = mydb["Uber"]
    nd = {}
    b = []
    count_batches = 0
    for i in mycol.find():
        if i["dispatching_base_number"] not in b:
            count_batches += 1
            b.append(i["dispatching_base_number"])
        if findDay(i["date"]) in nd.keys():
            nd[findDay(i["date"])] += 1
        else:
            nd[findDay(i["date"])] = 1
    for i in nd.keys():
        nd[i] //= count_batches
    return nd


def fun3():
    mycol = mydb["Uber"]
    d = {}
    fl = []
    for i in mycol.find():
        if i["dispatching_base_number"] + " " + findDay(i["date"]) in d.keys():
            d[i["dispatching_base_number"] + " " + findDay(i["date"])] = d[i["dispatching_base_number"] + " " + findDay(
                i["date"])] + i["active_vehicles"]
        else:
            d[i["dispatching_base_number"] + " " + findDay(i["date"])] = i["active_vehicles"]
    for i in d:
        l = []
        l.extend(i.split(" "))
        l.append(d[i])
        fl.append(l)
    return fl


def event():
    mycol = mydb["Events"]
    event_list = []
    for i in mycol.find({}, {"_id": 0}):
        event_list.append(list(dict(i).values()))
    return event_list


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

if __name__ == "__main__":
    fun1("C:/Users/Ashutosh/Bigdata/Uber.json")
    fun2()
    fun3()
    event()



