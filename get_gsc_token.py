"""
One-time script to get a Google Search Console OAuth refresh token.
Run: py get_gsc_token.py path/to/oauth_client.json
"""
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

client_json = sys.argv[1] if len(sys.argv) > 1 else "oauth_client.json"

flow = InstalledAppFlow.from_client_secrets_file(client_json, SCOPES)
creds = flow.run_local_server(port=0)

print("\n✅ Copy these values into your Streamlit secrets:\n")
print(f'[gsc]')
print(f'site_url = "https://scentifiedperfume.com"')
print(f'client_id = "{creds.client_id}"')
print(f'client_secret = "{creds.client_secret}"')
print(f'refresh_token = "{creds.refresh_token}"')
