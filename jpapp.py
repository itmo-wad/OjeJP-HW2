import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__, template_folder='templates')
app.config["MONGO_URI"] = "mongodb://localhost:27023/WAD"
app.secret_key= b'_johnson\n\isosec]/'

# Mongodb client
mongo = PyMongo()

# Mongodb collections
mongo.init_app(app)
users = mongo.db.users


@app.route('/')
def index():            #redirect to the main page
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():                        #redirect to the login page

    user_in_session = 'username' in session
    if user_in_session:
        # flash('Logged back in successfully', 'other')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if not username:
            flash('You have not provided a username', 'danger')
        elif not password:
            flash('You have not provided a password', 'danger')
        else:
            existing_user = users.find_one({'username': username})
            if not existing_user:
                flash('Wrong login or password', 'danger')
            if check_password_hash(existing_user['password'], password) == False:
                flash('Wrong login or password', 'danger')
            else:
                flash('Logged in successfully.', 'success')
                resp = make_response(redirect(url_for('profile')))
                session['username'] = username
                return resp

    return render_template('login.html')

@app.route('/profile', methods=('GET', 'POST'))
def profile():                                      #redirect to the profile page
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'username' in session:
        user = mongo.db.users.find_one({'username': session['username']})
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_in_session = 'username' in session
    if user_in_session:
        # flash('Logged back in successfully', 'success')
        return redirect(url_for('profile'))

    if request.method == 'POST':

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        location = request.form["location"]

        if not username:
            flash('You have not provided a username', 'danger')
        elif not password:
            flash('You have not provided a password', 'danger')
        else:
            existing_username = users.find_one({'username': username})
            if existing_username:
                flash('This username is already taken, please choose another one', 'danger')
                return redirect(url_for('signup'))

            encrypted_password = generate_password_hash(password)
            users.insert_one(
                {'username': username, 'password': encrypted_password,
                 'email': email, 'location':location})

            flash('New User created successfully.', 'success')
            resp = make_response(redirect(url_for('profile')))
            session['username'] = username
            return resp
    return render_template('signup.html')


@app.route('/pwdupdate', methods=('GET', 'POST'))
def password_update():                          #redirect to the profile page
    if 'username' not in session:
        flash('Session expired. Please reconnect.', 'danger')
        return redirect(url_for('login'))

    user_session = session['username']

    if request.method == "POST":
        password = request.form["new-password"]
        confirmation_password = request.form["confirm-password"]
        if not password or not confirmation_password:
            flash("No info entered", 'danger')
        elif password != confirmation_password:
            flash("Passwords do not match", 'danger')
        else:
            query = {"username": user_session}

            hashed_password = generate_password_hash(password)
            newvalues = {"$set": {"username": user_session, "password": hashed_password}}
            users.update_one(query, newvalues)
            flash("Password was just updated", 'success')
            return redirect(url_for('login'))

    return render_template("pwdupdate.html", name=user_session)


@app.route('/updateprofile', methods=('GET', 'POST'))
def update_profile():
    if 'username' not in session:
        flash('Session expired. Please reconnect.', 'danger')
        return redirect(url_for('login'))

    user_session = session['username']

    if request.method == "POST":

        username = request.form["name"]
        email = request.form["email"]
        location = request.form["location"]

        if not username or not username:
            flash("No info entered", 'danger')
        else:

            IMAGES_FOLDER = './static/images/'
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

            query = {"username": user_session}
            if request.files.__len__() > 0:
                image_data = request.files['file']
                filename = f'{user_session}{os.path.splitext(image_data.filename)[1]}'

                folder = os.path.abspath(IMAGES_FOLDER)
                path = os.path.join(folder, filename)
                os.makedirs(folder, exist_ok=True)

                image_data.save(path)

                mongo.db.users.update_one({'username': session['username']}, {"$set": {
                    'images_url': f'/static/images/{filename}',
                }})

                newvalues = {"$set": {"name": username, "email": email, "location":location,
                                      'images_url': f'/static/avatars/{filename}'}}
                users.update_one(query, newvalues)
            else:
                newvalues = {"$set": {"name": username, "email": email}}
                users.update_one(query, newvalues)

            flash("Profile was just updated", 'success')
            return redirect(url_for('login'))

    data = mongo.db.users.find_one(filter={"username": session['username']})
    return render_template("updateprofile.html", data=data)

@app.route('/logout', methods=['POST'])
def sign_out():                                 #function to clear sessionlogin
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="localhost",port=5001,debug=True)
