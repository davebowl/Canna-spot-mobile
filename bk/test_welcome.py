from app import app

client = app.test_client()
response = client.get('/', follow_redirects=False)
print(f'Status: {response.status_code}')
print(f'Location: {response.headers.get("Location", "N/A")}')
