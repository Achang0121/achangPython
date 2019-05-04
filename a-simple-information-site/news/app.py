#!/usr/bin/env python3
import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
file_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'files'))

class File():
    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        data_dict = {}
        for filename in os.listdir(file_dir):
            with open(os.path.join(file_dir, filename)) as f:
                data_dict[filename[:-5]] = json.load(f)
        return data_dict

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_content(self, filename):
        return self._files[filename]

f = File()

@app.route('/')
def index():
    # 显示文章名称的列表
    # 也就是/home/shiyanlou/files/目录下所有json文件中的title信息列表
    return render_template('index.html', title_list=f.get_title_list())    

@app.route('/files/<filename>')
def file(filename):
    # 读取并显示 filename.json中的文章内容
    # 例如 filename='helloshiyanlou' 的时候显示 helloshiyanlou.json中的内容
    # 不存在，则显示包含字符窗 'shiyanlou 404' 404 错误页面
    if not f.get_content(filename):
        return abort(404)
    return render_template('file.html', data=f.get_content(filename))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
        
        
if __name__ == '__main__':
    app.run()
