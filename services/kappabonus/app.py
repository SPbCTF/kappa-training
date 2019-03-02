from flask import Flask,session,request, Response, redirect, jsonify, render_template
from passlib.hash import scrypt
from random import choices
from string import ascii_uppercase, digits
import mysql.connector
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from re import sub

config = {}
with open("config.ini", "r") as config_file:
    for line in config_file:
        key, value = line.split("=")
        config[key] = value.strip()

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
    return sub('[^a-zA-Z0-9-]','',string)


@app.route('/')
def mainpage():
    if not 'username' in session:
        return redirect("/login/")
    return redirect("/my/")


@app.route('/signup/', methods=['POST','GET'])
def register():
    if 'username' in session:
        return redirect("/my/")
    
    error = None
    if request.method == 'POST':
        content = request.form
        
        username = sanitize(request.form.get("username", ""))
        password = request.form.get("password", "")
        promocode = request.form.get("promocode", "")

        if username and password:
            cursor = conn.cursor()
            cursor.execute("select username from user where username=%s", (username, ))
            rows = cursor.rowcount
            cursor.fetchall()
            cursor.close()
            
            if rows == 0:
                try:
                    result = VIPKEY.encrypt(b64decode(promocode))
                except:
                    result = ""

                is_vip = result == session.get("challenge", None)
                
                conn.cursor().execute(
                    "insert into user (username, password, vip) values (%s, %s, %i)",
                    (username, scrypt.hash(password), is_vip)
                )

                return redirect("/login/")
            else:
                error = "User exists"
        else:
            error = "Fill more fields"

    token = ''.join(choices(ascii_uppercase + digits, k=16))
    session['challenge'] = VIPKEY.encrypt(token.encode('utf-8'), 0)[0]
    
    return render_template(
        'signup.html', 
        token=b64encode(session['challenge']).decode("utf-8"),
        error=error
    )


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect("/my/")
    
    error = None
    
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        cursor = conn.cursor()
        cursor.execute("select password, posted_flags from user where username=%s", (username, ))
        row = cursor.fetchone()
        cursor.close()
        
        if row is not None and scrypt.verify(password, row[0]):
            if row[1] < 10:
                session['username'] = username
                return redirect("/my/")
            else:
                error = "So much bad flags, you've banned"
        else:
            error = "Wrong login or password"
    return render_template(
        'login.html',
        error=error
    )


@app.route('/sell/', methods=['POST','GET'])
def sell():
    if 'username' not in session:
        return redirect("/login/")
    
    username = session["username"]    

    cursor = conn.cursor()
    cursor.execute("select vip from user where username=%s", (username, ))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        del session["username"]
        return redirect("/login/")

    vip = row[0]
    error = None

    if request.method == 'POST':
        cost = request.form.get("cost", "")
        if vip or len(cost) < 4:
            flag = request.form.get("flag", "")
            team = request.form.get("team", "")
        
            if flag and team in ["1", "2"] and cost > 0 and (vip or cost < 3):
                cursor = conn.cursor()
                cursor.execute('select balance, posted_flags from user where username=%s', (username, ))
                row = cursor.fetchone()
                cursor.close()
                balance, posted_flags = row
                
                if posted_flags >= 10:
                    del session["username"]
                    return redirect("/login/")
                
                team = "lcbc" if team == "2" else "kappa"

                conn.cursor().execute(
                    "update into user (balance, posted_flags) values (%i, %i) where username=%s",
                    (balance + int(price), posted + 1, username)
                )
                conn.cursor().execute(
                    # there is definitely no sql injection
                    "insert into {team} (flag, cost, username) values (%s, %i, %s)".format(team),
                    (flag, int(price), username)
                )

                return redirect("/my/")
            else:
                error = "Fill form correctly"
        else:
            error = "Won't buy such expensive flag!"
            
    return render_template(
        "sell.html",
        error=error
    )


@app.route('/buy/', methods=['GET'])
def buy():
    if username not in session:
        return redirect("/login/")
    
    cursor = conn.cursor()
    cursor.execute('select id, "kappa" as team, cost from kappa')
    flags = cursor.fetchall()
    cursor.close()
    return render_template("buy.html",flags=flags)

@app.route('/my/')
def my():
    if username not in session:
        return redirect("/login/")
    
    username = session["username"]
    
    cursor = conn.cursor()
    cursor.execute('select id, "kappa" as team, cost, flag from kappa where username=%s union select id, "lcbc" as team, cost, flag from lcbc where username=%s', (username, username))
    flags = cursor.fetchall()
    cursor.close()
    return render_template("index.html",flags=flags)


@app.route('/buyflag/<int:flag_id>', methods=['GET'])
def buy_flag(flag_id):
    if username not in session:
        return jsonify({"success": False, "reason": "login first"})
    username = session["username"]

    cursor = conn.cursor()
    cursor.execute("select balance from users where username=%s", (username, ))
    row = cursor.fetchone()
    balance = row[0]
    cursor.close()

    cursor = conn.cursor()
    cursor.execute("select flag, price from kappa where id=%i", (flag_id, ))
    row = cursor.fetchone()
    if row is None:
        return jsonify({"success": False, "reason": "no flag"})
    flag, price = row

    if price > balance:
        return jsonify({"success": False, "reason": "no money - no flags"})

    conn.cursor().execute("update into users (balance) values (%i) where username=%s", (balance - price, username))

    return jsonify({"success": True, "flag": flag})


if config["share_flags"] == "true":
    @app.after_request
    def sharing_with_buddies(response):
        response.headers["X-Share-Flags"] = "true"
        return response


@app.route('/ref/')
def ref():
    if username not in session:
        return redirect("/login/")
    
    return render_template("ref.html")


@app.route('/logout/')
def logout():
    del session["username"]
    
    return redirect('/login/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3377)

