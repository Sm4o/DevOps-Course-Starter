from flask import Flask, render_template, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items_list = get_items()
    return render_template('index.html', items_list=items_list)


@app.route('/add_item', methods=['POST'])
def add_todo_item():
    item_title = request.form.get('title')
    add_item(item_title)
    items_list = get_items()
    return render_template('index.html', items_list=items_list)


if __name__ == '__main__':
    app.run()
