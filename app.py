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
    session["user_already_exists"] = False
    session["not_same_password"] = False
    session["not_admin_password"] = False
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

@app.route("/go_register_admin")
def go_register_admin():
    return render_template("register_admin.html")

@app.route("/register",methods=["POST","GET"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password == password2:
        try:
            hash_value = generate_password_hash(password)
            sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, false)"
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/")
        except Exception:
            session["not_same_password"] = False
            session["user_already_exists"] = True
            return redirect("/go_register")
    else:
        session["user_already_exists"] = False
        session["not_same_password"] = True
        return redirect("/go_register")

@app.route("/register_admin",methods=["POST","GET"])
def register_admin():
    correctadminpassword = "abc123"
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    adminpassword = request.form["adminpassword"]
    if password == password2 and adminpassword == correctadminpassword:
        try:
            hash_value = generate_password_hash(password)
            sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, true)"
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/")
        except Exception:
            session["not_same_password"] = False
            session["user_already_exists"] = True
            session["not_admin_password"] = False # poista nämä ylimääräiset
            return redirect("/go_register_admin")
    elif password == password2 and adminpassword != correctadminpassword:
        session["user_already_exists"] = False
        session["not_same_password"] = False
        session["not_admin_password"] = True
        return redirect("/go_register_admin")
    else:
        session["user_already_exists"] = False
        session["not_same_password"] = True
        session["not_admin_password"] = False
        return redirect("/go_register_admin")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/inarea", methods=["POST","GET"])
def inarea():
    direction = request.form['arean']
    session["area"] = direction
    rdir = "SELECT id FROM areas WHERE area =:direction"
    rdirection = db.session.execute(rdir, {"direction":direction}).fetchone()[0]
    sql = "SELECT request FROM requests WHERE area_id =:rdirection"
    result = db.session.execute(sql, {"rdirection":rdirection})
    areas = result.fetchall()
    session["current_area_id"] = rdirection
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
    del session["not_same_password"]
    del session["user_already_exists"]
    del session["not_admin_password"]
    session["area"] = "no_area_chosen"
    del session["area"]
    sql = db.session.execute("SELECT area, request_amount FROM areas")
    areass = sql.fetchall()
    return render_template("areas.html", areass=areass)

@app.route("/app_request", methods=["POST","GET"])
def app_request():
    title = request.form['request']
    sarea = session["area"]
    rdir = "SELECT id FROM areas WHERE area =:sarea"
    rdirection = db.session.execute(rdir, {"sarea":sarea}).fetchone()[0]
    sql = "SELECT * FROM request WHERE area_id =:rdirection AND request_title =:title"
    result = db.session.execute(sql, {"rdirection":rdirection, "title":title})
    requesta = result.fetchone()
    session["current_request"] = requesta.request_title
    return render_template("request.html", requesta=requesta)

@app.route("/create_request", methods=["POST", "GET"])
def create_request():
    title = request.form['title']
    need = request.form['need']
    offer = request.form['offer']
    contact = request.form['contact']
    postedby = session["username"]
    area = session["area"]
    rdir = "SELECT id FROM areas WHERE area =:area"
    areaid = db.session.execute(rdir, {"area":area}).fetchone()[0]
    sql = "INSERT INTO request (request_title, need, offer, contact, postedby, area_id) VALUES (:title, :need, :offer, :contact, :postedby, :areaid)"
    sql2 = "INSERT INTO requests (request, area_id) VALUES (:title, :areaid)"
    sql3 = "UPDATE areas SET request_amount = (request_amount+1) WHERE area =:area"
    db.session.execute(sql3, {"area":area})
    db.session.execute(sql2, {"title":title, "areaid":areaid})
    db.session.execute(sql, {"title":title, "need":need, "offer":offer, "contact":contact, "postedby":postedby, "areaid":areaid})
    db.session.commit()
    return redirect("/go_areas")

@app.route("/go_create_request")
def go_create_request():
    return render_template("create_request.html")

@app.route("/del_request", methods=["POST"])
def del_request():
    current_request = session["current_request"]
    area = session["area"]
    area_id = session["current_area_id"]
    sql = "DELETE FROM requests WHERE request = :current_request AND area_id = :area_id"
    sql2 = "UPDATE areas SET request_amount = (request_amount-1) WHERE area =:area"
    sql3 = "DELETE FROM request WHERE request_title = :current_request AND area_id = :area_id"
    db.session.execute(sql2, {"area":area})
    db.session.execute(sql, {"current_request":current_request, "area_id":area_id})
    db.session.execute(sql3, {"current_request":current_request, "area_id":area_id})
    db.session.commit()
    del session["current_request"]
    del session["current_request_id"]
    return redirect("/go_areas")

@app.route("/go_back")
def go_back():
    direction = session["area"]
    rdir = "SELECT id FROM areas WHERE area =:direction"
    rdirection = db.session.execute(rdir, {"direction":direction}).fetchone()[0]
    sql = "SELECT request FROM requests WHERE area_id =:rdirection"
    result = db.session.execute(sql, {"rdirection":rdirection})
    areas = result.fetchall()
    session["current_area_id"] = rdirection
    return render_template("area.html", areas=areas)