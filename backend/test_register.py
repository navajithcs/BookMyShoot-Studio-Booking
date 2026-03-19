import requests
url='http://localhost:5000/api/register'
payload={
  'first_name':'navajith',
  'last_name':'cs',
  'email':'navajith78@gmail.com',
  'user_type':'customer',
  'password':'Password123',
  'phone':'1234567890'
}
try:
    r=requests.post(url,json=payload,timeout=10)
    print('Status',r.status_code)
    print(r.text)
except Exception as e:
    print('Error:',e)
