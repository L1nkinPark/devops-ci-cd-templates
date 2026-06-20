import requests
import base64

client_id = '23k9b82pf42m1nv9gslab0b70h'
client_secret = '1t6g4lial29aloo5i4g5hsqb8puskogo6k2kb629nf9ddpebfruv'
redirect_uri = 'https://h1eudayne.dev'
token_endpoint = 'https://us-east-1tpt9lktih.auth.us-east-1.amazoncognito.com/oauth2/token'
authorization_code = '2be0fd25-f22e-471b-846c-0ebcc2303b4b'

# Encode the client ID and client secret
client_credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')

# Prepare the request headers and body
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {encoded_credentials}'
}

body = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri
}

# Make the POST request to the token endpoint
response = requests.post(token_endpoint, headers=headers, data=body)

# Check if the request was successful
if response.status_code == 200:
    tokens = response.json()
    id_token = tokens.get('id_token')
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    
    # Save to files
    with open('id_token.txt', 'w', encoding='utf-8') as f:
        f.write(id_token or '')
    with open('access_token.txt', 'w', encoding='utf-8') as f:
        f.write(access_token or '')
    with open('refresh_token.txt', 'w', encoding='utf-8') as f:
        f.write(refresh_token or '')
        
    print('=== EXCHANGE TOKEN SUCCESS ===')
    print('1. ID Token (Saved at id_token.txt):')
    print(f'   {id_token[:20]}...{id_token[-20:] if id_token else ""}')
    print('2. Access Token (Saved at access_token.txt):')
    print(f'   {access_token[:20]}...{access_token[-20:] if access_token else ""}')
    print('3. Refresh Token (Saved at refresh_token.txt):')
    print(f'   {refresh_token[:20]}...{refresh_token[-20:] if refresh_token else ""}')
else:
    print('Failed to exchange authorization code for tokens:', response.text)