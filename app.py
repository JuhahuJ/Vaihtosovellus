from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            result = db.session.execute("SELECT area, request_amount FROM areas")
            result2 = db.session.execute("SELECT area FROM areas")
            areas = result2.fetchall()
            arealist = []
            for area in areas:
                arealist.append(area)
            areass = result.fetchall()
            session["username"] = username
            return render_template("areas.html", areass=areass, areas=arealist)
        else:
            return redirect("/")

@app.route("/register",methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,false)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/inarea", methods=["POST","GET"])
def inarea():
    direction = request.form['arean']
    direction = direction.replace("'","")
    direction = direction.replace(",","")
    direction = direction.replace("(","")
    direction = direction.replace(")","")
    rdir = "SELECT id FROM areas WHERE area =:direction"
    rdirection = db.session.execute(rdir, {"direction":direction}).fetchone()[0]
    sql = "SELECT request FROM requests WHERE area_id =:rdirection"
    result = db.session.execute(sql, {"rdirection":rdirection})
    area = result.fetchall()
    return render_template("area.html", area=area)

@app.route("/create_area", methods=["POST","GET"])
def create_area():
    return render_template("create_area.html")

@app.route("/creating_area", methods=["POST","GET"])
def creating_area():
    areaname = request.form['name_of_area']
    sql = "INSERT INTO areas (area, request_amount) VALUES (:areaname, 0)"
    db.session.execute(sql, {"areaname":areaname})
    db.session.commit()
    sql2 = db.session.execute("SELECT area, request_amount FROM areas")
    sql3 = db.session.execute("SELECT area FROM areas")
    areas = sql3.fetchall()
    arealist = []
    for area in areas:
        arealist.append(area)
    areass = sql2.fetchall()
    return render_template("areas.html", areass=areass, areas=arealist)