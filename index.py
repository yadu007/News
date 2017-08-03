from flask import Flask,render_template,request
import requests
import urllib
import MySQLdb
from urlparse import urlparse
from bs4 import BeautifulSoup
app = Flask(__name__)
app.debug = True
soup=""
Heading=""
domain=""
data=""
Itext=""
@app.route("/")
def hello():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def my_form_post():
    db = MySQLdb.connect("localhost","root","pwd","SAVEDATA" )
    cursor = db.cursor()
    sql="SELECT * FROM SAVES3"
    cursor.execute(sql)
    #db.commit
    data = cursor.fetchall()
    global data
    global domain
    global soup
    global Heading
    global Itext
    Itext = request.form['text']
    parse=urlparse(Itext)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parse)
    page_source=requests.get(Itext)
    soup=BeautifulSoup(page_source.content)
    Heading=soup.find('p').getText()
    return render_template("index.html",result =soup.h1.string,header=Heading,name=domain,disp=data)
@app.route('/save', methods=['POST'])
def save():
    global data
    global domain
    global soup
    global Heading
    global Itext
    db = MySQLdb.connect("localhost","root","pwd","SAVEDATA" )
    cursor = db.cursor()
    sql = "INSERT INTO SAVES3(HEAD \
       ) \
       VALUES ('%s')" % \
       (Itext)
    try:
        cursor.execute(sql)
        db.commit()
    except TypeError as e:
        db.rollback()
        return str(e)
    db = MySQLdb.connect("localhost","root","pwd","SAVEDATA" )
    cursor = db.cursor()
    sql="SELECT * FROM SAVES3"
    cursor.execute(sql)
    data = cursor.fetchall() #update in each refresh
    return render_template("index.html",result =soup.h1.string,header=Heading,name=domain,disp=data)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8990)
