# send_to_sheets.py
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

load_dotenv()

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Add your service account file
creds = ServiceAccountCredentials.from_json_keyfile_name('google-python-creds.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open_by_key(os.getenv('GOOGLE_API_KEY'))

# Get the first sheet of the Spreadsheet
worksheet = sheet.get_worksheet(0)

with open("article_content.json", "r") as f:
    carousel_output = json.load(f)

data = [
    [carousel_output["Cover_Title"], carousel_output["Cover_Subtext"], carousel_output["Slide_1_Title"], carousel_output["Slide_1_Subtext"], carousel_output["Slide_1_Type"], carousel_output["Slide_2_Title"], carousel_output["Slide_2_Subtext"], carousel_output["Slide_2_Type"], carousel_output["Slide_3_Title"], carousel_output["Slide_3_Subtext"], carousel_output["Slide_3_Type"], carousel_output["Slide_4_Title"], carousel_output["Slide_4_Subtext"], carousel_output["Slide_4_Type"], carousel_output["Slide_5_Title"], carousel_output["Slide_5_Subtext"], carousel_output["Slide_5_Type"], carousel_output["CTA_Title"], carousel_output["CTA_Subtext"]]
]
print(data)

# # Insert the data into the sheet
worksheet.append_row(data[0])

print("Data successfully written to Google Sheets.")
