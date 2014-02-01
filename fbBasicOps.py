import facebook

#post something on the wall
def postFacebook(oauth_access_token,postMessage):
    graph = facebook.GraphAPI(oauth_access_token)
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")
    graph.put_object("me", "feed", message=postMessage)

#make comments on the posts
def commentFacebook(oauth_access_token, nthComment, comment):
    graph = facebook.GraphAPI(oauth_access_token)
    feed = graph.get_connections("me", "feed")
    post = feed["data"][nthComment]
    graph.put_object(post["id"], "comments", message=comment)

#upload a photo
def photoUpload(oauth_access_token, path, comment):
    graph = facebook.GraphAPI(oauth_access_token)
    graph.put_photo(open(path), comment, None)

