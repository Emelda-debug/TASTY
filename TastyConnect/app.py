import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from create_table import RecipeTable, engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

# Link the RecipeTable class to the database engine
RecipeTable.metadata.create_all(engine)

# Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Recipe {self.title}>'

# EDAMAM API configuration
EDAMAM_API_URL = 'https://api.edamam.com/doc/open-api/recipe-search-v2.json'
EDAMAM_APP_ID = 'd5bc01db'
EDAMAM_API_KEY = '7cb36906dd09adf1ac5dd13da5f09ae0'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        
        # Make a request to the EDAMAM API to retrieve recipe data
        response = requests.get(
            EDAMAM_API_URL,
            params={'q': query, 'app_id': EDAMAM_APP_ID, 'app_key': EDAMAM_API_KEY}
        )
        
        if response.status_code == 200:
            data = response.json()
            recipes = data.get('hits', [])
            return render_template('results.html', recipes=recipes)
    
    return render_template('search.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)