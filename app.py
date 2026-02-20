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
    player_placeholder = "<div style='color:#666;'>URLを入力してPLAYを押してください</div>"
    is_loop_checked = "checked" 
    v_id = ""
    current_url = ""

    if request.method == 'POST':
        if 'delete' in request.form:
            player_placeholder = "<div style='color:#d9534f;'>消去しました</div>"
            current_url = ""
        else:
            current_url = request.form.get('url','')
            v_id = get_video_id(current_url)
            is_loop_checked = "checked" if "loop" in request.form else ""
            
            if v_id:
                player_placeholder = '<div id="player-wrapper" style="max-width:800px; margin:0 auto; shadow: 0 4px 15px rgba(0,0,0,0.3);"><div id="yt-player"></div></div>'
            else:
                player_placeholder = "<div style='color:#d9534f;'>無効なURLです</div>"

    loop_js_flag = "true" if is_loop_checked else "false"

    head = f"""
    <html><head><title>YT-Player</title>
    <style>
        body {{ text-align:center; padding:40px 20px; background:#1a1a1a; color:#eee; font-family: 'Helvetica Neue', Arial, sans-serif; }}
        h1 {{ margin-bottom: 30px; font-weight: 300; letter-spacing: 2px; }}
        .controls {{ margin-top: 30px; background: #2a2a2a; padding: 20px; border-radius: 12px; display: inline-block; }}
        input[type='text'] {{ width:400px; padding:12px; border:none; border-radius:6px; background:#333; color:#fff; margin-bottom: 15px; }}
        button {{ padding:12px 25px; cursor:pointer; border-radius:6px; border:none; font-weight:bold; transition: 0.3s; }}
        .btn-play {{ background:#007bff; color:white; }}
        .btn-play:hover {{ background:#0056b3; }}
        .btn-delete {{ background:#444; color:#ccc; margin-left:10px; }}
        .btn-delete:hover {{ background:#555; }}
        label {{ cursor: pointer; font-size: 14px; color: #bbb; }}
    </style>
    
    <script src="https://www.youtube.com/iframe_api"></script>
    
    <script>
        let player;
        const videoId = "{v_id}";
        const loopEnabled = {loop_js_flag};

        function onYouTubeIframeAPIReady() {{
            if (!videoId || videoId === "None" || videoId === "") return;
            
            player = new YT.Player('yt-player', {{
                height: '450',
                width: '100%',
                videoId: videoId,
                playerVars: {{
                    'autoplay': 1,
                    'controls': 1,
                    'rel': 0,
                    'enablejsapi': 1
                }},
                events: {{
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}

        function onPlayerStateChange(event) {{
            if (event.data === YT.PlayerState.ENDED && loopEnabled) {{
                player.playVideo();
            }}
        }}

        window.addEventListener('keydown', function(e) {{
            if (!player || typeof player.getPlayerState !== 'function') return;

            if (e.keyCode === 32 || e.keyCode === 75) {{
                if (document.activeElement.tagName === 'INPUT') return;
                
                e.preventDefault(); 
                
                const currentState = player.getPlayerState();
                if (currentState === 1 || currentState === 3) {{
                    player.pauseVideo();
                }} else {{
                    player.playVideo();
                }}
            }}
        }});
    </script>
    </head ><body>
    """
    
    title = "<h1>YT Player</h1>"
    
    form = f"""
    <div class='controls'>
        <form method='POST' style='margin:0;'>
            <input type='text' name='url' value='{current_url}' placeholder='動画URLを入力' autocomplete='off'><br>
            <label><input type='checkbox' name='loop' {is_loop_checked}>ループ再生</label>
            <div style='margin-top:15px;' >
                <button type='submit' class='btn-play' >PLAY</button>
                <button type='submit' name='delete' class='btn-delete'>DELETE</button>
            </div>
        </form>
    </div>
    """
    
    footer = "</body></html>"
    
    return head + title + player_placeholder + form + footer

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
