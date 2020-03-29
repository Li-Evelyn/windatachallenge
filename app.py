from flask import Flask
from flask import render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import graphs_test

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("site.html")

@app.route('/home.html')
@app.route('/home')
def hello_world():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)
