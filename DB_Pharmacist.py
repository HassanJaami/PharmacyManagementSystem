from ast import If
from sqlalchemy import Column, String, Integer, Date
from DB_Base import Base
from datetime import date
import json


class Pharmacist(Base):
    __tablename__ = "pharmacist"
    pharmacist_id = Column(Integer, primary_key=True)
    pharmacist_name = Column(String(100), nullable=False)
    pharmacist_phoneNo = Column(String(20), nullable=False)
    pharmacist_userName = Column(String(100), nullable=False)
    pharmacist_password = Column(String(20), nullable=False)
    pharmacist_salary = Column(Integer, nullable=False)

    def __init__(self, name, phone, userName, password, salary):
        self.pharmacist_name = name
        self.pharmacist_phoneNo = phone
        self.pharmacist_userName = userName
        self.pharmacist_password = password
        self.pharmacist_salary = salary

# ************************************************************************************************


# hnd = PharmacistDBHndler()
# p = hnd.getAllPharmacists()
# print(p)
# json_object = json.dumps(p, indent = 4)
# print(json_object)
