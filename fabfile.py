import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import os
import glob
import json
import markdown
import shutil
from PIL import Image
from datetime import date

from fabric.operations import prompt
from fabric.api import run
from fabric.colors import green as _green, yellow as _yellow, red as _red

from jinja2 import Environment, FileSystemLoader

PLATFORMS = {
    '1': 'Web',
    '2': 'iOS',
    '3': 'Android',
    '4': 'Windows Phone',
    '5': 'Desktop',
    '6': 'Library',
    '7': 'Other',
}


def add():
    '''
    Add a new app
    '''
    print _green("--- Generating new app for Kippt App Gallery")

    name = prompt("App name:", default='', validate=r'^[\w|\W\s.-]+$')
    developer = prompt("Developer (your name/organization):", validate=r'^[\w|\W\s-]+$')
    developer_website = prompt("(Optional) Developer website (or Twitter address):", default='')
    print 'Platform:\n[1] Web\n[2] iOS\n[3] Android\n[4] Windows Phone\n[5] Desktop\n[6] Library\n[7] Other\n'
    platform = prompt("Platform:", default='1', validate=r'^[1-7]+$')
    price = prompt("(Optional) Price (e.g. $4):", default='')
    link = prompt("Link (e.g. App Store or website):", default='')
    added = date.today().strftime('%B%e. %Y')

    website = prompt("(Optional) Website:", default='')
    twitter = prompt("(Optional) Twitter (e.g. @getappname):", default='')

    slug = re.sub('[^\w\s-]', '', name).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)

    data = {
        'slug': slug,
        'name': name,
        'developer': developer,
        'developer_website': developer_website,
        'platform_id': platform,
        'platform': PLATFORMS[platform],
        'price': price,
        'added': added,
        'link': link,
        'website': website,
        'twitter': twitter,
        'images': {
            'logo': None,
            'screenshots': [],
        }
    }

    # Create directory
    if not os.path.exists('apps/%s' % slug):
        os.makedirs('apps/%s' % slug)
        os.makedirs('apps/%s/images' % slug)
        os.makedirs('apps/%s/images/screenshots' % slug)

    # Lets find the logo
    print _green('--- (Optional) Add logo (logo.png/logo.jpg, 256x256px) to /apps/%s/images/' % slug)
    prompt("Press enter to continue")
    if os.path.exists('apps/%s/images/logo.jpg' % slug):
        logo_file = Image.open('apps/%s/images/logo.jpg' % slug)
        logo_filename = 'logo.jpg'
    elif os.path.exists('apps/%s/images/logo.png' % slug):
        logo_file = Image.open('apps/%s/images/logo.png' % slug)
        logo_filename = 'logo.png'
    else:
        logo_file = None
    if logo_file:
        width, height = logo_file.size
        if width > 256 or height > 256:
            print _red('---    You made the logo too big - Make sure it\'s 256x256px' % slug)
            return
        else:
            data['images']['logo'] = logo_filename

    # Screenshots
    print _green('--- (Optional) Add  max 3 screenshots (JPG/PNG, max. 1024x1024) to /apps/%s/images/screenshots/' % slug)
    prompt("Press enter to continue")
    for screenshot in os.listdir('apps/%s/images/screenshots' % slug):
        if screenshot.split('.')[-1].lower() in ['png', 'jpeg', 'jpg']:
            screenshot_path = 'apps/%s/images/screenshots/%s' % (slug, screenshot)
            screenshot_file = Image.open(screenshot_path)
            width, height = screenshot_file.size
            if width <= 1024 and height <= 1024:
                data['images']['screenshots'].append(screenshot)
            else:
                print _red('---    You made the screenshot too big (max 1024x1024)' % slug)
                return

    manifest = open("apps/%s/manifest.json" % slug, "w")
    manifest.write(json.dumps(data, indent=4))
    manifest.close()

    manifest = open("apps/%s/description.md" % slug, "w")
    manifest.write('This is %s.\n\nIt\'s time to add a markdown formatted description for the app.' % name)
    manifest.close()

    print _green('--- Add app description to /apps/%s/description.md' % slug)
    prompt("Press enter to continue")

    print _green('--- Saved to /apps/%s/' % slug)
    print _green('--- Rendering templates and moving assets...')

    render(slug)


def render(slug):
    '''
    Compile app template into HTML
    '''
    if not os.path.exists('apps/%s' % slug):
        print _red('--- App with this slug can\'t be found(%s)' % slug)
        return

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('apps/app_template.html')

    # Manifest
    data = ''
    with open("apps/%s/manifest.json" % slug, "r") as manifest:
        data = manifest.read().replace('\n', '')
    context = json.loads(data)

    # Description
    description = ''
    with open("apps/%s/description.md" % slug, "r") as desc_file:
        description = desc_file.read()

    # Images to /static/
    if not os.path.exists('static/apps/%s' % slug):
        os.makedirs('static/apps/%s' % slug)

    if context['images'].get('logo'):
        shutil.copy2('apps/%s/images/%s' % (slug, context['images']['logo']), 'static/apps/%s' % (slug))
    for screenshot in context['images'].get('screenshots'):
        shutil.copy2('apps/%s/images/screenshots/%s' % (slug, screenshot), 'static/apps/%s' % (slug))

    # Description
    context['description'] = markdown.markdown(description)

    # Write output
    if not os.path.exists('templates/apps/%s' % slug):
        os.makedirs('templates/apps/%s' % slug)
    else:
        # remove old files
        open("templates/apps/%s/index.html" % slug, "w").close()

    output = open("templates/apps/%s/index.html" % slug, "w")
    output.write('{% extends "base.html" %}\n{% block body %}\n')
    output.write(template.render(context))
    output.write('\n{% endblock %}')
    output.close()

    print _green('--- Done rendering. You can always re-render files with')
    print _yellow('---     fab render:%s' % slug)


def build_apps():
    '''
    Build /apps/ page
    '''
    apps = []
    libs = []
    for app in glob.glob(os.path.join('apps/', '*')):
        data = ''
        with open("%s/manifest.json" % app, "r") as manifest:
            data = manifest.read().replace('\n', '')
        data = json.loads(data)
        if data.get('platform_id') in ['6']:
            libs.append(data)
        else:
            apps.append(data)

    output = open('templates/apps.html', 'w')
    output.write('{% extends "base.html" %}\n{% block bodyclass %}apps-gallery{% endblock %}\n{% block body %}')
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('apps/apps_template.html')
    output.write(template.render({'apps': apps, 'libs': libs}))
    output.write('\n{% endblock %}')
