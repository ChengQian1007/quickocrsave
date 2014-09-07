__author__ = 'chrisshroba'

from flask import *
from PIL import image
import os

app = Flask(__name__)

@app.route("/api/analyze_picture", methods=["POST"])
def root():
    image_file = request.files["file"]
    image_file.save(os.path.join(os.getcwd(), "temp.jpeg"))

