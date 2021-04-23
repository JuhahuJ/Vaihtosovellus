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
            session["username"] = username
            return redirect("/go_areas")
        else:
            return redirect("/")

@app.route("/go_register")
def go_register():
    return render_template("register.html")

@app.route("/register",methods=["POST","GET"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password == password2:
        try:
            hash_value = generate_password_hash(password)
            sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,false)"
            db.session.execute(sql, {"username":username,"password":hash_value})
            db.session.commit()
            del session["not_same_password"]
            del session["user_already_exists"]
            return redirect("/")
        except Exception:
            session["user_already_exists"] = True
            return redirect("/go_register")
    else:
        session["not_same_password"] = True
        return redirect("/go_register")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/inarea", methods=["POST","GET"])
def inarea():
    direction = request.form['arean']
    rdir = "SELECT id FROM areas WHERE area =:direction"
    rdirection = db.session.execute(rdir, {"direction":direction}).fetchone()[0]
    sql = "SELECT request FROM requests WHERE area_id =:rdirection"
    result = db.session.execute(sql, {"rdirection":rdirection})
    areas = result.fetchall()
    return render_template("area.html", areas=areas)

@app.route("/create_area", methods=["POST","GET"])
def create_area():
    return render_template("create_area.html")

@app.route("/creating_area", methods=["POST","GET"])
def creating_area():
    areaname = request.form['name_of_area']
    sql = "INSERT INTO areas (area, request_amount) VALUES (:areaname, 0)"
    db.session.execute(sql, {"areaname":areaname})
    db.session.commit()
    return redirect("/go_areas")

@app.route("/go_areas", methods=["POST","GET"])
def go_areas():
    sql = db.session.execute("SELECT area, request_amount FROM areas")
    areass = sql.fetchall()
    return render_template("areas.html", areass=areass)
