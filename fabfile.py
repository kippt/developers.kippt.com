import re
import os
import json
from datetime import date

from fabric.operations import prompt
from fabric.api import run
from fabric.colors import green as _green, yellow as _yellow

def add():
    '''
    Add a new app
    '''
    print _green("--- Generating new app for Kippt App Gallery")
    
    name = prompt("App name:", default='', validate=r'^[\w\s-]+$')
    developer = prompt("Developer (your name/organization):", default='')
    platform = prompt("Platform (e.g. iOS):", default='')
    price = prompt("Price (e.g. $4):", default='')
    added = date.today().strftime('%B%e. %Y')
    link = prompt("Link (e.g. App Store or website):", default='')
    
    website = prompt("Website:", default='')
    twitter = prompt("Twitter (e.g. @getappname):", default='')
    
    data = {
        'name': name,
        'developer': developer,
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
    
    manifest = open("apps/%s/manifest.json" % slug, "w")
    manifest.write(json.dumps(data, indent=4))
    manifest.close()
    
    manifest = open("apps/%s/description.md" % slug, "w")
    manifest.write('This is %s.\n\nIt\'s time to add a markdown formatted description for the app.' % name)
    manifest.close()
    
    print _green('--- Saved to /apps/%s/' % slug)
    print _green('--- Remember to edit description.md and convert to html with')
    print _yellow('---     fab compile %s' % slug) 