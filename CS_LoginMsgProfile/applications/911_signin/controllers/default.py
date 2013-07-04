# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.contrib.login_methods.rpx_account import use_janrain
from gluon.contrib.login_methods.extended_login_form import ExtendedLoginForm

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    
    form_janrain = use_janrain(auth,filename='private/janrain.key')
    auth.settings.login_form = ExtendedLoginForm(auth, form_janrain, signals=['token'])
    return dict(form=auth())


def home():
    return dict(uid=auth.user_id)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

@auth.requires_login()
def myprofile():
	tmp_usr=db(db.basic_info.username == auth.user.username)(db.basic_info.email == auth.user.email).select().first()
	if tmp_usr==None:
		db.basic_info.email.default=auth.user.email
		form=SQLFORM(db.basic_info, submit_button='Create Profile')
		form.vars.first_name=auth.user.first_name
		form.vars.last_name=auth.user.last_name
		form.vars.username=auth.user.username

	else:
		form=SQLFORM(db.basic_info,tmp_usr.id,showid=False, submit_button='Update Profile')

	form.vars.prefix = 'Mr.'
	form.vars.email_share_with = 'Only my network'
	form.vars.phone_share_with = 'Only my network'

	db.experience.username.default=auth.user.username
	db.education.username.default=auth.user.username
	form2=SQLFORM(db.experience, submit_button='Add experience')
	form3=SQLFORM(db.education, submit_button='Add education')

	if form.process().accepted:
		response.flash='Profile updated'

	if form2.process().accepted:
		response.flash='Experience added'

	if form3.process().accepted:
		response.flash='Education added'

	experience=db(db.experience.username == auth.user.username).select()
	education=db(db.education.username == auth.user.username).select()

	return dict(form=form, form2=form2, form3=form3, experience=experience, education=education)



@auth.requires_login()
def profile():
	uname = request.args(0)
	user_obj = db(db.auth_users.username == uname).select()
	profile_obj = db(db.basic_info.username == uname).select()
	exp_obj = db(db.experience.username == uname).select()
	edu_obj = db(db.education.username == uname).select()
	return dict(user=user_obj, profile=profile_obj, experience=exp_obj, education=edu_obj)


@auth.requires_login()
def changepicture():
	tmp_pic=db(db.profile_pic.uname == auth.user.username).select()
	if tmp_pic:
		form=SQLFORM(db.profile_pic,tmp_pic.first().id,showid=False, submit_button='Upload Picture')
	else:
		db.profile_pic.uname.default=auth.user.username
		form=SQLFORM(db.profile_pic, submit_button='Upload Picture')

	if form.process().accepted:
		response.flash='Image uploaded'
		redirect(URL('myprofile'))

	return dict(form=form)


@auth.requires_login()
def compose():
	form=SQLFORM(db.message)
	form.vars.sender=auth.user.username
	form.vars.read=False

	if form.process().accepted:
		response.flash='Message Sent'
		row = db(db.auth_users.username == form.vars.reciever).select().first()
		if row:
			ctr=row.unread_ctr+1
			db.auth_users[row.id] = dict(unread_ctr=ctr)
	return dict(form=form)

@auth.requires_login()
def inbox():
	inbox=db(db.message.reciever == auth.user.username).select(db.message.id, db.message.sender,db.message.subject,db.message.read, orderby=~db.message.id )
	return dict(inbox=inbox)

@auth.requires_login()
def message():
	mail = db.message(request.args(0))
	if mail.read == False:
		db.message[mail.id] = dict(read=True)
		ctr = db.auth_users(auth.user.id).unread_ctr-1
		db.auth_users[auth.user.id]	= dict(unread_ctr=ctr)
	return dict(mail=mail)

@auth.requires_login()
def outbox():
	outbox=db(db.message.sender == auth.user.username).select(db.message.id, db.message.reciever,db.message.subject, db.message.read, orderby=~db.message.id )
	return dict(outbox=outbox)

@auth.requires_login()
def sent_message():
	mail = db.message(request.args(0))
	return dict(mail=mail)
