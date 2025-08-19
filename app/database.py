from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL ='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Gulam%40123@localhost/fastapi data"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
# get conn/session to db and we are able to send session and then call end
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()    


Base = declarative_base()



#we are not using the below we're using alchemy for this
# while True:

#   try:
#     # hardcoding DB info here is a big problem 
#     conn = psycopg2.connect(host= 'localhost', database = 'fastapi data',
#                              user = 'postgres', password = 'Gulam@***', cursor_factory= RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was successful")
#     break  # exits from the infinite loop 

#   except Exception as error:
#     print("connection to Database failed")
#     print("Error: ", error)
#     time.sleep(3)
