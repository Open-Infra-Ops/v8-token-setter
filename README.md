# v8-token-setter
A server update and apply v8 token

### refresh
The v8 token has an expiration time and needs to be refreshed regularly.
The server supports command line to refresh the token, just type `python3 manage.py refresh`.

### API
The server supports query v8 token through API and it needs a specific query token.

uri: /token/?token=
