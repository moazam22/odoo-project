import functools
import xmlrpc.client
HOST = 'moazam-vostro-3559'
PORT = 8069
DB = 'Pre-Internship'
USER = 'john@email.com'
PASS = '1234'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1) Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print("Logged in as %s (uid:%d)" % (USER,uid))
call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)
# 2) get_sessions
sessions = call('openacademy.session','search_read', [], ['name','seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))
# 3) create a new session
session_id = call('openacademy.session', 'create', {
    'name' : 'My test 4 session',
    'course_id' : 1,
})