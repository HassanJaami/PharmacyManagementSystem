from sqlalchemy import Column, String, Table, Integer, Date, ForeignKey
from DB_Base import Base
from sqlalchemy.orm import relationship
from datetime import date

class OrderProduct(Base):
    __tablename__ = "orderProduct"
    orderProd_id = Column(Integer, primary_key=True)
    orderProd_qty = Column(Integer, nullable=False)

    order_id = Column(Integer, ForeignKey('orders.order_id'))
    order = relationship('Orders', backref='orderProduct')

    product_id = Column(Integer, ForeignKey('product.product_id'))
    prod = relationship('Product', backref='orderProduct')


    def __init__(self, quantity, order, prod):
        self.orderProd_qty = quantity
        self.order = order
        self.prod = prod
