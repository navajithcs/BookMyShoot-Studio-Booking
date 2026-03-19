import requests, json

# Check photographers
r = requests.get('http://localhost:5000/api/photographers')
d = r.json()
print("=== Photographers ===")
for p in d.get('photographers', []):
    print(f"  ID: {p['id']}, Keys: {list(p.keys())}")

# Check pending requests for each photographer
for p in d.get('photographers', []):
    pid = p['id']
    r2 = requests.get(f'http://localhost:5000/api/bookings/requests/photographer/{pid}')
    d2 = r2.json()
    count = len(d2.get('bookings', []))
    pname = p.get('user', {}).get('first_name', 'Unknown')
    print(f"\n  Photographer {pid} ({pname}, specialty={p.get('specialty','N/A')}) - Pending requests: {count}")
    for b in d2.get('bookings', []):
        cust = b.get('customer', {})
        cname = f"{cust.get('first_name','')} {cust.get('last_name','')}" if cust else f"Customer #{b.get('customer_id')}"
        print(f"    Booking {b['id']}: {cname} - {b['service_type']} on {b['event_date']} - ₹{b.get('total_price',0)}")

# Check all pending bookings
r3 = requests.get('http://localhost:5000/api/bookings/requests')
d3 = r3.json()
print(f"\n=== All Pending Bookings: {len(d3.get('bookings',[]))} ===")
for b in d3.get('bookings', []):
    print(f"  ID:{b['id']} service:{b['service_type']} photographer_id:{b.get('photographer_id')}")
