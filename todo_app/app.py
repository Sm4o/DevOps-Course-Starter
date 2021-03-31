import os

from flask import (
    Flask,
    render_template, 
    request, 
    redirect,
    url_for,
)

from todo_app.config import Config, TrelloConfig
from todo_app.data.trello import Trello, CardStatus
from todo_app.views.views import ViewModel


app = Flask(__name__)
app.config.from_object(Config)

trello = Trello(TrelloConfig.APP_KEY, TrelloConfig.TOKEN, TrelloConfig.BOARD_ID)


@app.route('/')
def index():
    items_list = trello.get_items()
    item_view_model = ViewModel(items_list)
    return render_template('index.html', 
                           view_model=item_view_model)


@app.route('/add_item', methods=['POST'])
def add_todo_item():
    item_title = request.form.get('title')
    item_description = request.form.get('description')
    trello.add_item(item_title, item_description)
    return redirect(url_for('index'))


@app.route('/complete/<item_id>')
def complete_item(item_id):
    trello.update_item(item_id, CardStatus.DONE)
    return redirect(url_for('index'))


@app.route('/do/<item_id>')
def do_item(item_id):
    trello.update_item(item_id, CardStatus.DOING)
    return redirect(url_for('index'))


@app.route('/uncomplete/<item_id>')
def uncomplete_item(item_id):
    trello.update_item(item_id, CardStatus.TODO)
    return redirect(url_for('index'))


@app.route('/delete/<item_id>')
def remove_item(item_id):
    trello.delete_item(item_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
