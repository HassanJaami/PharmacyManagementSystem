from sqlalchemy import Column, String, Integer
from DB_Base import Base
from datetime import date

# from DB_Batch import BatchDBHndler


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    product_PPU = Column(Integer, nullable=False)
    product_vendor = Column(String(100), nullable=True)
    product_description = Column(String(1000), nullable=True)

    def __init__(self, name, ppu, vendor, descip):
        self.product_name = name
        self.product_PPU = ppu
        self.product_vendor = vendor
        self.product_description = descip


#hnd = ProductDBHndler()
# hnd.removeProduct(1)

#hnd.updateProduct('zzz', 99, '2023-8-15')
