from sqlalchemy import Column, Integer, Date, ForeignKey
from DB_Base import Base
from sqlalchemy.orm import relationship
from datetime import date


class Batch(Base):
    __tablename__ = "batch"
    batch_no = Column(Integer, nullable=False, primary_key=True)
    batch_quantity = Column(Integer, nullable=False)
    batch_expiry = Column(Date, nullable=False)

    product_id = Column(Integer, ForeignKey(
        'product.product_id'), primary_key=True)

    prod = relationship('Product', backref='batch')

    def __init__(self, batchNo, batchQuant, batchExp, prod):
        self.batch_no = batchNo
        self.batch_quantity = batchQuant
        self.batch_expiry = batchExp
        self.prod = prod


# How to construct Batch table:

# print(p)

# ph.__del__()

# hnd = BatchDBHndler()
# hnd.addBatch(1, 1000, '2023-08-15', p)
