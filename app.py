from flask import Flask,render_template,request,url_for,redirect,session
from pymongo import MongoClient
from flask_session import Session
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY']="@13@6$$#ddfccv"
# app.secret_key = "@13@6$$#ddfccv"
client ="mongodb://localhost:27017/edvora"
cluster=MongoClient(client)
db=cluster['edvora']
col=db['auth']
col2=db['session.flask_session.sessions']

app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB']=db['session']
sess=Session(app)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home',username=session['user']))
    return redirect(url_for('login'))

@app.route('/home/<string:username>')
# @app.route('/home')
def home(username):
    if 'user' in session :
        # print(session.get('user'))
        exist = col.find_one({'username':username})
        print(exist['username'])
        name=exist['name']
        return render_template('index.html',name=name,username=username)
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def register():

    # try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            userName = request.form['uname']
            password = request.form['password']
            flag=0
            # Use get() method
            if(not name or not userName or not email or not password):
                message = "Please fill required fields"
                return render_template('signup.html', message=message)
            else:

                # Registering for Bank Manager

                exist = col.find_one({'username': userName,'email':email})
                if exist is None:
                    hashpass = bcrypt.hashpw(
                       password.encode('utf-8'), bcrypt.gensalt())

                    col.insert(
                        {'username': userName, 'name': name, 'email': email, 'password': hashpass,'flag':flag})

                    session['user'] = userName
                    # session['id'] = exist['_id']

                    return redirect(url_for('login'))
                message = "User already exist"
                return render_template('signup.html', message=message)

    # except:
    #     message = "Something messed up!! Please Register again"
    #     return render_template("signup.html", message=message)

        return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def login():

    
        if request.method == 'POST':

            userName = request.form['uname']
            if(not userName):
                message = "Please fill required fields"
                return render_template('signin.html', message=message)
            else:

                userLogin = col.find_one({'username': userName})
                if userLogin:
                    if bcrypt.hashpw(request.form['password'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                        print(request.form['password'])
                        session['user'] = userName
                        # col.update_one({{'username': userName},{"$set":{'email':userName}}})
                        # session['id'] = userLogin['_id']
                        # print(session['id'])
                        return redirect(url_for('home',username=userName))
                        # return render_template('index.html',name=userLogin['name'],username=userLogin['username'])

                message = "Invalid credentials"
                return render_template('signin.html', message=message)

    # except:
    #     message = "Something messed up!!"
    #     return render_template("signin.html", message=message)

        return render_template("signin.html")

@app.route('/changepassword',methods=["GET","POST"])
def changePass():
    if 'user' in session:
        # user= col.find_one({'username': session['user']})
        # if(user['flag']==1):
            if request.method == 'POST':
                oldpass = request.form['oldpass']
                newpass = request.form['newpass']
                if(not oldpass or not newpass):
                        message = "Please fill required fields"
                        return render_template('changepassword.html', message=message)
                user= col.find_one({'username': session['user']})
                if bcrypt.hashpw(oldpass.encode('utf-8'), user['password']) == user['password']:
                    hashpass = bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt())
                    col.update_one({'username':session['user']},{"$set":{"password":hashpass,'flag':0}})
                    # return render_template('index.html',username=session['user'],name=user['name'])
                    return redirect(url_for('home',username=session['user']))
                message="Old Password incorrect"
                return render_template('changepassword.html',message=message)
            return render_template('changepassword.html')
        # session.pop('user',None)
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    # exist=col.find_one({'username':session['user']})
    # print(exist)
    # exist2=col.find_one({'_id':session['id']})

    # if exist['username']==exist2['username']:
        # print(session['id'],"deleted")

        # col2.f
    # print(session.get('user'), "valueeeee")
        # print(col2['id'])
    session.pop('user',None)
        
    # else:
    #     session['user']=session.get('user')
    return redirect(url_for('index'))


if "__main__"==__name__:
    app.run(port=3000,debug=True)
