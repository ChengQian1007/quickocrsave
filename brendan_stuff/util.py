from PIL import Image
from subprocess import call
from xgoogle.search import GoogleSearch, SearchError
def image_to_text(in_img):
    """
    Accepts an image file and runs it through tesseract.
    :param in_img: image file to be OCRd
    :return: string of raw text sample.
    """
    in_img.save('input.png')
    call(["tesseract",'input.png','output'])
    foutput = open('output.txt','r')
    text = foutput.read()
    foutput.close()
    return text
def check_all_words(input_text):
    fdict = open('dictionary.txt','r')
    dictionary = fdict.read().split()
    result = []
    for word in input_text.split():
        if word.upper() in dictionary:
            result.append(word)
    return result

def convert_clean(in_img):
    text = image_to_text(in_img)
    return ' '.join(check_all_words(text))


def search_text(text):
    print "search for: "+text
    result_url = ""
    try:
      import ipdb;ipdb.set_trace()
      gs = GoogleSearch(text)
      gs.results_per_page = 50
      results = gs.get_results()
      res_urls = []
      for res in results:
        # print res.title.encode("utf8")
        # print res.desc.encode("utf8")
        print res.url.encode("utf8")

        res_urls.append(res.url.encode("utf8"))
      try:
          result = res_urls[0]
      except:
          result = ''
      return result
    except SearchError, e:
        print "Search failed: %s" % e
        return ""

def determine_link(full_text):
    # import ipdb; ipdb.set_trace()
    text_arr = full_text.split()
    cur_query = ""
    from collections import Counter
    url_counts = Counter()
    count = 0
    for text in text_arr:
        count+=1
        cur_query+=text+" "
        if count % 20 == 0:
            url_counts[search_text(cur_query)]+=1
            cur_query = ""

    return url_counts.most_common()




def example():
    text = convert_clean(Image.open('test2.jpg'))
    url = determine_link(text)
    print "FINAL:"+str(url)
    cleaned = open('cleaned_output.txt','w')
    cleaned.write(text)
    cleaned.close()

