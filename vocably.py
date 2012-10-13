from bottle import route, run, template, redirect, request

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

import httplib2

@route('/')
def home():
    return template('mobile_website/index.html')

@route('/login')
def login():
    print "Logging in a user: redirecting to Google"
    redirect(flow.step1_get_authorize_url())

@route('/oauth2callback')
def login_callback():
    print "Login callback from Google"
    if request.query.error:
        print "There was an error: '%s'" % request.query.error
        print "Redirecting back to root"
        redirect('/')
    else:
        print "Successfully acquired an authentication token"
        credentials = flow.step2_exchange(request.query.code)
        storage.put(credentials)
        print "Stored credentials"
        redirect('/')
        # http = credentials.authorize(httplib2.Http())

flow = flow_from_clientsecrets('config/client_secrets.json',
                               scope='https://mail.google.com/',
                               redirect_uri='http://localhost:8080/oauth2callback')
storage = Storage('config/credentials')
run(host='localhost', port=8080, debug=True, reloader=True)
