from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

#Edamam API
load_dotenv()
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

#api need this header, it is not in the documentation
header = {
    "Edamam-Account-User": "test",
}



#database for favorites recipe
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)       #this is to set up flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

db.init_app(app)

class User(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str]
    url: Mapped[str]
    image: Mapped[str]


@app.route('/')
def home():
    return render_template("index.html")

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

        #api call
        response = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params, headers=header)
        data = response.json()

        label = []
        url = []
        image = []

        for recipe in data["hits"][:5]:  # Print first 5 recipes
            label.append(recipe["recipe"]["label"])
            image.append(recipe["recipe"]["image"])
            url.append(recipe["recipe"]["url"])

        recipes = zip(label, url, image)    #zip function to combine lists into tuples to loop all at the same time

        return render_template("result.html", recipes=recipes)

@app.route('/add_favorites', methods=['GET', 'POST'])
def add_favorites():
    if request.method == 'POST':
        new_favorite = User(
            label=request.form['label'],
            url=request.form['url'],
            image=request.form['image']
        )
        db.session.add(new_favorite)
        db.session.commit()

    return "<h1>Favorite Added</h1>"



@app.route('/random')
def random():
    params = {
        "type": "public",
        "q": "any",
        "random": True,
        "app_id": APP_ID,
        "app_key": API_KEY
    }

    # api call
    response = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params, headers=header)
    data = response.json()

    label = []
    url = []
    image = []

    for recipe in data["hits"][:5]:  # Print first 5 recipes
        label.append(recipe["recipe"]["label"])
        image.append(recipe["recipe"]["image"])
        url.append(recipe["recipe"]["url"])

    recipes = zip(label, url, image)  # zip function to combine lists into tuples to loop all at the same time

    return render_template("random.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)

