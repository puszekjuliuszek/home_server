from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny_klucz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gender = db.Column(db.String(10))  # Dodanie pola płci
    birthdate = db.Column(db.Date)  # Dodanie pola daty urodzenia
    is_alive = db.Column(db.Boolean)  # Dodanie pola informacji o życiu
    deathdate = db.Column(db.Date)  # Dodanie pola daty śmierci

    father = db.relationship('User', remote_side=[id], foreign_keys=[father_id], backref='children_father',
                             uselist=False)
    mother = db.relationship('User', remote_side=[id], foreign_keys=[mother_id], backref='children_mother',
                             uselist=False)

    # Relacja między użytkownikami jako małżonkowie
    spouses = db.relationship('User', secondary='spouse_association',
                              primaryjoin='User.id==spouse_association.c.user_id',
                              secondaryjoin='User.id==spouse_association.c.spouse_id',
                              backref='spouse_of')

# Tabela asocjacyjna dla relacji małżonków
spouse_association = db.Table('spouse_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('spouse_id', db.Integer, db.ForeignKey('user.id')))

# Przykładowe widoki
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = User.query.all()  # Pobierz wszystkich użytkowników z bazy danych
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        father_id = request.form.get('father_id')  # Odczytaj ojca z formularza
        mother_id = request.form.get('mother_id')  # Odczytaj matkę z formularza
        gender = request.form['gender']
        is_alive = request.form['is_alive']

        is_alive = True if is_alive == 'yes' else False

        # Utwórz nowego użytkownika z ojcem i matką
        user = User(username=username, password=hashed_password, gender=gender, is_alive=is_alive)
        if father_id:
            user.father_id = int(father_id)
        if mother_id:
            user.mother_id = int(mother_id)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/concerts')
def concerts():
    return render_template('concerts.html')

@app.route('/photos')
def photos():
    image_list = ['prof2.jpg', 'prof3.jpg']

    return render_template('photos.html', image_list=image_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)