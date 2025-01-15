from flask import Flask, redirect, jsonify, request, session, send_from_directory
import requests 
import urllib.parse
from datetime import datetime
import os

app = Flask(__name__, static_folder='build')
app.secret_key = os.getenv('SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID') ##provided by spotify 
CLIENT_SECRET = os.getenv('CLIENT_SECRET')##provided by spotify 
REDIRECT_URI = 'https://spinsync.onrender.com/callback' ##set in the dashboard

##print("CLIENT_ID:", CLIENT_ID)

AUTH_URL = 'https://accounts.spotify.com/authorize' ##url to get token from spotify 
TOKEN_URL = 'https://accounts.spotify.com/api/token' ## url to refresh token 
API_BASE_URL = 'https://api.spotify.com/v1/' 


@app.route('/')
def serve():
    # Serve React's index.html
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_files(path):
    # Serve other static files or fallback to index.html
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login():
    ##define necessary scopes
    scope = 'user-read-private user-read-email'

    ##create params to pass over to the call we make to spotify 
    params = {
        'client_id' : CLIENT_ID,
        'response_type': 'code', ## what spotify says to use
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True ##forces the user to log in every time, change later on 
    }

    ## redirect to url and pass params 
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    ##if user could not log in
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    ##
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code', 
            'redirect_uri': REDIRECT_URI, 
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        ##token info contains 
        ##access token
        ##refresh token 
        ##expires in 

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    ##check if token exists 
    if 'access_token' not in session:
        return redirect('/login')
    
    ##check if token is expired 
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    ##make request to spotify API

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    return jsonify(playlists)

##refresh token 
@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session: 
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'], 
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_ID
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')
    
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))  # Use the PORT environment variable or default to 8000
    app.run(host='0.0.0.0', port=port)