import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google API 密钥 JSON 文件的路径
json_keyfile = '/home/pi/final/avian-current-389606-0a47da6fc795.json'

# 授权范围
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# 从 JSON 文件创建凭据
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

# 使用凭据授权并打开 Google 表单
client = gspread.authorize(credentials)
sheet = client.open('Test').sheet1
