# Written by Jeffrey Liu
# for TartanHacks 2014
# Oauth for Facebook

import oauth2 as oauth
import urllib
import urllib2
import cgi
import urlparse

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '704355656271613'
FACEBOOK_APP_SECRET = '0d6d5783fe7e575fa9e280fda7e730e1'
# REDIRECT_URI = 'http://127.0.0.1:5000/new'
REDIRECT_URI = 'http://flask-kaikang.appspot.com/finish'
# REDIRECT_URI = 'http://localhost:5000/finish'

def get_goto_url():
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=REDIRECT_URI,scope='publish_stream')
    url = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode(args)
    return url

def get_url(path, args=None):
    args = args or {}
    endpoint = "https://graph.facebook.com"
    return endpoint+path+'?'+urllib.urlencode(args)

def get_code(auth_url):
    # code = auth_url.split('?code=')[-1]
    code = urlparse.parse_qs(urlparse.urlparse(auth_url).query).get('code')[0]
    return code

def get(path, args=None):
    print get_url(path,args)
    return urllib2.urlopen(get_url(path, args=args)).read()


def get_access_token_from_code(code, redirect_uri, app_id, app_secret):
    """Get an access token from the "code" returned from an OAuth dialog.

    Returns a dict containing the user-specific access token and its
    expiration date (if applicable).

    """

    args = {
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": app_id,
        "client_secret": app_secret,
    }
    # We would use GraphAPI.request() here, except for that the fact
    # that the response is a key-value pair, and not JSON.
    print "https://graph.facebook.com/oauth/access_token" +\
                               "?" + urllib.urlencode(args)
    response = urllib2.urlopen("https://graph.facebook.com/oauth/access_token" +
                               "?" + urllib.urlencode(args)).read()
    query_str = cgi.parse_qs(response)
    if "access_token" in query_str:
        result = {"access_token": query_str["access_token"][0]}
        if "expires" in query_str:
            result["expires"] = query_str["expires"][0]
        return result
    else:
        response = json.loads(response)
        raise GraphAPIError(response)

def get_auth_token(auth_url):

    code = get_code(auth_url)
    ACCESS_TOKEN = get_access_token_from_code(code,REDIRECT_URI,FACEBOOK_APP_ID,FACEBOOK_APP_SECRET)

    return ACCESS_TOKEN
