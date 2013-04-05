# developer.kippt.com

Developer site for [Kippt](https://kippt.com)'s API.

## Setup local environment

To setup local environment (requires git, virtualenv and pip)

    git clone https://github.com/kippt/developers.kippt.com.git
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

To run local version:

    python app.py

## Contribute 3rd party apps

If you have made an app or some other hack on top of Kippt's API, you can submit
that to app gallery. To do so, submit a pull request with your app's information:

    fab add

This will create necessary files and will instruct you to add image assets to
correct folders. After this you'll need to run ```fab render:<app_slug>```
command to generate the HTML for the app.

Once the app is compiled correctly, you'll need to compile the app directory
page:

    fab build_apps

__Need help?__ If you want Kippt's staff to add your app, contact us directly
and we'll take care of it for you.

## Lisence

This site is licensed under MIT. Feel free to use it as a base for your own site
but replace Kippt's copyrighted assets (logo) with your own. You'll want to also
use your own Typekit and Google Analytics.