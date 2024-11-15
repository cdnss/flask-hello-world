
#%pip install flask pyngrok

#from pyngrok import ngrok
import os
import sys
import socket
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request,Response
import json, html
app = Flask(__name__)


target = "https://154.26.137.28"

def geturl(x):
    cookies = {
    cookie['name']: cookie['value'] for cookie in [
        {"domain": "154.26.137.28", "expirationDate": 1731597407, "hostOnly": True, "httpOnly": False, "name": "_as_ipin_tz", "path": "/", "sameSite": "Strict", "secure": False, "session": False, "storeId": "0", "value": "Asia/Jakarta"},
        {"domain": "154.26.137.28", "expirationDate": 1731597407, "hostOnly": True, "httpOnly": False, "name": "_as_ipin_lc", "path": "/", "sameSite": "Strict", "secure": False, "session": False, "storeId": "0", "value": "id"},
        {"domain": "154.26.137.28", "expirationDate": 1731597407, "hostOnly": True, "httpOnly": False, "name": "_as_ipin_ct", "path": "/", "sameSite": "Strict", "secure": False, "session": False, "storeId": "0", "value": "ID"}
    ]
}

    res = requests.get(x, cookies=cookies)
    return res.text

def rex(tag_name, attribute_name, a, soup, host, css):
    if a != 1:
        for tag in soup.find_all(tag_name):
            if tag.get(attribute_name) and not tag.get(attribute_name).startswith("http"):
                tag[attribute_name] = target + tag.get(attribute_name)
    else:
        for tag in soup.find_all(tag_name):
            qq = tag.get(attribute_name)
            # Check if qq is not None before calling replace
            if qq is not None and not tag.get(attribute_name).startswith("http"):
                if css != 1:
                  tag[attribute_name] = host + tag.get(attribute_name)
                else:
                  tag[attribute_name] = host +"/f"+ tag.get(attribute_name) +"?"
            else:
                if tag.get(attribute_name):
                  if css != 1:
                    tag[attribute_name] = qq.replace(target, host)
                  else:
                    tag[attribute_name] = qq.replace(target, host+"/f") + "?"
                
def head(soup, host):
    elements = soup.select("script[type='application/ld+json'], #judi, #judi2, #disqus_thread, .sidebar, #as_radio-js, script[id^=disqus] ")
    if elements:  # Check if any elements were selected
        for element in elements:
            element.decompose() #use decompose instead of clear
    rex("link", "href", "", soup, host, "")
    #rex("script", "src", 1, soup, host, 1)
    rex("amp-img", "src", "", soup, host, "")
    #rex("img", "src", "", soup, host, "")
    rex("a", "href", "", soup, host, "")
    rex("a", "href", 1, soup, host, "")
    rex("iframe", "src", "", soup, host, "")
    html = soup.prettify().replace("$(document).find('#pembed').html(atob(defaultpembed));", """

$(document).find('#pembed').html(atob(defaultpembed));
}
  var sa = jQuery("#embed_holder iframe").attr("src");
  if ( sa.startsWith('"""+target+"""') ) {
  
  var sb = sa.replace('"""+target+"""', window.location.protocol + '//' + window.location.host)
  
  jQuery("#pembed").html(`
  
  <iframe src="${sb}" frameborder="0" marginwidth="0" marginheight="0" scrolling="NO" width="100%" height="100%" allowfullscreen="true"></iframe>
  
  
  `)
  
  

  """).replace("function statistic()", "/* ").replace('jQuery("#pembed").html(embed);', F"""
  
  jQuery("#pembed").html(embed);
  
  var sc = jQuery("#embed_holder iframe").attr("src");
  if ( sc.startsWith('"""+target+"""') ) {
  
  var sv = sc.replace('"""+target+"""', window.location.protocol + '//' + window.location.host)
  
  jQuery("#pembed").html(`
  
  <iframe src="${sv}" frameborder="0" marginwidth="0" marginheight="0" scrolling="NO" width="100%" height="100%" allowfullscreen="true"></iframe>
  
  
  `)
  
  
  }
  
  """)
   
    return html


@app.route("/")
def ok():
    host = request.host_url[:-1]
    soup = BeautifulSoup(geturl(target), 'html.parser')
    print( request.host )
    return head(soup, host)

@app.route("/<path:all>" , strict_slashes=False)
def post(all):
    host = request.host_url[:-1]
    url = request.full_path
    soup = BeautifulSoup(geturl(target+url), 'html.parser')
    print( target+url )
    return head(soup, host)
    
@app.route("/f/<path:i>", strict_slashes=False)
def f(i):
    host = request.host_url[:-1]
    url = request.full_path.split("/f")[1]
    soup = BeautifulSoup(geturl(target+url), 'html.parser')
    res = ""
    if url.endswith("css?"):
      res = Response(head(soup, host), mimetype='text/css')
    elif url.endswith(".js?"):
      res = Response(head(soup, host), mimetype='text/json')
    elif url.endswith("xml?"):
      res = Response(head(soup, host), mimetype='text/xml')  
    else:
      res = head(soup, host)
      
    return res
    """
@app.route("/anime/<path:a>" , strict_slashes=False)
def anime(a):
    host = "http://"+request.host + "/post"
    url = request.full_path
    soup = BeautifulSoup(geturl(target+url), 'html.parser')
    print( target+url )
    return head(soup, host)
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
    
    """
    ngrok.set_auth_token("2eGyEJzcdePNVkGXaSao5HUo7QO_Ci6EDAi5wmRYV99kZQNB")
    ngrok_tunnel = ngrok.connect(5000)
    print('Public URL:', ngrok_tunnel.public_url)
    app.run()
    """
