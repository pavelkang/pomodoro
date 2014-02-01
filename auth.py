import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.api.client import EvernoteClient
from parsing import *

client_one = EvernoteClient(
    consumer_key = 'jeff95723',
    consumer_secret = '12e44f902d948991',
    sandbox = True
)

def parse_query_string(authorize_url):
    uargs = authorize_url.split('?')
    vals = {}
    if len(uargs) == 1:
        raise Exception('Invalid Authorization URL')
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals

def get_goto_url():
    # request_token = client_one.get_request_token('http://localhost:5000/App')
    request_token = client_one.get_request_token('http://flask-kaikang.appspot.com/App')
    goto_auth_url = client_one.get_authorize_url(request_token)
    return (goto_auth_url, request_token)

def get_auth_token(request_token, authurl):
    vals = parse_query_string(authurl)
    auth_token = client_one.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        vals['oauth_verifier']
    )
    return auth_token

def authorize(auth_token):
    client = EvernoteClient(token=auth_token)
    userStore = client.get_user_store()
    user = userStore.getUser()
    noteStore = client.get_note_store()
    filter = NoteStoreTypes.NoteFilter()
    filter.words = "intitle:TODO"
    notes = noteStore.findNotes(filter,0,100)
    contents = []
    for note in notes.notes:
        contents.append(noteStore.getNoteContent(note.guid))
    processed_message = detag(contents[0])
    return (processed_message, auth_token)
