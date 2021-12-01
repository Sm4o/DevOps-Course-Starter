import os

from flask import (
    Flask,
    render_template, 
    request, 
    redirect,
    url_for,
)

from todo_app.config import TrelloConfig, Config
from todo_app.data.trello import Trello, CardStatus
from todo_app.data.mongodb import MongoDB
from todo_app.views.views import ViewModel


def create_app():
    app = Flask(__name__)

    mongo = MongoDB(
        Config().MONGODB_CONNECTION, 
        Config().DATABASE_NAME
    )

    @app.route('/')
    def index():
        items_list = mongo.get_items()
        item_view_model = ViewModel(items_list)
        return render_template('index.html', 
                               view_model=item_view_model)

    @app.route('/add_item', methods=['POST'])
    def add_todo_item():
        item_title = request.form.get('title')
        item_description = request.form.get('description')
        mongo.add_item(item_title, item_description)
        return redirect(url_for('index'))

    @app.route('/complete/<item_id>')
    def complete_item(item_id):
        mongo.update_item(item_id, CardStatus.DONE)
        return redirect(url_for('index'))

    @app.route('/do/<item_id>')
    def do_item(item_id):
        mongo.update_item(item_id, CardStatus.DOING)
        return redirect(url_for('index'))

    @app.route('/uncomplete/<item_id>')
    def uncomplete_item(item_id):
        mongo.update_item(item_id, CardStatus.TODO)
        return redirect(url_for('index'))

    @app.route('/delete/<item_id>')
    def remove_item(item_id):
        mongo.delete_item(item_id)
        return redirect(url_for('index'))
    return app


if __name__ == '__main__':
    app = create_app() 
    app.run()
