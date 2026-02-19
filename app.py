from flask import Flask, request
import re

app = Flask(__name__)

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    player_content = "URLを入力してください"
    if request.method == 'POST':
        v_id = get_video_id(request.form.get('url', ''))
        if v_id:
            src_url = f"https://www.youtube.com/embed/{v_id}?playlist={v_id}&loop=1&autoplay=1"
            player_content = f'<div><iframe width="100%" height="400" src="{src_url}" frameborder="0" allow="autoplay"></iframe></div>'
        else:
            player_content = "無効なURLです"

    head = "<html><head><title>LoopTube</title></head><body style='text-align:center;padding:20px;'>"
    title = "<h1>LoopTube Player</h1>"
    form = "<form method='POST'><input type='text' name='url' style='width:70%' placeholder='URLを貼る'><button type='submit'>PLAY</button></form>"
    footer = "</body></html>"
    
    return head + title + player_content + form + footer

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
