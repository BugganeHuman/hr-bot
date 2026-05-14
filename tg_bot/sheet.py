import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os


load_dotenv()
base_path = os.path.dirname(os.path.abspath(__file__))

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

path_to_creds = os.path.join(base_path, "..", "creds.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_creds, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv('SHEET_ID')).sheet1