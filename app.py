from flask import Flask, render_template
from models import get_db, User, Recipe  # Убедитесь, что импортируете нужные модели и функцию get_db
from auth import auth_blueprint
from recipe import recipe_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Регистрация блюпринтов
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(recipe_blueprint, url_prefix='/recipes')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)



