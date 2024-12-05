import requests

# Keycloak credentials
token_url = "http://localhost:8080/realms/master/protocol/openid-connect/token"
client_id = "admin"
client_secret = "b2k13JjcgI0hJtUgHhL5r1Yn8yNo4pnr"

# Get the token
response = requests.post(token_url, data={
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials',
})
print(response.text)
access_token = response.json().get("access_token")

# Call the protected resource
api_url = "http://127.0.0.1:8000/dummy/1/?format=json"
headers = {"Authorization": f"Bearer {access_token}"}
api_response = requests.get(api_url, headers=headers)

print(api_response.text, api_response.status_code)
