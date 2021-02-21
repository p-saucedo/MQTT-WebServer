from flask import Flask, flash, request, redirect, url_for, render_template
from clientMQTT import MQTTClient
from time import sleep
app = Flask(__name__)

global client
client = None

# Routes
@app.route('/')
def index():

    global client
    client = MQTTClient('127.0.0.1')
    client.run_client()

    sleep(1) # Needed for retrieveing the mainpage html
    
    return render_template('index.html', code = client.get_html())

@app.route('/search', methods = ['POST'])
def search():
    
    try:
        searched_route = request.form['route']
    except KeyError:
        return render_template('index.html', code = "<p>NO URL PROVIDED</p>")
    
    global client
    if(client.suscribe(searched_route) == False):
        return render_template('index.html', code = "<p>URL DOES NOT EXISTS</p>")
    else:
        return render_template('index.html', code = client.get_html())


    

    


if __name__ == "__main__":
    app.run(
            debug=True, 
            port=5000, 
            threaded=False
            )