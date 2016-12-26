import feedparser, json, urllib, urllib2
from flask import Flask, render_template, request


app = Flask(__name__)

WEATHER_URL ="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=05feee21417b0866b7c8e76e830365a0"

CURRENCY_URL ="https://openexchangerates.org//api/latest.json?app_id=05feee21417b0866b7c8e76e830365a0"

RSS_FEED = {
    'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn':'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {'publication':'bbc',
               'city': 'London,UK'}

@app.route("/")
def home():
   # get customized headlines, based on user input or default
   publication = request.args.get('publication')
   if not publication:
       publication = DEFAULTS['publication']
   articles = get_news(publication)
   # get customized weather based on user input or default
   city = request.args.get('city')
   if not city:
       city = DEFAULTS['city']
   weather = get_weather(city)
   return render_template("home.html", articles=articles,
    weather=weather)

def get_news(query):
   if not query or query.lower() not in RSS_FEED:
       publication = DEFAULTS["publication"]
   else:
       publication = query.lower()
   feed = feedparser.parse(RSS_FEED[publication])
   return feed['entries']

def get_weather(query):
   query = urllib.quote(query)
   url = WEATHER_URL.format(query)
   data = urllib2.urlopen(url).read()
   parsed = json.loads(data)
   weather = None
   if parsed.get('weather'):
       weather = {'description': parsed['weather'][0]['description'],
              'temperature': parsed['main']['temp'],
              'city': parsed['name'],
              'country': parsed['sys']['country']
}
   return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
