from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

#Edamam API
load_dotenv()
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

#api need this header, it is not in the documentation
header = {
    "Edamam-Account-User": "test",
}

app = Flask(__name__)

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

@app.route('/favorites')
def favorites():
    return render_template("favorites.html")

if __name__ == "__main__":
    app.run(debug=True)








