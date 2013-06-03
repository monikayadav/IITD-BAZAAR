# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    return dict()

def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query1 = db.requests.category.like('%'+partialstr+'%')
    query2 = db.requests.sub_category.like('%'+partialstr+'%')
    query3=  db.requests.item_name.like('%'+partialstr+'%') 
    query4=  db.requests.description.like('%'+partialstr+'%')
    query5=  db.requests.purpose.like('%'+partialstr+'%')
    categories = db(query1).select(db.requests.category,distinct=True,orderby=db.requests.category)
    sub_categories=  db(query2).select(db.requests.sub_category,distinct=True,orderby=db.requests.sub_category)
    item_names=  db(query3).select(db.requests.item_name,distinct=True,orderby=db.requests.item_name)
    descriptions=  db(query4).select(db.requests.description,distinct=True,orderby=db.requests.description)
    purpose=  db(query5).select(db.requests.purpose,distinct=True,orderby=db.requests.purpose)
    items=[]
    for (i,requests) in enumerate(categories):
        items.append(DIV(A(requests.category, _id="res1%s"%i, _href="#", _onclick="copyToBox($('#res1%s').html())"%i), _id="resultLiveSearch"))
    for (i,requests) in enumerate(sub_categories):
        items.append(DIV(A(requests.sub_category, _id="res2%s"%i, _href="#", _onclick="copyToBox($('#res2%s').html())"%i), _id="resultLiveSearch"))
    for (i,requests) in enumerate(item_names):
        items.append(DIV(A(requests.item_name, _id="res3%s"%i, _href="#", _onclick="copyToBox($('#res3%s').html())"%i), _id="resultLiveSearch"))
    for (i,requests) in enumerate(descriptions):
        items.append(DIV(A(requests.description, _id="res4%s"%i, _href="#", _onclick="copyToBox($('#res4%s').html())"%i), _id="resultLiveSearch"))
    for (i,requests) in enumerate(purpose):
        items.append(DIV(A(requests.purpose, _id="res5%s"%i, _href="#", _onclick="copyToBox($('#res5%s').html())"%i), _id="resultLiveSearch"))
    return TAG[''](*items)

    
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
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


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



#displays the recent posts
def recent_posts():
    result=''
    my_query=db.requests.id>0
    myset=db(my_query)
    rows = myset.select()
    print rows
    for row in rows:
        result=str(row.id) +'\t'+ str(row.user_id) +'\t'+ str(row.email_id) +'\t'+ str(row.phone_no) +'\t'+ str(row.category) +'\t'+ str(row.sub_category) +'\t'+ str(row.item_name) +'\t'+ str(row.description) +'\t'+ str(row.price)  +'\t'+ str(row.purpose) +'\n'+ result       
    return result
        
         
           
#search through search bar
def search1():
    m=''
    result=''
    y=[]
    x=request.body.read()
    result=Query_results(str(x))
    if result!='':
        return result
    else:
        y=x.split()
        for a in y:
            result=result + Query_results(str(a))
        return result


def Query_results(y):
    a=''
    result=''
    count1=0
    my_query=(db.requests.category.contains(y)) | (db.requests.sub_category.contains(y)) | (db.requests.item_name.contains(y)) | (db.requests.purpose.contains(y)) | (db.requests.description.contains(y))
    myset=db(my_query)
    rows = myset.select()
    for row in rows:
        result=str(row.id) +'\t'+ str(row.user_id) +'\t'+ str(row.email_id) +'\t'+ str(row.phone_no)+'\t'+ str(row.category) +'\t'+ str(row.sub_category) +'\t'+ str(row.item_name) +'\t'+ str(row.description) +'\t'+str(row.price) +'\t'+str(row.purpose) +'\n'+ result       
    count1=myset.count()
    if count1==0:
        return str(a)
    else:
        return result

#search through menubar
def search2():
     a=''
     result=''
     count2=0
     b=[]
     x=request.body.read()
     b=x.split("#")
     my_query=((db.requests.category.contains(b[0])) & (db.requests.sub_category.contains(b[1])) )
     myset=db(my_query)
     rows = myset.select()
     count2=myset.count()
     for row in rows:
        result=str(row.id) +'\t'+ str(row.user_id) +'\t'+ str(row.email_id) +'\t'+ str(row.phone_no)+'\t'+ str(row.category) +'\t'+ str(row.sub_category) +'\t'+ str(row.item_name) +'\t'+ str(row.description) +'\t'+str(row.price) +'\t'+str(row.purpose) +'\n'+ result       
     if count2==0:
         return str(a)
     else:
         return result


def post_ad():
    return dict()
    
    
def fetch_uid():
    from gluon.tools import Auth
    auth = Auth(db)
    return auth.user_id
   
    
def insert_post():
    print "hello"
    from gluon.tools import Auth
    auth = Auth(db)
    text1=request.vars['text1']
    text2=request.vars['text2']
    text3=request.vars['text3']
    text4=request.vars['text4']
    text5=request.vars['text5']
    text6=request.vars['text6']
    text7=request.vars['text7']
    text8=request.vars['text8']
    db.requests.insert(user_id=auth.user_id, phone_no=text1, email_id=text2, category=text3, sub_category=text4, item_name=text5, description=text6,price=text7,purpose=text8)
    session.flash="Post Submitted"
    redirect(URL('index'))
    return dict()

def insert_order():
    x=request.body.read()
    a="r"
    b=x.split("#")
    my_query=(db.requests.category==b[0]) & (db.requests.sub_category==b[1]) & (db.requests.item_name==b[2])
    rows=db(my_query).select(db.requests.user_id)
    for row in rows:
        id1=row.user_id
    db.orders.insert(user_id=id1, category=b[0], sub_category=b[1],item_name=b[2],buyer_name=b[3],email_id=b[4],phone_no=b[5])
    return a

def profile():
    a=""
    count=0
    result=""
    from gluon.tools import Auth
    auth = Auth(db)
    my_query=(db.orders.user_id==auth.user_id) 
    myset=db(my_query)
    rows = myset.select(db.orders.ALL)
    for row in rows:
        result= str(row.category) +'\t'+ str(row.sub_category) +'\t'+ str(row.item_name) +'\t'+ str(row.buyer_name)+'\t'+ str(row.email_id) +'\t'+ str(row.phone_no) +'\n'+ result       
    count=myset.count()
    if count==0:
        return str(a)
    else:
        return result
