import requests

print('Fetching bookings...')
r = requests.get('http://127.0.0.1:5000/api/bookings/photographer/1')
if r.status_code == 200:
    bookings = r.json().get('bookings', [])
    pending = [b for b in bookings if b.get('status') == 'pending']
    if pending:
        b = pending[0]
        print(f'Decline booking ID {b["id"]}...')
        put_res = requests.put(f'http://127.0.0.1:5000/api/bookings/{b["id"]}/status', json={'status': 'declined', 'photographer_id': 1})
        print(f'Status: {put_res.status_code}')
        print(put_res.text[:200])
    else:
        print('No pending bookings.')
else:
    print('Failed:', r.status_code)
