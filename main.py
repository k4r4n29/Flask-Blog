'''
    import flask-mail 
'''
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

#this variable is to check whether you are working in local server or production server
local_server = True
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
#Mail method functnality depends upon app server
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

#Contacts model view
class Contacts(db.Model):
    '''
        sno , name, email, phone_num,msg, date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(12),  nullable=False)
    phone_num = db.Column(db.Integer, nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)

#Posts  model view
class Posts(db.Model):
    '''
        sno , name, email, phone_num,msg, date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    slug = db.Column(db.String(12),  nullable=False)
    content = db.Column(db.String(80), nullable=False)
    file_name = db.Column(db.String(50),nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route('/')
def index():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html',params=params,posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first() # this is to make a post slug to be first not be a duplicate
    return render_template('post.html', params=params, post=post)

@app.route('/contact' , methods=['GET','POST'])
def contact():
    if(request.method == 'POST'):
         #add entry to the database
         name=request.form.get('name')
         email=request.form.get('email')
         phone=request.form.get('phone')
         message=request.form.get('message')
         entry = Contacts(name=name,email=email,phone_num=phone,msg=message,date=datetime.now())
         db.session.add(entry)
         db.session.commit()
         mail.send_message('new message from '+name,sender=email,recipients = [params['gmail-user']],body=message+"\n"+phone)
    return render_template('contact.html',params=params)

app.run(debug=True)
