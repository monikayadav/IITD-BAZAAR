db = DAL('mysql://root:monika@localhost/database2')
    
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.define_tables(username=True, signature=False)
auth.settings.registration_requires_approval = True
auth.settings.actions_disabled=['change_password','request_reset_password','profile','forgot_username','retrieve_username','remember']

##from gluon.contrib.login_methods.basic_auth import basic_auth
##auth.settings.login_methods.append(
  ##  basic_auth('https://basic.example.com'))
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

##from gluon.contrib.login_methods.pam_auth import pam_auth
##auth.settings.login_methods=[pam_auth()]

db.define_table('requests' , 
Field('user_id','integer'),
Field('email_id','string'),
Field('phone_no','integer'),
Field('category','string'),
Field('sub_category' , 'string'),
Field('item_name','string'),
Field('description','string'),
Field('price','integer'),
Field('purpose','string'))

db.define_table('orders' ,
Field('user_id','integer'),
Field('category','string'),
Field('sub_category','string'),
Field('item_name','string') ,
Field('buyer_name','string'),
Field('email_id','string'),
Field('phone_no','integer'))
