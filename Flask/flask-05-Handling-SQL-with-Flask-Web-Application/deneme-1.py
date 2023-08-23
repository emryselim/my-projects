from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# - configure required environmental variables for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./email.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120))

# Create the database tables
with app.app_context():
    db.create_all()

# - Write a function named `find_emails` which finds emails using keyword from the user table in the db,
# - and returns result as tuples `(name, email)`.
def find_emails(keyword):
    with app.app_context():
        user_emails = User.query.filter(User.username.ilike(f'%{keyword}%')).all()
        if not user_emails:
            user_emails = [("Not Found", "Not Found")]
        return user_emails

# - Write a function named `insert_email` which adds new email to users table the db.
def insert_email(name, email):
    with app.app_context():
        existing_user = User.query.filter_by(username=name).first()
        response = ''
        if len(name) == 0 or len(email) == 0:
            response = 'Username or email cannot be empty!!'
        elif not existing_user:
            new_user = User(username=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            response = f"User {name} and {email} have been added successfully"
        else:
            response = f"User {name} already exists"
        return response

# - Write a function named `emails` which finds email addresses by keyword using `GET` and `POST` methods,
# - using template files named `emails.html` given under `templates` folder
# - and assign to the static route of ('/')
@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_app_name = request.form['user_keyword']
        user_emails = find_emails(user_app_name)
        return render_template('emails.html', name_emails=user_emails, keyword=user_app_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)

# - Write a function named `add_email` which inserts new email to the database using `GET` and `POST` methods,
# - using template files named `add-email.html` given under `templates` folder
# - and assign to the static route of ('/add')
@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_app_name = request.form['username']
        user_app_email = request.form['useremail']
        result_app = insert_email(user_app_name, user_app_email)
        return render_template('add-email.html', result_html=result_app, show_result=True)
    else:
        return render_template('add-email.html', show_result=False)

# - Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__=='__main__':
    app.run(debug=True)
