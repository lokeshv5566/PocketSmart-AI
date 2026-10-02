def test_auth(client):
 r=client.post('/api/register',json={'name':'Test User','email':'test@example.com','password':'password123'});assert r.status_code==200
 r=client.post('/api/login',json={'email':'test@example.com','password':'password123'});assert r.status_code==200
 assert client.cookies.get('access_token')
def test_bad_login(client):
 client.post('/api/register',json={'name':'Test User','email':'test@example.com','password':'password123'})
 assert client.post('/api/login',json={'email':'test@example.com','password':'wrongpassword'}).status_code==401
