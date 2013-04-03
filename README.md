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

This will create the manifest and description files. After this you'll need to run
```fab compile:<app_slug>``` command given the HTML for the app.

