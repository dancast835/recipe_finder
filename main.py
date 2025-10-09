import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


#------------------------------------------------- Variables -----------------------------------------------#
#API Edamam
load_dotenv()
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

#api needs this header, it is not in the documentation
header = {
    "Edamam-Account-User": "test",
}


#initialize flask
app = Flask(__name__)
app.secret_key = "Cachapaconqueso"

user_verified = False

#------------------------------------------------ Database setup ------------------------------------------------#
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    favorites: Mapped[list["Favorite"]] = db.relationship(back_populates="user")

class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str]
    url: Mapped[str]
    image: Mapped[str]

    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    user: Mapped["User"] = db.relationship(back_populates="favorites")

with app.app_context():
    db.create_all()

#------------------------------------------------- Routes ------------------------------------------------#
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        user = User.query.filter_by(username=username).first()
        if user:
            global user_verified
            user_verified = True
            return render_template("favorites.html")
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    global user_verified
    user_verified = False
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(
            username=request.form['new user']
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")

#TODO: make it to if user is in session the link will take directly to favorites page
@app.route('/favorites')
def favorites():
    if 'username' in session:
        return render_template("favorites.html")
    elif not user_verified:
        return render_template("login.html")

    return render_template("favorites.html")


@app.route('/add_favorites', methods=['GET', 'POST'])
def add_favorites():
    if request.method == 'POST':
        new_favorite = Favorite(
            label=request.form['label'],
            url=request.form['url'],
            image=request.form['image']
        )
        db.session.add(new_favorite)
        db.session.commit()

    return "<h1>Favorite Added</h1>"


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        ingredient = request.form['ingredients']

        params = {
            "type": "public",
            "q": ingredient,
            "app_id": APP_ID,
            "app_key": API_KEY
        }

        label = []
        url = []
        image = []

        #api call for recipe search
        response = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params, headers=header)
        data = response.json()

        for recipe in data["hits"][:5]:  # Print first 5 recipes
            label.append(recipe["recipe"]["label"])
            image.append(recipe["recipe"]["image"])
            url.append(recipe["recipe"]["url"])

        recipes = zip(label, url, image)    #zip function to combine lists into tuples to loop all at the same time in html file

        return render_template("result.html", recipes=recipes)

@app.route('/random')
def random():
    params = {
        "type": "public",
        "q": "any",
        "random": True,
        "app_id": APP_ID,
        "app_key": API_KEY
    }

    label = []
    url = []
    image = []

    # api call for random recipe
    response = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params, headers=header)
    data = response.json()

    for recipe in data["hits"][:5]:  # Print first 5 recipes
        label.append(recipe["recipe"]["label"])
        image.append(recipe["recipe"]["image"])
        url.append(recipe["recipe"]["url"])

    recipes = zip(label, url, image)  # zip function to combine lists into tuples to loop all at the same time

    return render_template("random.html", recipes=recipes)



if __name__ == "__main__":
    app.run(debug=True)