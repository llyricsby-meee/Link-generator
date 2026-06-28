from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/generate')
def generate():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter missing"}), 400
    
    # Vercel के लिए 'quiet' मोड और सही 'user_agent' जरूरी है
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ytsearch1 इस्तेमाल कर रहे हैं ताकि केवल पहला परिणाम मिले
            results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in results and results['entries']:
                video = results['entries'][0]
                return jsonify({"link": video['webpage_url']})
            else:
                return jsonify({"error": "No result found"}), 404
    except Exception as e:
        # यहाँ साफ़ पता चलेगा कि YouTube ने ब्लॉक किया है या कुछ और
        return jsonify({"error": "Server error", "details": str(e)}), 500

# Vercel के लिए app को ग्लोबल रखना जरूरी है
