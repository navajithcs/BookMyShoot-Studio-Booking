import os, requests
from dotenv import load_dotenv

load_dotenv('backend/.env')
url = "https://api.razorpay.com/v1/payments/pay_SOG8Kp3vTfIsbC/refund"
response = requests.post(url, auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET')))
print('STATUS CODE:', response.status_code)
print('RESPONSE:', response.text)
