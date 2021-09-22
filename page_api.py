
from flask import render_template,  Blueprint

page = Blueprint('page', __name__)


@page.route("/map", methods=["GET"])
def map():

    return render_template("map.html")

@page.route("/mean", methods=["GET"])
def mean():

    return render_template("mean.html")