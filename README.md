<h1>🍴 Recipe Finder</h1>

This is the Recipe Finder web app built with Flask and the Edamam API.
It lets users search recipes by ingredients, view images, and save their favorites once logged in.

It’s simple, clean. Uses API integration, Flask routes, and database management using SQLAlchemy.


<h2>🚀 Features</h2>

🔍 Search for recipes using ingredients or keywords

❤️ Save your favorite recipes after logging in

👤 Create an account and manage your saved recipes

🧾 Stores all data using SQLAlchemy with SQLite

🖼️ Responsive layout with Bootstrap and Jinja templates



<h2>🧠 Tech Stack</h2>

Backend: Flask, SQLAlchemy
Frontend: HTML, CSS, Bootstrap, Jinja2
API: Edamam Recipe Search API
Database: SQLite (easy to switch to PostgreSQL)

<h2>🧩 Project Structure</h2>
recipe-finder/ <br>
│ <br>
├── static/                # CSS, images <br>
├── templates/           # HTML templates <br>
├── main.py               # Main Flask app, database <br>
└── README.md


<h2>⚙️ Setup</h2>

1. Clone the repo:
git clone https://github.com/yourusername/recipe-finder.git
cd recipe-finder


2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate     # on Windows: venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt


4. Add your .env file with:
APP_ID=your_app_id
API_KEY=your_app_key
SECRET_KEY=your_secret_key


5. Run the app:
flask run


6. Open your browser at
👉 http://127.0.0.1:5000


<h2>👨‍💻 Author</h2>
Luis Daniel Castro Ortiz
📍 Orlando, FL <br>
💼 GitHub: github.com/dancast835 | 💬 LinkedIn: https://www.linkedin.com/in/luisdanielcastro
