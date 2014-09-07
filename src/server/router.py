__author__ = 'chrisshroba'

from flask import *
from PIL import Image
import os
import my_utils
import time
import requests
app = Flask(__name__,
            static_folder="../../static",
            static_path="")



@app.route("/api/analyze_picture", methods=["POST"])
def root():
    timestamp = time.strftime("%A, %B %e, %G")
    image_file = request.files["userfile"]
    filename = os.path.join(os.getcwd(), "temp.jpeg")
    image_file.save(filename)

    img = Image.open("temp.jpeg")

    data = my_utils.get_links_from_image(img)

    ret_data = []
    for entry in data:
        url = entry[0][0]
        title = entry[0][1]
        num = entry[1]
        print "%s\t%-80s - %s" % (num,title,url)
        obj = {
            "url": url,
            "title": title,
            "num": num
        }
        ret_data.append(obj)

    scan = {
        "timestamp": timestamp,
        "possible_sources": ret_data
    }
    if len(ret_data)>=1:
        with open("scans.txt", "a") as myfile:
            myfile.write(json.dumps(scan)+", ")

    os.remove(filename)
    return json.dumps(ret_data[0:3])



@app.route("/api/get_all_sources")
def get_all_sources():
    scans_file = open("scans.txt").read()[:-2]
    ret = "{\"scans\" : [%s]}" % scans_file
    return ret



app.run(port=8080,host="0.0.0.0")