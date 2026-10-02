def test_requires_auth(client):
 r=client.post('/api/generate-home',json={'budget':50000,'room_type':'Living Room','style':'Modern','items':[{'category':'Light','quantity':2}]});assert r.status_code==401
def test_home_fallback(client):
 client.post('/api/register',json={'name':'Test User','email':'test@example.com','password':'password123'})
 r=client.post('/api/generate-home',json={'budget':50000,'room_type':'Living Room','style':'Modern','items':[{'category':'Light','quantity':2}]})
 assert r.status_code==200; assert r.json()['planner_type']=='home'; assert r.json()['id']>0
