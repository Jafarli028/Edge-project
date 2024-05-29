from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://en.wikipedia.org/w/api.php"

def suggest(query):
    url = f"{BASE_URL}?action=opensearch&search={query}&limit=1&namespace=0&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    suggestion = data[1][0] if data[1] else None
    return suggestion

def get_page_id(title):
    url = f"{BASE_URL}?action=query&titles={title}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    pages = data['query']['pages']
    page = next(iter(pages.values()))
    return page

def geosearch(lat, lon):
    url = f"{BASE_URL}?action=query&list=geosearch&gscoord={lat}|{lon}&gsradius=10000&gslimit=10&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    geosearch_results = data['query']['geosearch']
    return geosearch_results

def get_page_url(pageid):
    url = f"{BASE_URL}?action=query&pageids={pageid}&format=json&prop=info&inprop=url"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    page = data['query']['pages'].get(str(pageid))
    if page and 'fullurl' in page:
        return page['fullurl']
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest_route():
    query = request.form.get('query')
    result = suggest(query)
    return jsonify({'query': query, 'suggestion': result})

@app.route('/page_id', methods=['POST'])
def page_id_route():
    title = request.form.get('title')
    result = get_page_id(title)
    return jsonify(result)

@app.route('/geosearch', methods=['POST'])
def geosearch_route():
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    result = geosearch(lat, lon)
    return jsonify(result)

@app.route('/page_url', methods=['POST'])
def page_url_route():
    try:
        pageid = int(request.form.get('pageid'))
        result = get_page_url(pageid)
        if result is None:
            return jsonify({'error': 'Page not found'}), 404
        return jsonify({'pageid': pageid, 'url': result})
    except ValueError:
        return jsonify({'error': 'Invalid pageid'}), 400

if __name__ == '__main__':
    app.run(debug=True)
