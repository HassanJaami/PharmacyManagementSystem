from sqlalchemy import Column, String, Integer, Date
from DB_Base import Base


class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True)
    admin_name = Column(String(100), nullable=False)
    admin_userName = Column(String(100), nullable=False)
    admin_password = Column(String(20), nullable=False)

    def __init__(self, name, userName, password):
        self.admin_name = name
        self.admin_userName = userName
        self.admin_password = password

# ************************************************************************************************
