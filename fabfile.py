import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import os
import json
import markdown
from datetime import date

from fabric.operations import prompt
from fabric.api import run
from fabric.colors import green as _green, yellow as _yellow, red as _red

from jinja2 import Environment, FileSystemLoader

def add():
    '''
    Add a new app
    '''
    print _green("--- Generating new app for Kippt App Gallery")
    
    name = prompt("App name:", default='', validate=r'^[\w\s-]+$')
    developer = prompt("Developer (your name/organization):", validate=r'^[\w\s-]+$')
    developer_website = prompt("(Optional) Developer website (or Twitter address):", default='')
    print 'Platform:\n[1] Web\n[2] iPhone\n[3] Android\n[4] Windows Phone\n[4] Desktop\n[5] Library\n[6] Other\n'
    platform = prompt("Platform:", default='1', validate=r'^[1-6]+$')
    price = prompt("(Optional) Price (e.g. $4):", default='')
    link = prompt("(Optional) Link (e.g. App Store or website):", default='')
    added = date.today().strftime('%B%e. %Y')
    
    website = prompt("(Optional) Website:", default='')
    twitter = prompt("(Optional) Twitter (e.g. @getappname):", default='')
    
    data = {
        'name': name,
        'developer': developer,
        'developer_website': developer_website,
        'platform': platform,
        'price': price,
        'added': added,
        'link': link,
        'website': website,
        'twitter': twitter,
    }
    
    # Create directory
    slug = re.sub('[^\w\s-]', '', name).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)
    if not os.path.exists('apps/%s' % slug):
        os.makedirs('apps/%s' % slug)
        os.makedirs('apps/%s/images' % slug)
    
    manifest = open("apps/%s/manifest.json" % slug, "w")
    manifest.write(json.dumps(data, indent=4))
    manifest.close()
    
    manifest = open("apps/%s/description.md" % slug, "w")
    manifest.write('This is %s.\n\nIt\'s time to add a markdown formatted description for the app.' % name)
    manifest.close()
    
    print _green('--- Add app description to /apps/%s/description.md' % slug)
    prompt("Press enter to continue", default='')
    
    print _green('--- (Optional) Add logo (logo.png/logo.jpg, 256x256px) to /apps/%s/images/' % slug)
    prompt("Press enter to continue", default='')
    
    print _green('--- (Optional) Add screenshots (JPG/PNG, max. 1024x1024 & 1MB) to /apps/%s/images/' % slug)
    prompt("Press enter to continue", default='')
    
    print _green('--- Saved to /apps/%s/' % slug)
    print _yellow('---     fab compile:%s' % slug) 

def compile(slug):
    '''
    Compile app template into HTML
    '''
    if not os.path.exists('apps/%s' % slug):
        print _red('--- App with this slug can\'t be found(%s)' % slug)
        return
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('apps/template.html')
    
    # Manifest
    data = ''
    with open ("apps/%s/manifest.json" % slug, "r") as manifest:
        data = manifest.read().replace('\n', '')
    context = json.loads(data)
    
    # Description
    description = ''
    with open ("apps/%s/description.md" % slug, "r") as desc_file:
        description = desc_file.read()
    
    context['description']= markdown.markdown(description)
    
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


    