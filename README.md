# developer.kippt.com

Developer site for [Kippt](https://kippt.com)'s API. 

## Setup local environment

To setup local environment (requires git, virtualenv and pip)

    git clone https://github.com/kippt/developer.kippt.com.git
    virtualenv ENV
    . ENV/bin/activate
    pip install -r requirements.txt

To run local version:

    python app.py

## Contribute 3rd party apps

If you have made an app or some other hack on top of Kippt's API, you can submit
that to app gallery. To do so, submit a pull request with your app's information:

1. Create a folder under ```gallery/apps``` and copy templates from ```gallery/apps/template```
2. Modify files with your app's information
3. Profit.
