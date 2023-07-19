from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
# config database test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# add secret key
app.config['SECRET_KEY'] = 'thisissecret'

# load login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# initialize database
db = SQLAlchemy(app)

# create user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

# create login loader
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# create login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        email = request.form['email']
        # check if user exists
        user = User.query.filter_by(name=user, email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return '<h1>Invalid username or password</h1>'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)
# route from dashboard to logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# abouot route 
@app.route('/about')
def about():
    return """<h1>about page</h1>"""



# create helper function for adding users
def add_user(name, email):
    my_user = User(name=name, email=email)
    db.session.add(my_user)
    db.session.commit()

# collect data from form and add to database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user = request.form['name']
        email = request.form['email']
        add_user(user, email)
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, debug=True)
