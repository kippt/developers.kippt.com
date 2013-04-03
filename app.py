import os

from flask import Flask
from flask import render_template

from flaskext.markdown import Markdown

app = Flask(__name__)

# Flask extensions
Markdown(app)

## Error views

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

## App views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/policy/')
def policy():
    return render_template('policy.html')

@app.route('/apps/')
def apps():
    return render_template('apps.html')

@app.route('/apps/<app_slug>')
def app_view(app_slug):
    '''
    App View
    '''
    
    # Check that directory exists
    if not os.path.exists('templates/apps/%s/' % app_slug):
        abort(404)
    
    return render_template('apps/%s/index.html' % app_slug)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('PORT'):
        app.debug = True
    app.run(host='0.0.0.0', port=port)
