from PIL import Image
from subprocess import call
from urllib import urlencode
from collections import Counter
import json
import requests
import os
import random
import time
import re

PROXY_LIST=['http://proxy-ip-list.com/download/proxy-list-port-3128.txt']
def image_to_text(in_img):
    """
    Accepts an image file and runs it through tesseract.
    :param in_img: image file to be OCRd
    :return: string of raw text sample.
    """
    in_img.save('input.png')
    call(["tesseract", 'input.png', 'output'])

    foutput = open('output.txt', 'r')
    text = foutput.read()
    foutput.close()
    os.remove('output.txt')
    os.remove('input.png')

    return text


def check_all_words(input_text):
    fdict = open('dictionary.txt', 'r')
    dictionary = fdict.read().split()
    result = []
    for word in input_text.split():
        if word.upper() in dictionary:
            result.append(word)
    return result


def convert_clean(in_img):
    text = image_to_text(in_img)
    return ' '.join(check_all_words(text))


def get_result_json(text):
    # import ipdb;ipdb.set_trace()
    proxy_list = requests.get(PROXY_LIST[0]).text
    response_code = 200
    link = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"+urlencode({'q': text})
    response = requests.get(link)
    response_text, response_code = response.text, response.status_code
    if json.loads(response_text)["responseStatus"] not in range(400, 500):
        response_text = response_text.replace('\u003c/b\u003e', '').replace('\u003cb\u003e', '')
        return response_text
    print "Forbidden by Google on this IP.  Switching to next proxy."
    proxies = []
    for row in proxy_list.split('\r'):
        ip_search = re.search('^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\:3128', row)
        if ip_search:
            ip = ip_search.group(0)
            if ip:
                proxies.append(ip)
        try:

            proxyDict = {"http": ip}

            response = requests.get(link, proxies=proxyDict)
            response_text, response_code = response.text, response.status_code
            if "<html>" not in response_text:
                response_text = response_text.replace('\u003c/b\u003e', '').replace('\u003cb\u003e', '')
                return response_text
        except Exception:
            print "failed on", row, "\n continuing..."


    if response_code in range(400, 500):
        print "BUSTED: Google caught you" #raise Exception('BUSTED: Google caught you.')

def determine_link(full_text):
    text_arr = full_text.split()
    cur_query = ""
    count = 0
    final_dict = Counter()
    chunk_size = 20
    num_chunks = 10
    for text in text_arr:
        count += 1
        cur_query += text+" "
        if (count % chunk_size == 0 and count < chunk_size * num_chunks) or count == len(text_arr)-1:
            results_json = json.loads(get_result_json(cur_query))
            print results_json

            if results_json["responseStatus"] in range(400, 500):
                raise Exception('BUSTED: Google caught you.')

            cur = results_json["responseData"]["results"]
            for x in range(len(cur)):
                cur_key = cur[x]['url'], cur[x]["title"]
                final_dict[cur_key] += 1
            cur_query = ""

    return final_dict.most_common()

def get_links_from_image(image):
    text = convert_clean(image)
    urls = determine_link(text)
    return urls

def example():
    text = convert_clean(Image.open('../../test_data/cracking_coding_foreward.jpg').rotate(-90))
    urls = determine_link(text)
    for row in urls:
        print row
    cleaned = open('cleaned_output.txt', 'w')
    cleaned.write(text)
    cleaned.close()
    os.remove('cleaned_output.txt')
