import xmlrpc.client

host = 'localhost'
port = 8069
url = "http://%s:%d" % (host, port)
db = input('Database:')
username = input('User:')
password = input("Password:")

# The xmlrpc/2/common endpoint provides meta-calls which don’t require authentication,
# such as the authentication itself or fetching version information.
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# print(common.version())

# The authentication itself is done through the authenticate function and returns a user
# identifier (uid) used in authenticated calls instead of the login.
uid = common.authenticate(db, username, password, {})
# print(uid)