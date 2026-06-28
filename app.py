from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/generate')
def generate():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is missing"}), 400
    
    # yt-dlp की सेटिंग्स जो इसे एक 'Bot' के बजाय 'User' की तरह दिखाती हैं
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # ytsearch: के जरिए सर्च किया
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info and info['entries']:
                video_url = info['entries'][0]['webpage_url']
                return jsonify({"link": video_url})
            else:
                return jsonify({"error": "No results found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # रेंडर के PORT का इस्तेमाल करें
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
