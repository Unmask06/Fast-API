# import pandas as pd
# from io import BytesIO

# # Replace with the path to your local Excel file
# excel_file_path = r"C:\Users\IDM252577\Desktop\TimeSheet.xlsx"

# # Read the Excel file into a BytesIO object
# with open(excel_file_path, 'rb') as file:
#     excel_bytes = BytesIO(file.read())

# # Read the BytesIO object into a DataFrame
# df = pd.read_excel(excel_bytes)

# # Now you have your data in a DataFrame (df)
# print(df)

import base64
import pandas as pd
from io import BytesIO

filepath = r"dataurl.txt"
# Replace 'data_url' with your actual data URL obtained from JavaScript
with open(filepath, 'r') as file:
    data_url = file.read()

# Extract the Base64-encoded data from the data URL
data_index = data_url.find(",") + 1
base64_data = data_url[data_index:]

# Decode the Base64 data
binary_data = base64.b64decode(base64_data)

# Create a BytesIO object and write the binary data to it
excel_io = BytesIO(binary_data)

# Read the Excel data into a DataFrame using pandas
df = pd.read_excel(excel_io)

# Now 'df' contains your data as a DataFrame
