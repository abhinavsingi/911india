# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate, Mail
auth = Auth(db=db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'email@xyz.com'
mail.settings.login = 'username:passwd'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

auth.settings.table_user = db.define_table(
	"auth_users",
	Field('first_name', requires = [IS_NOT_EMPTY(), IS_LENGTH(32), IS_ALPHANUMERIC()]),
	Field('last_name', requires = [IS_NOT_EMPTY(), IS_LENGTH(32), IS_ALPHANUMERIC()]),
	Field('username', length=32, unique = True, requires = [IS_NOT_EMPTY(), IS_LENGTH(32)]),
	Field('email', length=128, unique = True, default='', requires = [IS_EMAIL(), IS_NOT_EMPTY()]),
	Field('password', 'password', readable=False, label='Password', requires=CRYPT(digest_alg='sha512')), 
	Field('registration_key', length=128, writable=False, readable=False, default=''),
	Field('unread_ctr', 'integer', default=0, writable=False, readable=False))
	
db.define_table('basic_info',
	Field('prefix', requires = IS_IN_SET(['Mr.', 'Mrs.', 'Dr.'])),
	Field('first_name', requires = [IS_NOT_EMPTY(), IS_LENGTH(32), IS_ALPHANUMERIC()]),
	Field('last_name', requires = [IS_NOT_EMPTY(), IS_LENGTH(32), IS_ALPHANUMERIC()]),
	Field('suffix', requires = [IS_LENGTH(32), IS_ALPHANUMERIC()]),
	Field('username', length=32, writable=False, readable=False),
	Field('email', writable=False),
	Field('email_share_with', requires = IS_IN_SET(["Don't Share", "Only my network", "Everyone"])),
	Field('phone_no', 'integer', requires = [IS_LENGTH(11,11), IS_ALPHANUMERIC()]),
	Field('phone_share_with', requires = IS_IN_SET(["Don't Share", "Only my network", "Everyone"])),
	Field('mobile_no', 'integer', requires = [IS_LENGTH(10,10), IS_ALPHANUMERIC()]),
	Field('chat_im', requires = [IS_LENGTH(32)]),
	Field('current_location', requires = [IS_LENGTH(150)]),
	Field('hometown', requires = [IS_LENGTH(150)]))
	
db.define_table('experience',
	Field('username', length=32, writable=False, readable=False),
	Field('post', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('hospital', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('city', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('country', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('start_date', 'date', requires = [IS_NOT_EMPTY(), IS_DATE()]),
	Field('end_date', 'date', requires = [IS_NOT_EMPTY(), IS_DATE()]),
	Field('description', 'text', length=500))

db.define_table('education',
	Field('username', length=32, writable=False, readable=False),
	Field('degree', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('institute', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('city', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('country', requires = [IS_NOT_EMPTY(), IS_LENGTH(64)]),
	Field('start_date', 'date', requires = [IS_NOT_EMPTY(), IS_DATE()]),
	Field('end_date', 'date', requires = [IS_NOT_EMPTY(), IS_DATE()]),
	Field('description', 'text', length=500))

db.define_table('message',
    Field('sender', length=32, writable=False, readable=False),
    Field('reciever', length=32, requires = [IS_NOT_EMPTY(), IS_LENGTH(32)]),
	Field('subject', length=200, requires = [IS_LENGTH(200)]),
	Field('message', 'text', length=1000, requires = [IS_LENGTH(1000)]),
	Field('read', 'boolean', writable=False, readable=False),
	Field('attach', 'upload')
	)

db.define_table('profile_pic',
	Field('uname', readable=False, writable=False),
	Field('file', 'upload'))

options = [T('Conference'), T('Workshop'), T('Webinar/Pod-cast')]

db.define_table('events', 
	Field('Title', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
	Field('City', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
	Field('Country', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
	Field('Event_URL', default="http://", requires=IS_URL()),
	Field('Starts_At', 'datetime', requires=IS_NOT_EMPTY()),
	Field('Ends_At', 'datetime', requires=IS_NOT_EMPTY()),
	Field('Event_Type', widget=SQLFORM.widgets.radio.widget, requires=IS_IN_SET(options)),
	Field('Category', widget=SQLFORM.widgets.options.widget, requires=IS_IN_SET(['Physician/Surgeon', 'Psychiatry', 'Paediatrics', 'Opthalmology', 'OBG', 'Neurology', 'ENT', 'Dermatology', 'Dentistry', 'Nursing', 'Physio Occupational Therapy', 'Audiology/Speech Therapy', 'Alternative Medicine', 'Cardiology', 'Urology', 'Clinical Psychologist'], zero=T('Choose one'))),
	Field('Discount', widget=SQLFORM.widgets.radio.widget, requires=IS_IN_SET(['Yes', 'No'])),
	Field('Created_On', 'datetime', writable=False, default = request.now),
	Field('read', 'boolean', writable=False, readable=False),
	Field('unread_ctr', 'integer', default=0, writable=False, readable=False))

db.define_table('case_studies',
	Field('Subject', requires=IS_NOT_EMPTY()),
	Field('Question', 'text', requires=IS_NOT_EMPTY()))

db.define_table('connection',
	Field('uid1', readable=False, writable=False),
	Field('uid2', readable=False, writable=False))
