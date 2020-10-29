import xmlrpc.client

host = 'localhost'
port = 8069
url = "http://%s:%d" % (host, port)
db = input('Database:')
username = input('User:')
password = input("Password:")

"""
    Logging in

    Odoo requires users of the API to be authenticated before they can query most data.
    
    The xmlrpc/2/common endpoint provides meta-calls which don’t require authentication, such as the 
    authentication itself or fetching version information. To verify if the connection information is 
    correct before trying to authenticate, the simplest call is to ask for the server’s version. 
    The authentication itself is done through the authenticate function and returns a user identifier (uid) 
    used in authenticated calls instead of the login.
"""
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# print(common.version())

uid = common.authenticate(db, username, password, {})
# print(uid)

"""
    Calling methods

The second endpoint is xmlrpc/2/object, is used to call methods of odoo models via the execute_kw RPC function.

Each call to execute_kw takes the following parameters:

    the database to use, a string
    the user id (retrieved through authenticate), an integer
    the user’s password, a string
    the model name, a string
    the method name, a string
    an array/list of parameters passed by position
    a mapping/dict of parameters to pass by keyword (optional)

For instance to see if we can read the res.partner model we can call check_access_rights with operation passed by 
position and raise_exception passed by keyword (in order to get a true/false result rather than true/error):
"""
name_model ="openacademy.session"
#name_model = input("Name of model:")

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# print(models.execute_kw(db, uid, password,
#     'res.partner', 'check_access_rights',
#     ['read'], {'raise_exception': False}))


"""
    List records

Records can be listed and filtered via search().

search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all 
records matching the filter. To list customer companies for instance:

    Pagination

By default a search will return the ids of all records matching the condition, which may be a huge number. 
offset and limit parameters are available to only retrieve a subset of all matched records.
"""
# print(models.execute_kw(db, uid, password,
#     name_model, 'search',
#     [[['active', '=', True]]]))
# print(models.execute_kw(db, uid, password,
#     name_model, 'search',
#     [[['active', '=', True]]],
#     {'limit': 5})
# )