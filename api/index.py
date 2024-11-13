
#%pip install flask pyngrok

#from pyngrok import ngrok
import os
import sys
import socket
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request
import json
app = Flask(__name__)


target = "https://anoboy.icu"

def geturl(x):
    res = requests.get(x)
    return res.text

def rex(tag_name, attribute_name, a, soup, host):
    if a != 1:
        for tag in soup.find_all(tag_name):
            if tag.get(attribute_name) and not tag.get(attribute_name).startswith("http"):
                tag[attribute_name] = target + tag.get(attribute_name)
    else:
        for tag in soup.find_all(tag_name):
            qq = tag.get(attribute_name)
            # Check if qq is not None before calling replace
            if qq is not None and not tag.get(attribute_name).startswith("http"):
                
                tag[attribute_name] = host + tag.get(attribute_name)

            else:
                tag[attribute_name] = qq.replace(target, host)
                
def head(soup, host):
    elements = soup.select("script[type='application/ld+json'], div[id^='ad'], #judi, #judi2, #disqus_thread, .sidebar, #coloma")
    if elements:  # Check if any elements were selected
        for element in elements:
            element.decompose() #use decompose instead of clear
    rex("link", "href", "", soup, host)
    rex("script", "src", "", soup, host)
    rex("amp-img", "src", "", soup, host)
    rex("img", "src", "", soup, host)
    rex("a", "href", "", soup, host)
    rex("a", "href", 1, soup, host)
    rex("iframe", "src", "", soup, host)
    html = soup.prettify().replace("</head>", """
  <style>
  #menu,   div.column-three-fourth  { width:100% !important;
           overflow: hidden;
          }

   
  </style>
  </head>
  """)
    return html


@app.route("/")
def ok():
    host = "http://" +request.host + "/post"
    soup = BeautifulSoup(geturl(target), 'html.parser')
    print( request.host )
    return head(soup, host)

@app.route("/post/<path:all>" , strict_slashes=False)
def post(all):
    host = "http://"+request.host + "/post"
    url = request.path.split("/post")[1]
    soup = BeautifulSoup(geturl(target+url), 'html.parser')
    print( request.host )
    return head(soup, host)
    
@app.route("/post/")
def pot():
    host = "http://" +request.host + "/post"
    soup = BeautifulSoup(geturl(target), 'html.parser')
    print( request.host )
    return head(soup, host)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
    
    """
    ngrok.set_auth_token("2eGyEJzcdePNVkGXaSao5HUo7QO_Ci6EDAi5wmRYV99kZQNB")
    ngrok_tunnel = ngrok.connect(5000)
    print('Public URL:', ngrok_tunnel.public_url)
    app.run()
    """
