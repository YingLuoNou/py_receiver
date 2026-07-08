# /// script
# dependencies = [
#     "flask",
# ]
# ///

import os
import socket
from flask import Flask, request, redirect, flash, render_template_string

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# 【核心修改】直接获取当前终端所在的目录！不需要再从 PowerShell 传参了
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML 模板：一个简单的上传表单和文件列表
HTML_TEMPLATE = '''
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>局域网文件共享与上传</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .upload-box { border: 2px dashed #ccc; padding: 20px; text-align: center; background: #fafafa; }
        .file-list { margin-top: 30px; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 8px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
        a { color: #0066cc; text-decoration: none; }
        .flash { color: green; font-weight: bold; margin-bottom: 15px; }
    </style>
</head>
<body>
    <h2>局域网文件共享与上传服务器</h2>
    
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for message in messages %}
          <div class="flash">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="upload-box">
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <input type="submit" value="上传文件" style="padding: 5px 15px;">
        </form>
    </div>

    <div class="file-list">
        <h3>当前目录文件列表（点击可下载）：</h3>
        <ul>
            {% for file in files %}
            <li>
                <a href="/download/{{ file }}">{{ file }}</a>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

def get_local_ip():
    """获取本机局域网 IP 地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有文件部分')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'文件 {filename} 上传成功！')
            return redirect(request.url)

    # 获取当前目录下的所有文件
    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and not f.startswith('.')]
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    print("\n" + "="*50)
    print(f" 接收服务器已在当前目录启动！")
    print(f" 当前工作目录: {UPLOAD_FOLDER}")
    print(f" 👉 局域网地址: http://{local_ip}:{port}")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)