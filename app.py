"https://docs.python.org/2/library/doctest.html"
from flask import Flask
from flask import make_response
from flask import jsonify
import json
from flask import Flask, request, jsonify
from flask import abort
from flask import make_response, url_for, redirect, session
from time import gmtime, strftime
from flask import render_template 
import MySQLdb, os
from flask_cors import CORS, cross_origin 
from time import gmtime, strftime
import flask


app = Flask(__name__)
app.debug = True

CORS(app)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
"""cors = CORS(app, resources={r"/api/*": {"origins": "*"}})"""

MYSQL_PORT=int(os.environ.get('MYSQL_PORT'))
MYSQL_NAME=os.environ.get('MYSQL_NAME')
MYSQL_USER=os.environ.get('MYSQL_USER')
MYSQL_PSWD=os.environ.get('MYSQL_PSWD')

def mk_conn():
    return MySQLdb.connect(db=MYSQL_NAME, user=MYSQL_USER, passwd=MYSQL_PSWD, port=MYSQL_PORT)
    '''return MySQLdb.connect(MYSQLCONNSTR_localdb)'''

@app.route("/api/v1/info")
def home_index():
    conn = mk_conn()     
    cur = conn.cursor()
    print ("Opened database successfully")
    api_list=[]
    cur.execute("SELECT buildtime, version, methods, links   from apirelease")     
    data = cur.fetchall()
    for row in data:
        a_dict = {}
        a_dict['version'] = row[1]
        a_dict['buildtime'] = str(row[0])
        a_dict['methods'] = row[3]
        a_dict['links'] = row[2]
        api_list.append(a_dict)
    cur.close()
    conn.close()
    return jsonify({'api_version': api_list}), 200

def list_users():
    conn = mk_conn()    
    cur = conn.cursor()
    print ("Opened database successfully")
    api_list=[]
    cur.execute("SELECT username, full_name, emailid, password, id from users")
    data = cur.fetchall()
    for row in data:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['name'] = row[1]
        a_dict['email'] = row[2] 
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)
    cur.close()
    conn.close()
    return jsonify({'user_list': api_list})


@app.route('/api/v1/users', methods=['GET']) 
def get_users():
    return list_users()

def list_user(user_id):  
    conn = mk_conn()     
    cur = conn.cursor()
    print("Opened database successfully")       
    api_list = []       
    cur.execute("SELECT * from users where id=%s",(user_id,))       
    data = cur.fetchall()       
    if len(data) != 0:          
        user = {'username': data[0][0], 'name': data[0][3], 'email': data[0][1], 'password': data[0][2],'id': data[0][4]}
        cur.close()
        conn.close()
    else:
        abort(404)             
    return jsonify(user)
 
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

@app.errorhandler(404)
def resource_not_found(error):      
    return make_response(jsonify({'error': 'Resource not found!'}),  404) 

def add_user(new_user):
    conn = mk_conn()
    print ("Opened database successfully")
    cur = conn.cursor()
    print (new_user['username'], new_user['email'])
    cur.execute("SELECT * from users where username = %s or emailid = %s ", (new_user['username'], new_user['email']))
    data = cur.fetchall()
    print(data)
    if len(data) != 0:
        abort(409)
    else:
        cur.execute("insert into users (username, emailid, password, full_name) values(%s,%s,%s,%s)",(new_user['username'],new_user['email'], new_user['password'], new_user['name']))
        conn.commit()
        return "Success"


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {'username': request.json['username'], 'email': request.json['email'], 'name': request.json.get('name',""), 'password': request.json['password']}
    return jsonify({'status': add_user(user)}), 201

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

def del_user(del_user):
    conn = mk_conn()
    print ("Opened database successfully")
    cur=conn.cursor()
    cur.execute("SELECT * from users where username= %s ", (del_user,))
    data = cur.fetchall()
    if len(data) == 0:         
        abort(404)       
    else:        
        cur.execute("delete from users where username== %s",(del_user,))        
        conn.commit()          
    return "Success" 

def upd_user(user):
    conn = mk_conn()
    print ("Opened database successfully")
    cur =conn.cursor()
    cur.execute("SELECT * from users where id= %s ", (user['id'],))
    data = cur.fetchall()
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
    for i in key_list:
        if i != "id":
            print (user, i)
            # cur.execute("UPDATE users set {0}=%s where id=%s ", (i, user[i], user['id']))
        cur.execute("""UPDATE users SET {0} = %s WHERE id = %s""".format(i), (user[i], user['id'],))
        conn.commit()
    return "Success"

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
         abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    print(key_list)
    for i in key_list:
        user[i] = request.json[i]
        print (user)
    return jsonify({'status': upd_user(user)}), 200

def list_tweets():
    conn = mk_conn()     
    cur = conn.cursor()
    print ("Opened database successfully")
    api_list=[]
    cur.execute("SELECT username, body, tweet_time, id from tweets")
    data = cur.fetchall()
    if data != 0:
        for row in data:
            tweets = {'tweetedby' :  row[0] , 'body' : row[1], 'timestamp': str(row[2]), 'id' : row[3]}
            api_list.append(tweets)
    else:
        return api_list
    cur.close()
    conn.close()
    return jsonify({'tweets_list': api_list})

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def add_tweet(new_tweets):
    conn = mk_conn()
    print ("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT * from users where username=%s ", (new_tweets['username'],))
    data = cur.fetchall()
    print("data")
    print(data)
    print(new_tweets)
    if len(data) == 0:
        abort(404)
    else:
        cur.execute("INSERT into tweets (username, body, tweet_time) values(%s,%s,%s)", (new_tweets['username'], new_tweets['body'], new_tweets['created_at']))
        
    conn.commit()   
    cur.close()
    conn.close()
    return "Success"
    
@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():       
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet = {'username' : request.json['username'], 'body': request.json['body'], 'created_at' : strftime("%Y-%m-%d %H:%M:%S", gmtime())}
    #print (user_tweet)
    return  jsonify({'status': add_tweet(user_tweet)}), 201

def list_tweet(user_id):
    print (user_id)
    conn = mk_conn()
    print ("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT * from tweets  where id=%s",(user_id,))
    data = cur.fetchall() 
    print (data) 
    if len(data) == 0:
        abort(404)
    else: 
        user = {'id': data[0][0],'username': data[0][1], 'body': data[0][2],'tweet_time': data[0][3]}
    cur.close()
    conn.close()
    return jsonify(user) 


@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    """curl http://localhost:5000/api/v2/tweets/2"""
    return list_tweet(id)

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')
    
@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.route('/')      
def main():       
    return render_template('main.html') 

@app.route('/addname')     
def addname():    
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        # And then redirect the user to the main page       
        return redirect(url_for('main'))     
    else:       
        return render_template('addname.html', session=session)

@app.route('/clear')       
def clearsession():       # Clear the session       
    session.clear()       # Redirect the user to the main page       
    return redirect(url_for('main'))

@app.route('/set_cookie') 
def cookie_insertion(): 
    redirect_to_main = redirect('/') 
    response = current_app.make_response(redirect_to_main )   
    response.set_cookie('cookie_name',value='values') 
    return response 



if __name__ == "__main__":
    app.run()
    "app.run(host='0.0.0.0', port=5000, debug=True)"
