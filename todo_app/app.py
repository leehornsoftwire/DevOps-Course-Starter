from flask import Flask, render_template, request
from flask.globals import session
from werkzeug.utils import redirect
from todo_app.data.items_backend import Item, ItemsBackend, Status
from todo_app.data.session_items import SessionItems

from todo_app.data.trello.trello_items import TrelloItems
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel


SESSION_BACKEND = "Session"
TRELLO_BACKEND = "Trello"


def create_app():
    app = Flask(__name__, static_folder="./static")
    app.config.from_object(Config())

    @app.route("/")
    def index():
        view_model = get_view_model()
        return render_template("index.html", view_model=view_model)

    @app.route("/switchbackend", methods=["POST"])
    def switch_backend():
        specified_backend = get_item_backend_name()
        if specified_backend == SESSION_BACKEND:
            set_item_backend(TRELLO_BACKEND)
        else:
            set_item_backend(SESSION_BACKEND)
        return redirect("/")

    @app.route("/items/new", methods=["POST"])
    def add_item_route():
        item = Item(title=request.form.get("title"), status=Status.TODO)
        get_item_backend().add_item(item)
        return redirect("/")

    @app.route("/items/setstatus", methods=["POST"])
    def set_status():
        get_item_backend().set_status(
            request.form.get("id"), Status(request.form.get("status"))
        )
        return redirect("/")

    @app.route("/items/delete", methods=["POST"])
    def delete_item_route():
        """
        To be properly REST-ful this should use the DELETE method,
        but html forms can only send get and post - using post to keep things simple for now
        """
        get_item_backend().delete_item(request.form.get("id"))
        return redirect("/")

    return app


def clear_session_data():
    keys = list(session.keys())
    for key in keys:
        session.pop(key)


def get_item_backend_name():
    return session.get("ItemBackend") or SESSION_BACKEND


def set_item_backend(to: str):
    session["ItemBackend"] = to


def get_item_backend() -> ItemsBackend:
    specified_backend = get_item_backend_name()
    if specified_backend == SESSION_BACKEND:
        return SessionItems.load()
    elif specified_backend == TRELLO_BACKEND:
        return TrelloItems.load()
    else:
        raise ValueError("Unknown backend")


def get_view_model() -> ViewModel:
    return ViewModel(get_item_backend())
