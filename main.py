from flask import Flask, render_template, request,redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Corrected key
db = SQLAlchemy(app)  # Corrected module name
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Added nullable=False
    password = db.Column(db.String(100), nullable=False)  # Added nullable=False

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Corrected hashing

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # logic for register

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name = name,email = email, password= password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # logic for login
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Call check_password on the user instance
            session['email'] = user.email
            session['name'] = user.name  # Store the name in the session

            return redirect('/dashboard')  # Corrected: return the redirect

        else:
            return render_template("login.html", message="Invalid User")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if session['name']:
        user = User.query.filter_by(email = session['email']).first()
        return render_template('dashboard.html', user = user)
    return redirect('/login')


@app.route('/logout')
def logout():
    # Clear the session
    session.pop('email', None)
    session.pop('name', None)

    # Redirect to the login page or homepage
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
