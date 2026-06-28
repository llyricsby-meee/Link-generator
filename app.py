from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/generate')
def generate():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter missing"}), 400
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in results and results['entries']:
                return jsonify({"link": results['entries'][0]['webpage_url']})
            return jsonify({"error": "No results found"}), 404
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
