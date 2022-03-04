from flask import Flask, request, render_template
from decouple import config
import json, requests
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    date_obj = datetime.fromisoformat(date[:-1]).astimezone(timezone('Asia/Kolkata'))
    format = '%d-%m-%y'
    return date_obj.strftime(format) 

@app.route("/")
def home():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + config('api_key')
    response = requests.get(url)
    data = response.json()
    news_list = data['articles']
    return render_template('home.html', news_list=news_list)

@app.route("/sources")
def sources():
    url = "https://newsapi.org/v2/top-headlines/sources?apiKey=" + config('api_key')
    response = requests.get(url)
    data = response.json()
    source_list = data['sources']
    return render_template('sources.html', source_list=source_list)

@app.route("/category/<cat>")
def category(cat):
    url = f"http://newsapi.org/v2/top-headlines?country=in&category={cat}&apiKey=" + config('api_key')
    response = requests.get(url)
    data = response.json()
    news_list = data['articles']
    return render_template('category.html', cat=cat.title(), news_list=news_list)

@app.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.form['keyword']
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey=" + config('api_key')
    response = requests.get(url)
    data = response.json()
    news_list = data['articles']
    return render_template('search.html', keyword=keyword.title(), news_list=news_list)

if __name__ == '__main__':
    app.run(debug=config('debug',cast=bool,default=True))