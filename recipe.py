from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from models import get_db, Recipe, Comment

recipe_blueprint = Blueprint('recipe', __name__)

@recipe_blueprint.route('/')
def recipes():
    db = next(get_db())  # Получаем сессию
    all_recipes = db.query(Recipe).all()  # Запрос всех рецептов
    return render_template('recipes.html', recipes=all_recipes)


@recipe_blueprint.route('/<int:recipe_id>')
def recipe_detail(recipe_id):
    db = next(get_db())
    recipe = db.query(Recipe).get(recipe_id)
    comments = db.query(Comment).filter_by(recipe_id=recipe_id).all()
    return render_template('recipe_detail.html', recipe=recipe, comments=comments)


@recipe_blueprint.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # Проверка и сохранение загруженного изображения
        image_path = None
        image = request.files.get('file')
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('static/uploads', filename)
            image.save(image_path)

        db = next(get_db())
        new_recipe = Recipe(title=title, description=description, image_path=image_path)
        db.add(new_recipe)
        db.commit()

        flash('Recipe added successfully!')
        return redirect(url_for('recipe.recipes'))
    return render_template('add_recipe.html')


@recipe_blueprint.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    db = next(get_db())
    recipe = db.query(Recipe).get(recipe_id)
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        db.commit()

        flash('Recipe updated successfully!')
        return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))
    return render_template('edit_recipe.html', recipe=recipe)


@recipe_blueprint.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    db = next(get_db())
    recipe = db.query(Recipe).get(recipe_id)
    db.delete(recipe)
    db.commit()

    flash('Recipe deleted successfully!')
    return redirect(url_for('recipe.recipes'))


@recipe_blueprint.route('/<int:recipe_id>/comment', methods=['POST'])
def add_comment(recipe_id):
    if 'user_id' not in session:
        flash('You need to be logged in to comment!')
        return redirect(url_for('auth.login'))

    content = request.form['content']
    user_id = session['user_id']

    # Optional file upload
    image = request.files.get('image')
    image_path = None
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join('static/uploads', filename)
        image.save(image_path)

    db = next(get_db())
    new_comment = Comment(content=content, user_id=user_id, recipe_id=recipe_id, image_path=image_path)
    db.add(new_comment)
    db.commit()

    flash('Comment added successfully!')
    return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))


@recipe_blueprint.route('/<int:recipe_id>/comments')
def view_comments(recipe_id):
    db = next(get_db())
    recipe = db.query(Recipe).get(recipe_id)
    comments = db.query(Comment).filter_by(recipe_id=recipe_id).all()
    return render_template('view_comments.html', recipe=recipe, comments=comments)
