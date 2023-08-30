from sqlalchemy import Column, String, Integer, Date, ForeignKey
from DB_Base import Base
from sqlalchemy.orm import relationship
from datetime import date

from DB_Orders import Orders


class TransactionDetail(Base):
    __tablename__ = "transactionDetail"
    transac_id = Column(Integer, primary_key=True)
    transac_amount = Column(Integer, nullable=False)

    order_id = Column(Integer, ForeignKey('orders.order_id'))
    # pharmacist_id = Column(Integer, ForeignKey('pharmacist.pharmacist_id'))

    order = relationship('Orders', backref='transactionDetail')

    # pharm = relationship('Pharmacist', backref='transactionDetail')

    def __init__(self, amount, order):
        self.transac_amount = amount
        self.order = order
        # self.pharm = phar
