from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONNECTION_URL

engine = create_engine(CONNECTION_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def startSession():
    try:
        # Session.close_all()
        Base.metadata.create_all(engine)
        session = Session()
    except Exception as e:
        print(str(e))
    else:
        return session
