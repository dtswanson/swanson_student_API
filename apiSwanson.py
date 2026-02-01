from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="USERNAME",
    password="PASSWORD",
    hostname="USERNAME.mysql.eu.pythonanywhere-services.com",
    databasename="USERNAME$default",
)
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the tblRecipes model
class Recipe(db.Model):
    __tablename__ = "tblRecipes"
    RecipeID = db.Column(db.Integer, primary_key=True)
    RecipeName = db.Column(db.String(255), nullable=False)
    votes = db.relationship('Vote', backref='recipe', lazy=True)

# Define the tblVotes model
class Vote(db.Model):
    __tablename__ = "tblVotes"
    VoteID = db.Column(db.Integer, primary_key=True)
    RecipeID = db.Column(db.Integer, db.ForeignKey('tblRecipes.RecipeID'), nullable=False)
    Upvotes = db.Column(db.Integer, default=0)
    Downvotes = db.Column(db.Integer, default=0)

@app.route("/", methods=["GET"])
def index():
    recipes = Recipe.query.all()  # Fetch all recipes
    return render_template("main_page.html", recipes=recipes)

@app.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
    recipes_data = [
        {
            "RecipeID": recipe.RecipeID,
            "RecipeName": recipe.RecipeName,
            "Upvotes": recipe.votes[0].Upvotes if recipe.votes else 0,
            "Downvotes": recipe.votes[0].Downvotes if recipe.votes else 0
        }
        for recipe in recipes
    ]
    return jsonify(recipes_data)

# Create a new recipe
@app.route("/add", methods=["POST"])
def add_recipe():
    for key in request.form:
        if key.startswith("recipe_name_"):
            recipe_name = request.form[key]
            if recipe_name:
                new_recipe = Recipe(RecipeName=recipe_name)
                db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('index'))

# Update a recipe
@app.route("/update/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Fetch the recipe or return 404
    recipe.RecipeName = request.form["recipe_name"]
    db.session.commit()
    return redirect(url_for('index'))

# Delete a recipe
@app.route("/delete/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Fetch the recipe or return 404
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

# Upvote a recipe
@app.route("/upvote/<int:recipe_id>", methods=["POST"])
def upvote_recipe(recipe_id):
    vote = Vote.query.filter_by(RecipeID=recipe_id).first()
    if not vote:
        vote = Vote(RecipeID=recipe_id, Upvotes=1, Downvotes=0)
        db.session.add(vote)
    else:
        vote.Upvotes += 1
    db.session.commit()
    return redirect(url_for('index'))

# Downvote a recipe
@app.route("/downvote/<int:recipe_id>", methods=["POST"])
def downvote_recipe(recipe_id):
    vote = Vote.query.filter_by(RecipeID=recipe_id).first()
    if not vote:
        vote = Vote(RecipeID=recipe_id, Upvotes=0, Downvotes=1)
        db.session.add(vote)
    else:
        vote.Downvotes += 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()