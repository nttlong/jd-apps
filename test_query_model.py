import datetime
import json

import ReCompact.dbm
import pymongo.mongo_client
import bson
@ReCompact.dbm.table(
    table_name="Employees",
    index=["Name"],
    keys=["Code"]
)
class Employees:
    Id = ReCompact.dbm.field(data_type=bson.ObjectId)
    Code= ReCompact.dbm.field(data_type=str,is_require=True)
    FirstName = ReCompact.dbm.field(data_type=str,is_require=True)
    LastName = ReCompact.dbm.field(data_type=str, is_require=True)
    BirtDate = ReCompact.dbm.field(data_type=datetime.datetime,is_require=True)
    STT = ReCompact.dbm.field(data_type=int, is_require=True)
employees= Employees()
# emp_code =employees.Code
# expx =  emp_code!=1
# expx2 = employees.FirstName!="123"
filter_b = employees.BirtDate
filter_b=filter_b==datetime.datetime.now()
# expx3 =expx2 & expx
print(filter_b)

cnn =  pymongo.mongo_client.MongoClient(
    host="192.168.18.36",
    port=27018
)

db=cnn.get_database(("test_001"))
employees<<db # Set database
try:
    ret =employees.find_one(filter_b)
    print("OK")
    print(ret)
except Exception as ex:
    print(ex)
#
# employees= Employees()
# employees<<db # Set database
# for i in range(0,1000):
#     try:
#         ret = employees.insert_one(
#             employees.Code==f"Emp{i}",
#             employees.FirstName==f"Emp{i}",
#             employees.LastName==f"Emp{i}",
#             employees.BirtDate ==datetime.datetime(1927,1,1),
#             employees.STT==i
#         )
#
#         ret = employees.update_many(
#             employees.Code=="Emp010",
#             employees.set(
#                 employees.Code=="Emp100",
#                 employees.LastName=="XXX",
#                 employees.FirstName=="YYY",
#
#             )
#         )
#     except ReCompact.dbm.db_actions.Error as e:
#         print(e.error_type)
# a= employees.FirstName!="Julia"
# b = employees.Code=="Emp002"
# fx = a & b
# arr = employees.aggregate.match(
#     fx
# )
# data = list(employees.find(fx))
#
# txt = json.dumps(data)
# print(data)