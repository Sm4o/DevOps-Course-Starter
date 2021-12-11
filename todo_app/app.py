from os import access
from functools import wraps
import requests
from flask import (
    Flask,
    render_template, 
    request, 
    redirect,
    url_for,
)
from flask_login import (
    LoginManager, 
    login_required, 
    login_user, 
    UserMixin, 
    current_user,
)
from oauthlib.oauth2 import WebApplicationClient

from todo_app.config import Config
from todo_app.data.mongodb import MongoDB, CardStatus
from todo_app.views.views import ViewModel


class User(UserMixin):
    def __init__(self, name):
        self.id = name 


login_manager = LoginManager()

# Bad practice, but hardcoded for training purposes
WRITER_LIST = ['Sm4o']


@login_manager.unauthorized_handler
def unauthenticated():
    client = WebApplicationClient(Config().GITHUB_CLIENT_ID)
    redirect_url = client.prepare_request_uri('https://github.com/login/oauth/authorize', 
                                              redirect_uri='http://localhost:5000/login/callback')
    return redirect(redirect_url)


@login_manager.user_loader
def load_user(name):
    return User(name)


def check_writer_role(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id in WRITER_LIST:
                return func(*args, **kwargs)
            else:
                return login_manager.unauthorized()
        else:
            # Only happens in tests or if no login_required decorator found
            return func(*args, **kwargs)
    return decorated_view


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager.init_app(app)

    mongo = MongoDB()

    client = WebApplicationClient(Config().GITHUB_CLIENT_ID)

    @app.route('/')
    @login_required
    def index():
        items_list = mongo.get_items()
        item_view_model = ViewModel(items_list, current_user, WRITER_LIST)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        code = request.args.get('code')
        # Obtain an access token
        url, headers, data = client.prepare_token_request(
            "https://github.com/login/oauth/access_token", 
            client_id=Config().GITHUB_CLIENT_ID, 
            client_secret=Config().GITHUB_CLIENT_SECRET,
            code=code,
        )
        headers['Accept'] = 'application/json'  
        response = requests.post(url, data=data, headers=headers)
        client.parse_request_body_response(response.text)
        url, headers, _ = client.add_token('https://api.github.com/user', headers=headers)
        github = requests.get(url, headers=headers)
        github_user = github.json()
        name = github_user['login']
        user = User(name)
        login_user(user)
        return redirect(url_for('index'))

    @app.route('/add_item', methods=['POST'])
    @check_writer_role
    @login_required
    def add_todo_item():
        item_title = request.form.get('title')
        item_description = request.form.get('description')
        mongo.add_item(item_title, item_description)
        return redirect(url_for('index'))

    @app.route('/complete/<item_id>')
    @check_writer_role
    @login_required
    def complete_item(item_id):
        mongo.update_item(item_id, CardStatus.DONE)
        return redirect(url_for('index'))

    @app.route('/do/<item_id>')
    @check_writer_role
    @login_required
    def do_item(item_id):
        mongo.update_item(item_id, CardStatus.DOING)
        return redirect(url_for('index'))

    @app.route('/uncomplete/<item_id>')
    @check_writer_role
    @login_required
    def uncomplete_item(item_id):
        mongo.update_item(item_id, CardStatus.TODO)
        return redirect(url_for('index'))

    @app.route('/delete/<item_id>')
    @check_writer_role
    @login_required
    def remove_item(item_id):
        mongo.delete_item(item_id)
        return redirect(url_for('index'))
    return app


if __name__ == '__main__':
    app = create_app() 
    app.run()
