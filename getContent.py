# Written by Jeffrey Liu
# this will get the note named "TODO"
"""
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.api.client import EvernoteClient
"""

def parse_query_string(authorize_url):
    uargs = authorize_url.split('?')
    vals = {}
    if len(uargs) == 1:
        raise Exception('Invalid Authorization URL')
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals

def getTODOnote(authurl,request_token, CLIENT):
    ##
    # Parse the URL to get the OAuth verifier
    ##
    try:
        vals = parse_query_string(authurl)
    except:
        return "ERROR 0 ___________________________"
    try:
        vals_veri = vals['oauth_verifier']
    except:
        return "ERROR 1 ___________________________"
    try:
        req_token = request_token['oauth_token']
    except:
        return "ERROR 2 ___________________________"
    try:
        req_secret = request_token['oauth_token_secret']
    except:
        return "ERROR 3 ___________________________"
    try:
        TEST_CLIENT = EvernoteClient(
                consumer_key = 'jeff95723',
                consumer_secret = '12e44f902d948991',
                sandbox = True
        )
    except:
        return "ERROR 3.5 --------------------"
    try:
        auth_token = TEST_CLIENT.get_access_token(
            req_token,
            req_secret,
            vals_veri
            )
    except:
        return sys.exc_info()[0] + "-------------------------"
    ##
    # Create a new EvernoteClient instance with our auth
    # token.
    ##
    try:
        client = EvernoteClient(token=auth_token)
    except:
        return "ERROR 4____________________________________________"

    ##
    # Test the auth token...
    ##
    try:
        userStore = client.get_user_store()
    except:
        return "ERROR 5--------------------"
    try:
        user = userStore.getUser()
    except:
        return "ERROR 6 ______________________"

    return "I wont get an error"



"""
    noteStore = client.get_note_store()
    for nb in notebooks:
        notebooksGUID = []
        notebooksGUID.append(nb.guid)
    filter = NoteStoreTypes.NoteFilter()
    filter.words = "intitle:TODO"
    notes = noteStore.findNotes(filter,0,100)

    ##
    # If our username prints, it worked.
    ##
    notesGUID = []
    contents = []
    for note in notes.notes:
        notesGUID.append(note.guid)
        contents.append(noteStore.getNoteContent(note.guid))
    return contents[0]
"""
