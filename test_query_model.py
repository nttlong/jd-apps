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

cnn =  pymongo.mongo_client.MongoClient(
    host="localhost",
    port=27017
)
db=cnn.get_database(("test_001"))

employees= Employees()
employees<<db # Set database
try:
    ret = employees.insert_one(
        employees.Code=="Emp010",
        employees.FirstName=="JSON",
        employees.LastName=="Julia",
        employees.BirtDate ==datetime.datetime(1927,1,1)
    )

    ret = employees.update_many(
        employees.Code=="Emp010",
        employees.set(
            employees.Code=="Emp100",
            employees.LastName=="XXX",
            employees.FirstName=="YYY",

        )
    )
except ReCompact.dbm.db_actions.Error as e:
    print(e.error_type)
employees.delete_many(employees.Code=="Emp001")
data = list(employees.find(employees.Code=="Emp001"))
txt = json.dumps(data)
print(data)