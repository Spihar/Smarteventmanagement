from flask import Flask, render_template, request, jsonify,session,url_for,redirect
#from pymongo import MongoClient
import os
from database import get_connection


app = Flask(__name__)
app.secret_key="hello"
app.config['UPLOAD_FOLDER']='static/uploads'

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select * from users where email =%s and password=%s",(email,password))
        user=cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            print(user)
            session['user'] = user[1]  # Store user info in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard
            #return "login sus"
        else:
            return render_template("loginPage.html", error="Invalid credentials")
            #return "login fail"
    return render_template("loginPage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        department = request.form.get("department")
        year = request.form.get("year")
        photo = request.files.get("photo")  # important: use request.files for file input

        # Save the uploaded photo
        photo_filename = photo.filename
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)

        # Save the data to DB
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, password, department, year, photo_path) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, department, year, photo_filename))
        conn.commit()
        cursor.close()
        conn.close()

        return "Signup successful!"  # or redirect to login or something

    return render_template("SignUp.html")


@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"<h1>Welcome, {session['user']}!</h1><p><a href='/logout'>Logout</a></p>"

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect(url_for(login))

@app.route("/orglogin", methods=["GET", "POST"])
def orglogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM organizers WHERE email = %s AND password = %s", (email, password))
        organizer = cursor.fetchone()
        cursor.close()
        conn.close()
        if organizer:
            session['organizer'] = organizer[1]
            return redirect(url_for('org_dashboard'))
        else:
            return render_template("orglogin.html", error="Invalid organizer credentials")
    return render_template("orglogin.html")

if __name__ == "__main__":
    app.run(debug=True)