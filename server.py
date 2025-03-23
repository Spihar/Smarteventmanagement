

from flask import Flask, render_template, request, jsonify,session,url_for,redirect
#from pymongo import MongoClient
import pickle
import pandas as pd
import qrcode
import os
from confemail import sendemail
from database import get_connection


app = Flask(__name__)
app.secret_key="hello"
app.config['UPLOAD_FOLDER']='static/uploads'

@app.route("/register_event", methods=["GET","POST"])
def register_event():
    if request.method=="GET":
        email=session['user']
        sendemail(email)


@app.route("/org_dashboard")
def org_dashboard():
    if 'organizer' not in session:
        return redirect(url_for('orglogin'))

    return render_template("orgdashboard.html")



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
            session['user'] = user[2]  # Store user info in session
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
        qr = qrcode.make(name)
        qr_filename = f"{name}_qr.png"
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
        qr.save(qr_path)
        qr_url = url_for('static', filename=f'uploads/{qr_filename}')
        print("Dynamic QR Code URL:", qr_url)  # for testing
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, password, department, year, photo_path) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, department, year, qr_filename))
        conn.commit()
        cursor.close()
        conn.close()
        session['user']=email
        return redirect(url_for('dashboard'))

        #return f"Signup successful! <br> <a href='{qr_url}' target='_blank'>View your QR code</a>"

    return render_template("SignUp.html")


@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_email=session['user']
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select department from users where email=%s",(user_email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        return "user not found"

    user_dept=result[0]
    with open("event_recommendation_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("event_mlb.pkl", "rb") as f:
        mlb = pickle.load(f)

    all_events = mlb.classes_

    user_input=mlb.transform([user_dept])

    # Create dummy input for prediction

    test_df = pd.DataFrame(user_input, columns=all_events)
    predicted_proba = model.predict_proba(test_df)

    top_indices = predicted_proba[0].argsort()[::-1]
    recommended_events = [all_events[i] for i in top_indices[:6]]

    # Render dashboard.html with events
    return render_template("dashboard.html", events=recommended_events, user_dept=user_dept)



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
            session['organizer'] = organizer[1]  # Assuming this is the organizer name or ID
            return redirect(url_for('orgdashboard'))  # Match route name below
        else:
            return render_template("orglogin.html", error="Invalid organizer credentials")

    return render_template("orglogin.html")

@app.route("/orgdashboard")
def orgdashboard():
    if 'organizer' not in session:
        return redirect(url_for('orglogin'))  # Protect route
    return render_template("orgdashboard.html", organizer=session['organizer'])


@app.route("/events")
def all_events():
    with open("event_mlb.pkl", "rb") as f:
        mlb = pickle.load(f)

    all_events = list(mlb.classes_)  # Get all event names
    return render_template("all_events.html", events=all_events)

@app.route("/validate_qr", methods=["POST"])
def validate_qr():
    data = request.get_json()
    qr_data = data.get("qr_data")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE photo_path = %s", (qr_data,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": f"Welcome {user[0]}! QR Code Validated."})
    else:
        return jsonify({"message": "Invalid QR Code!"}), 400


if __name__ == "__main__":
    app.run(debug=True)