import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
ClUSTER_NAME = os.getenv('ClUSTER_NAME')