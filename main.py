import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.exc import IntegrityError

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
app.secret_key = 'your_secret_key'

user_verified = False

#------------------------------------------------ Database setup ------------------------------------------------#
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipes.db"
db.init_app(app)

#set up for a one-to-many relationship between users and their favorite recipes
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)

    favorite: Mapped[list["Favorite"]] = relationship()

class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str]
    url: Mapped[str]
    image: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

with app.app_context():
    db.create_all()


#------------------------------------------------- Routes ------------------------------------------------#
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            global user_verified
            user_verified = True
            session['username'] = username
            return redirect(url_for("favorites"))
        else:
            flash("Username not found. Please sign up first.")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    global user_verified
    user_verified = False
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        new_user = User(
            username=request.form['new user']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists. Please choose a different one.")
            return render_template("login.html")
        else:
            flash("Signup successful! Please log in.")
            return render_template("login.html")

@app.route("/favorites")
def favorites():
    if 'username' not in session:
        return render_template("login.html")

    else:
        user = User.query.filter_by(username=session['username']).first()

        if user:
            user_favorites = Favorite.query.filter_by(user_id=user.id).all()
            fave_id = [fav.id for fav in user_favorites]
            label = [fav.label for fav in user_favorites]
            url = [fav.url for fav in user_favorites]
            image = [fav.image for fav in user_favorites]

            recipes = zip(fave_id, label, url, image)
            return render_template("favorites.html", recipes=recipes)


@app.route("/add_favorites", methods=["GET", "POST"])
def add_favorites():
    if request.method == "POST":
        try:
            user = User.query.filter_by(username=session['username']).first()

            if user:
                new_favorite = Favorite(
                    label=request.form['label'],
                    url=request.form['url'],
                    image=request.form['image'],
                    user_id=user.id
                )

                db.session.add(new_favorite)
                db.session.commit()
                flash("Recipe added to favorites!")
        except KeyError:
            db.session.rollback()
            flash("You must be logged in to save favorites.")

        return redirect(url_for("favorites"))


@app.route("/favorites/<int:favorite_id>/remove", methods=["GET", "POST"])
def remove_favorite(favorite_id):
    if request.method == "POST":
        user = User.query.filter_by(username=session['username']).first()
        fav = Favorite.query.filter_by(id=favorite_id, user_id=user.id).first()

        db.session.delete(fav)
        db.session.commit()
        #flash("Recipe removed from favorites!")
        return redirect(url_for("favorites"))



@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
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

        for recipe in data['hits'][:20]:
            label.append(recipe['recipe']['label'])
            image.append(recipe['recipe']['image'])
            url.append(recipe['recipe']['url'])

        recipes = zip(label, url, image)    #zip function to combine lists into tuples to loop all at the same time in html file

        return render_template("result.html", recipes=recipes)

#TODO: create a feature to let user quickly search for recipes under 20 or 10 mins of preparation time.
@app.route("/quick_cook")
def quick_cook():
    pass

@app.route("/random")
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

    for recipe in data['hits'][:20]:
        label.append(recipe['recipe']['label'])
        image.append(recipe['recipe']['image'])
        url.append(recipe['recipe']['url'])

    recipes = zip(label, url, image)  # zip function to combine lists into tuples to loop all at the same time

    return render_template("random.html", recipes=recipes)


if __name__ == "__main__":
    app.run()