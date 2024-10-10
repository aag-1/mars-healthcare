from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Routes
@app.route('/')
def ghar():
    """Render the home page."""
    return render_template('index.html')

@app.route("/hospitalfind")
def hospitalfinding():
    return render_template("hospitalfind.html")

@app.route("/doc_login")
def doctors_login():
    return render_template("login.html")

@app.route("/consultation")
def consultation():
    """Render the symptoms page."""
    return render_template('symptoms.html')

@app.route("/doctorinterface")
def doctor12():
    """Render the doctor interface page."""
    return render_template('doctor.html')

@app.route('/analyze_symptoms', methods=['POST'])
def analyze_symptoms():
    return render_template("health_results.html")
    """Analyze symptoms and render results."""
    symptoms = request.form.get('symptoms', '')

@app.route("/docinterface")
def docinterface():
    return render_template("docinterface.html")
    






#----login method----

login_manager = LoginManager(app)
login_manager.login_view = 'login'

users = {}


class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            users[username] = User(username, hashed_password)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)