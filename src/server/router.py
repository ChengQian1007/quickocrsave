__author__ = 'chrisshroba'

from flask import *
from PIL import Image
import os
import my_utils
import requests
app = Flask(__name__)

@app.route("/api/analyze_picture", methods=["POST"])
def root():
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
            url: url,
            title: title,
            num: num
        }
        ret_data.append(obj)


    os.remove(filename)
    return json.dumps(ret_data[0:3])

app.run(port=8080,host  ="0.0.0.0")