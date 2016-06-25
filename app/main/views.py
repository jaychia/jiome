from flask import jsonify
from . import main
from ..models import *

@main.route("/interests")
def getInterests():
	return jsonify(Interest.query.all())
