from flask import Flask, redirect, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Recipe(db.Model):
    __tablename__ = "recipies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Recipe" + str(self.id)


@app.route("/")
def default():
    recipe_count = Recipe.query.count()
    return render_template("index.html", num_recipes=recipe_count)

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    if request.method == "POST":
        recipe_title = request.form["title"]
        recipe_description = request.form["description"]
        recipe_author = request.form["author"]
        new_recipe = Recipe(title=recipe_title, description=recipe_description, author=recipe_author)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect("/recipes")
    else:
        all_recipes = Recipe.query.all()
        return render_template('recipes.html', recipes=all_recipes)
    
@app.route("/recipe/new/", methods=["POST", "GET"])
def new_recipe():
    if request.method == "POST":
        recipe_title = request.form["title"]
        recipe_description = request.form["description"]
        recipe_author = request.form["author"]
        #recipe_category = request.form["category"]
        new_recipe = Recipe(title=recipe_title, description=recipe_description, author=recipe_author)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect("/recipe/new")
    else:
        return render_template("new_recipe.html")

@app.route("/recipes/edit/<int:id>/", methods=["GET", "POST"])
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST":
        recipe_title = request.form["title"]
        recipe_description = request.form["description"]
        recipe_author = request.form["author"]
        #recipe_category = request.form["category"]
        db.session.commit()
        return redirect("/recipes/edit/")
    else:
        return render_template("edit.html", recipe=recipe)

@app.route("/recipes/delete/<int:id>/")
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect("/recipes")

@app.route("/h/<int:num>")
def num(num):
    return f"Your number is {num}"

@app.route("/hello/<string:name>/")
def hello(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)


