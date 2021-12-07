from flask import Flask, render_template, request
from flask.globals import session
from werkzeug.utils import redirect
from todo_app.data.items_backend import Item
from todo_app.data.session_items import SessionItems

from todo_app.data.trello_items import TrelloItems
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

SESSION_BACKEND = "Session"
TRELLO_BACKEND = "Trello"


def clear_session_data():
    keys = list(session.keys())
    for key in keys:
        session.pop(key)


def get_item_backend_name():
    return session.get("ItemBackend") or SESSION_BACKEND


def set_item_backend(to: str):
    session["ItemBackend"] = to


def get_item_backend():
    specified_backend = get_item_backend_name()
    if specified_backend == SESSION_BACKEND:
        return SessionItems.load()
    elif specified_backend == TRELLO_BACKEND:
        return TrelloItems.load()
    else:
        raise ValueError("Unknown backend")


@app.route("/")
def index():
    items = get_item_backend().get_items()
    return render_template(
        "index.html", items=items, item_backend=get_item_backend_name()
    )


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
    item = Item(title=request.form.get("title"), status="TO DO")
    get_item_backend().add_item(item)
    return redirect("/")


@app.route("/items/complete", methods=["POST"])
def complete_item_route():
    get_item_backend().complete_item(request.form.get("id"))
    return redirect("/")


@app.route("/items/uncomplete", methods=["POST"])
def uncomplete_item_route():
    get_item_backend().uncomplete_item(request.form.get("id"))
    return redirect("/")


@app.route("/items/delete", methods=["POST"])
def delete_item_route():
    """
    To be properly REST-ful this should use the DELETE method,
      but html forms can only send get and post - using post to keep things simple for now
    """
    get_item_backend().delete_item(request.form.get("id"))
    return redirect("/")
