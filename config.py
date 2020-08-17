import os 
from dotenv import load_dotenv
load_dotenv()


token = os.getenv("TOKEN")
host=os.getenv("HOST")
user=os.getenv("USER")
passwd=os.getenv("PASSWD")
database=os.getenv("DATABASE")
