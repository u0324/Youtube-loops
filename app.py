from flask import Flask, request
import re
import os

app = Flask(__name__)

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    player_content = "URLを入力してください"
    if request.method == 'POST':
        if 'delete' in request.form:
            player_content = "消去しました"
        else:
            v_id = get_video_id(request.form.get('url', ''))
            if v_id:
                src_url = f"https://www.youtube.com/embed/{v_id}?playlist={v_id}&loop=1&autoplay=1"
                player_content = f'<div><iframe width="100%" height="400" src="{src_url}" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div>'
            else:
                player_content = "無効なURLです"

    head = "<html><head><title>Yt-Player</title></head><body style='text-align:center;padding:20px;'>"
    title = "<h1>YT Player</h1>"
    
    form = "<form method='POST'><input type='text' name='url' style='width:60%' placeholder='URLを貼る' autocomplete='off'><button type='submit'>PLAY</button><button type='submit' name='delete' style='margin-left:5px;'>DELETE</button></form."
    
    footer = "</body></html>"
    
    return head + title + player_content + form + footer

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
