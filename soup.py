from bottle import route, run, request
import spotipy
from spotipy import oauth2

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '559598eb217440abb4fcd7629a363a53'
SPOTIPY_CLIENT_SECRET = 'efa4497b541a437295128ae14550ff8a'
SPOTIPY_REDIRECT_URI = 'https://spotifysoup.herokuapp.com/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@route('/')
def index():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print "Found cached token!"
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print "Found Spotify auth code in Request URL! Trying to get valid access token..."
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print "Access token available! Trying to get user information..."
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=8080)
