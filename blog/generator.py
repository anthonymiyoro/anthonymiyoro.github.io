import os

from flask import Flask, render_template
from werkzeug import cached_property
import markdown
import yaml

POSTS_FILE_EXTENTION = '.md'
app = Flask(__name__)


# turns markdown into html
class Post(object):
    def __init__(self, path):
        self.path = path
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.path, 'r') as fin:
            content = fin.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content)

    def _initialize_metadata(self):
        content = ''
        with open(self.path, 'r') as fin:
            for line in fin:
                if not line.strip():
                    break
                content += line
        self.__dict__.update(yaml.load(content))


# changes the format of the date of the post
def format_date(value, format='%B %d, %Y'):
    return value.strftime(format)
app.jinja_env.filters['date']=format_date


@app.route('/')
def index():
    posts = [Post('posts/hello.md')]
    return render_template('index.html', posts=posts)


@app.route('/blog/<path:path>')
def post(path):
    path = os.path.join('posts', path + POSTS_FILE_EXTENTION)
    post = Post(path)
    # renders to the post content_variable in the post.html
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
