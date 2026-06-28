from flask import Flask, request, jsonify
from pytubefix import Search

app = Flask(__name__)

@app.route('/generate')
def generate():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query missing"}), 400
    
    try:
        s = Search(query)
        if s.videos:
            return jsonify({"link": s.videos[0].watch_url})
        return jsonify({"error": "No results"}), 404
    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500
