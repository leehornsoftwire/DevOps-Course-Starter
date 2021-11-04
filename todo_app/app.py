from flask import Flask, render_template, request
from werkzeug.utils import redirect
from todo_app.data.session_items import (
    add_item,
    complete_item,
    delete_item,
    get_items,
    uncomplete_item,
)

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    items = get_items().items()
    list = [x for x in get_items().items()]
    return render_template("index.html", items=items)


@app.route("/items/new", methods=["POST"])
def add_item_route():
    add_item(request.form.get("title"))
    return redirect("/")


@app.route("/items/complete", methods=["POST"])
def complete_item_route():
    complete_item(int(request.form.get("id")))
    return redirect("/")


@app.route("/items/uncomplete", methods=["POST"])
def uncomplete_item_route():
    uncomplete_item(int(request.form.get("id")))
    return redirect("/")


@app.route("/items/delete", methods=["POST"])
def delete_item_route():
    """
    To be properly REST-ful this should use the DELETE method,
        but html forms can only send get and post - using post to keep things simple for now
    """
    delete_item(int(request.form.get("id")))
    return redirect("/")
