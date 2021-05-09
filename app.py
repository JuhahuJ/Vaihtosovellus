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
    try:
        del session['not_admin_password']
    except KeyError:
        pass
    try:
        del session['user_already_exists']
    except KeyError:
        pass
    try:
        del session['current_area_id']
    except KeyError:
        pass
    try:
        del session['not_same_password']
    except KeyError:
        pass
    try:
        del session['incorrect_password']
    except KeyError:
        pass
    try:
        del session['incorrect_user']
    except KeyError:
        pass
    try:
        del session['too_short_username']
    except KeyError:
        pass
    try:
        del session['too_short_password']
    except KeyError:
        pass
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username= :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        session["incorrect_user"] = True
        session["incorrect_password"] = False
        return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            sql = "SELECT admin FROM users where username= :username"
            result = db.session.execute(sql, {"username":username}).fetchone()[0]
            if result == True:
                session["admin"] = True
            else:
                session["admin"] = False
            session["username"] = username
            return redirect("/go_areas")
        else:
            session["incorrect_password"] = True
            session["incorrect_user"] = False
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
    if len(username) < 3:
        session["too_short_username"] = True
        session["too_short_password"] = False
        session["not_same_password"] = False
        session["user_already_exists"] = False
        return redirect("/go_register")
    elif len(password) < 4:
        session["too_short_password"] = True
        session["too_short_username"] = False
        session["not_same_password"] = False
        session["user_already_exists"] = False
        return redirect("/go_register")
    else:
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
                session["too_short_username"] = False
                session["too_short_password"] = False
                return redirect("/go_register")
        else:
            session["user_already_exists"] = False
            session["not_same_password"] = True
            session["too_short_username"] = False
            session["too_short_password"] = False
            return redirect("/go_register")

@app.route("/register_admin",methods=["POST","GET"])
def register_admin():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    adminpassword = request.form["adminpassword"]
    sql = "SELECT password FROM adminpass ORDER BY id DESC"
    hash_value = db.session.execute(sql).fetchone()[0]
    if len(password) < 4:
        session["too_short_password"] = True
        session["not_same_password"] = False
        session["user_already_exists"] = False
        session["not_admin_password"] = False
        return redirect("/go_register_admin")
    else:
        if password == password2 and check_password_hash(hash_value, adminpassword):
            try:
                hash_value = generate_password_hash(password)
                sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, true)"
                db.session.execute(sql, {"username":username, "password":hash_value})
                db.session.commit()
                return redirect("/")
            except Exception:
                session["not_same_password"] = False
                session["user_already_exists"] = True
                session["not_admin_password"] = False
                session["too_short_password"] = False
                return redirect("/go_register_admin")
        elif password == password2 and adminpassword != check_password_hash(hash_value, adminpassword):
            session["user_already_exists"] = False
            session["not_same_password"] = False
            session["not_admin_password"] = True
            session["too_short_password"] = False
            return redirect("/go_register_admin")
        else:
            session["user_already_exists"] = False
            session["not_same_password"] = True
            session["not_admin_password"] = False
            session["too_short_password"] = False
            return redirect("/go_register_admin")

@app.route("/logout")
def logout():
    del session["username"]
    try:
        del session['current_request']
    except KeyError:
        pass
    try:
        del session['noarea']
    except KeyError:
        pass
    try:
        del session['admin']
    except KeyError:
        pass
    try:
        del session['area']
    except KeyError:
        pass
    try:
        del session['current_area_id']
    except KeyError:
        pass
    try:
        del session['too_short_areaname']
    except KeyError:
        pass
    try:
        del session['duplicate_request_title']
    except KeyError:
        pass
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
    if len(areaname) < 3:
        session["too_short_areaname"] = True
        return redirect("/create_area")
    else:
        sql = "INSERT INTO areas (area, request_amount) VALUES (:areaname, 0)"
        db.session.execute(sql, {"areaname":areaname})
        db.session.commit()
        return redirect("/go_areas")

@app.route("/go_areas", methods=["POST","GET"])
def go_areas():
    try:
        del session['duplicate_request_title']
    except KeyError:
        pass
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
    sql4 = "SELECT request_title FROM request WHERE request_title = :title"
    check = db.session.execute(sql4, {"title":title}).fetchone()
    if check is not None:
        session["duplicate_request_title"] = True
        return redirect("/go_create_request")
    else:
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
    return redirect("/go_back")

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

@app.route("/del_areas", methods=["POST"])
def del_areas():
    area = session["area"]
    area_id = session["current_area_id"]
    sql = "DELETE FROM requests WHERE area_id = :area_id"
    sql2 = "DELETE FROM request WHERE area_id = :area_id"
    sql3 = "DELETE FROM areas WHERE area = :area"
    db.session.execute(sql, {"area_id":area_id})
    db.session.execute(sql2, {"area_id":area_id})
    db.session.execute(sql3, {"area":area})
    db.session.commit()
    return redirect("/go_areas")

@app.route("/go_modify_request", methods=["POST"])
def go_modify_request():
    title = session["current_request"]
    area = session["area"]
    rdir = "SELECT id FROM areas WHERE area =:area"
    rdirection = db.session.execute(rdir, {"area":area}).fetchone()[0]
    sql = "SELECT * FROM request WHERE area_id =:rdirection AND request_title =:title"
    result = db.session.execute(sql, {"rdirection":rdirection, "title":title})
    requesta = result.fetchone()
    session["current_request"] = requesta.request_title
    return render_template("modify_request.html", requesta=requesta)

@app.route("/modify_request", methods=["POST"])
def modify_request():
    title = request.form['title']
    current_title = session["current_request"]
    need = request.form['need']
    offer = request.form['offer']
    contact = request.form['contact']
    area = session["area"]
    rdir = "SELECT id FROM areas WHERE area =:area"
    areaid = db.session.execute(rdir, {"area":area}).fetchone()[0]
    sql = "UPDATE request SET (request_title, need, offer, contact) = (:title, :need, :offer, :contact) WHERE request_title = :current_title AND area_id = :areaid"
    sql2 = "UPDATE requests SET request = :title WHERE request = :current_title AND area_id = :areaid"
    db.session.execute(sql, {"title":title, "need":need, "offer":offer, "contact":contact, "current_title":current_title, "areaid":areaid})
    db.session.execute(sql2, {"title":title, "current_title":current_title, "areaid":areaid})
    db.session.commit()
    return redirect("/go_back")

@app.route("/go_admin_menu")
def go_admin_menu():
    return render_template("/admin_menu.html")

@app.route("/change_admin_password", methods=["POST"])
def change_admin_password():
    password = request.form['password']
    password2 = request.form['password2']
    username = session["username"]
    if password == password2:
        passw = generate_password_hash(password)
        sql = "INSERT INTO adminpass (password, changedby) VALUES (:passw, :username)"
        db.session.execute(sql, {"passw":passw, "username":username})
        db.session.commit()
    return redirect("go_admin_menu")

@app.route("/reset_admin_password", methods=["POST"])
def reset_admin_password():
    sql = "DELETE FROM adminpass WHERE NOT changedby = ''"
    db.session.execute(sql)
    db.session.commit()
    return redirect("go_admin_menu")

@app.route("/delete_user", methods=["POST"])
def delete_user():
    user = request.form['usersss']
    sql = "DELETE FROM users WHERE username = :user"
    db.session.execute(sql, {"user":user})
    db.session.commit()
    return redirect("/show_userlist")

@app.route("/show_userlist", methods=["POST", "GET"])
def show_userlist():
    sql = db.session.execute("SELECT username FROM users WHERE admin = False")
    userlist = sql.fetchall()
    return render_template("/userlist.html", userlist=userlist)