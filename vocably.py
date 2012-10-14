from bottle import route, run, debug, template, request, static_file, redirect

from utils import vocably_oauth as oauth, score, definition, database

# Landing Page
@route('/')
def home():
    output = template('home')
    return output

@route('/words.json')
def wordsdict():
    # Get words for user
    user_email = oauth.user_email()
    newwords = score.choose_words(user_email)
    word_defs = {w:definition.definition(w) for w in newwords}
    #word_defs = {"word1":"def1", "word2":"def2", "word3":"def3"}
    return word_defs

@route('/words')
def words():
    output = template('words', word_defs=wordsdict())
    return output

@route('/login')
def login():
    print "Logging in a user: redirecting to Google"
    redirect(oauth.authorization_url())

@route('/logout')
def logout():
    oauth.deauthorize()

@route('/oauth2callback')
def login_callback():
    print "Login callback from Google"
    if request.query.error:
        print "There was an error: '%s'" % request.query.error
        print "Redirecting back to root"
        redirect('/')
    else:
        print "Successfully acquired an authentication token"
        oauth.authorize(request.query.code)
        database.create_user(oauth.user_email(), 0)
        redirect('/emails')

@route('/emails')
def fetch_mail():
    email_text = oauth.fetch_mail()
    print "Got a bunch of email text"
    score.score_user(oauth.user_email(), email_text)
    redirect('/words')

# Static Files
@route('/css/:path#.+#', name='css')
def css(path):
    return static_file(path, root='css')

@route('/img/:path#.+#', name='img')
def img(path):
    return static_file(path, root='img')

@route('/js/:path#.+#', name='js')
def js(path):
    return static_file(path, root='js')

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
