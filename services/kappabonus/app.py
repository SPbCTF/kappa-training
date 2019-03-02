from flask import Flask,session,request, Response, redirect, jsonify, render_template
from passlib.hash import scrypt
from random import choices
from string import ascii_uppercase, digits
import mysql.connector
from base64 import b64encode
from Crypto.PublicKey import RSA
from re import sub

config = {}
with open("config.ini", "r") as config_file:
    for line in config_file:
        key, value = line.split("=")
        config[key] = value

app = Flask(__name__)
conn=mysql.connector.connect(
    host=config["host"],
    database=config["dbname"],
    user=config["user"],
    password=config["pass"]
)

app.secret_key = b'\xa1%\xca\xff\n1\xe4N\xa7\xd2\xff\x01i*\xae\xee\xf2\xc3\xc7q\xa1P}>{>\t\xac\xea\x07G<'

VIP_PUBKEY=b'0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xaa\x08\xac\x83kx\xec\xfd\xc0Iol\xa3Y\xd6\xba\x85n7\x08\xef<\x01\xa1 \xce5.\xa1\x9a<t\xf3Z\x88\x18\xaf\xf9\x05\xb1\xa9\x14J\xaaB\xf1\xc5&LN\x94\x1c\xec\x0e:\x80\xf0?\x1d\x98Ih_\x1c\x1b\x1f\xbbY\x91\xbaA\xe5\x08\xbcL,f\xe28>\x0c\xf9\x83\xc6\xb8Us\xc9~}n\xe7c\x94#\xf4\xa7G\xd7F2h\rn\x1cO\x1a\tv\x03rW\xaa\x07\xad@:\xc4%\x1c\xb9Ec~\xe9\xde&\xed\x86\\KL\xb0\xe3\xac\xd8\xfddgG\xe4\xec,\xb4\xef\x0b\x11\x81\xe1\xb4l;\xf1\xdeH\xf6!\x9c\x03\xf2\xa4\xb0\xc0\xbf\n\xc7\xc4\x99\t\xdbW\xa4\\!\xab\xc3_\x14Y\x05\xc1h,\xac35\x16\xc0\xb2\xf9\xdd\x15\x1e\xb0\x14\xc1\x0b^\xf1\xf8\x03\xbb\xf72\x1b\xcf,I|\xfdq\x8cg@\xbd\xee\x05\xb5}\xfa\xd7\xc7\xb4\x85\\1>\xce+\xfd\xc4\x8f\xcc\xba\xb1\x12hj\xf1\x1b\xb7\xc0\xf1\x04\xc6\xfc\x8e]?\'X\xe4\x89F\xad\xb7\x02\x03\x01\x00\x01'

VIPKEY=RSA.importKey(VIP_PUBKEY)

def sanitize(string):
    return sub('[^a-zA-Z\d=-]','',string)

@app.route('/')
def mainpage():
    if not 'username' in session:
        return redirect("/login/", code=301)
    return redirect("/my/", code=301)

@app.route('/signup/', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        content = request.form
        (username, password, response) = (content['username'], content['password'], content['promocode'])
        cursor = conn.cursor()
        cursor.execute("insert into users(username,password,vip) values (%s,%s,%i)",(sanitize(username),scrypt.hash(password),session['challenge'] == response))
        return redirect('/login', code=301)
    else:
        if not 'challenge' in session:
            session['challenge']=''.join(choices(ascii_uppercase + digits, k=16))
        return render_template("signup.html",token=b64encode(VIPKEY.encrypt(session['challenge'].encode('utf-8'))))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        content = request.form
        (username,password)=(content['username'],content['password'])
        cursor=conn.cursor()
        dbdata=cursor.execute("select password,vip,posted_flags from users where username=%s",(username))
        if(scrypt.verify(password,dbdata['password'])):
            if (not session['vip']) and dbdata['posted_flags']>=10:
                return jsonify({'error': "Ваш аккаунт заблокирован за злоупотребление системой"})
            session['username']=username
            session['vip']=dbdata['vip']
        else:
            return jsonify({'error': "Ваш аккаунт заблокирован за злоупотребление системой"})
    return Response(status=200)

@app.route('/sell/', methods=['POST','GET'])
def sell():
    if request.method == 'POST':
        content = request.form
        (flag,price,team)=(content['flag'],float(['cost']),content['team'])
        if price < 0:
            return Response(status=400)
        cursor=conn.cursor()
        username=session['username']
        dbdata = cursor.execute("select balance, posted_flags from users where username=%s", (username))
        balance=dbdata['balance']
        posted = dbdata['posted_flags']
        if not session['vip']:
            if len(content['cost'])>3:
                return Response(status=400)
            if posted>=10:
                session.clear()
                return redirect('/login/', code=301)
        if team==2:
            team="lcbc"
        else:
            team="kappa"
        cursor.execute(f"insert into {team}(flag,cost,username) values(%s,%i,%s)",(flag,int(price),username))
        cursor.execute("update into users(balance,posted_flags) values(%i,%i) where username=%s",(balance+price,posted+1,username))
    return Response(status=200)

@app.route('/buy/', methods=['GET'])
def buy():
    cursor = conn.cursor()
    flags = cursor.execute('select id, "kappa" as team, cost from kappa union select id, "lcbc" as team, cost from lcbc')
    return render_template("buy.html",flags=flags)

@app.route('/my/')
def my():
    cursor = conn.cursor()
    flags = cursor.execute('select id, "kappa" as team, cost, flag from kappa union select id, "lcbc" as team, cost, flag from lcbc')
    return render_template("index.html",flags=flags)


@app.route('/buyflag/<int:flag_id>', methods=['GET'])
def buy_flag(flag_id):
    cursor = conn.cursor()
    username = session['username']
    dbdata = cursor.execute("select balance from users where username=%s", (username))
    balance = dbdata['balance']
    dbdata = cursor.execute("select flag,price from kappa where id=%i", (flag_id))
    price = dbdata['price']
    flag = dbdata['flag']
    if (balance - price) < 0:
        return jsonify({'success': False, 'reason': "Недостаточно средств"})
    cursor.execute("update into users(balance) values(%i) where username=%s", (balance - price, username))
    return jsonify({'success': True, 'flag': flag})

if config["share_flags"] == "true":
    @app.after_request
    def sharing_with_buddies(response):
        response.headers["X-Share-Flags"] = "true"
        return response

@app.route('/ref/')
def ref():
    return render_template("ref.html")

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/', code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3377)
