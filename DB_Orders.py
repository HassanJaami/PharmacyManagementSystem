from sqlalchemy import Column, String, Integer, Date
from DB_Base import Base
from datetime import date


class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date, nullable=False)
    customer_name = Column(String(40), nullable=True)

    def __init__(self, customerName):
        self.order_date = date.today()
        self.customer_name = customerName
