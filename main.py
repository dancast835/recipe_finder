from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        ingredient = request.form['ingredients']
        print(ingredient)
        return render_template("result.html")

@app.route('/favorites')
def favorites():
    return render_template("favorites.html")

if __name__ == "__main__":
    app.run(debug=True)

load_dotenv()
#Edamam API
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

params = {
    "type": "public",
    "q": "chicken",
    "app_id": APP_ID,
    "app_key": API_KEY
}

#api need this header, it is not in the documentation
header = {
    "Edamam-Account-User": "test",
}

response = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params, headers=header)
data = response.json()

for recipe in data["hits"][:10]:   # Print first 10 recipes
    print(recipe["recipe"]["label"])
    print(recipe["recipe"]["image"])
    print(recipe["recipe"]["url"])


