from flask import (
    Flask,
    render_template, 
    request, 
    redirect,
    url_for,
)

from todo_app.flask_config import Config
from todo_app.data.session_items import (
    get_items, 
    add_item,
    get_item,
    save_item,
    delete_item,
)

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
    return redirect(url_for('index'))


@app.route('/complete/<item_id>')
def complete_item(item_id):
    item = get_item(item_id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect(url_for('index'))


@app.route('/delete/<int:item_id>')
def remove_item(item_id):
    item = delete_item(item_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
