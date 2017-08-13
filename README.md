# FS Mirror Utility

Useful utility to keep your FS images, documentations and Plugins up to date.

## prepare the virualenv

sudo pip install virtualenv

#### First time Setup

 Inside your cloned directory execute the following:

 virtualenv venv --system-site-packages
 source venv/bin/activate
 pip install -r requirements.txt

## Input:

Edit "config.yaml" file by editing ForeScout User / Pass Account provided by your ForeScout Account Manager  

You can select which files extensions to use: begin by downloading the .pdf and comment the remaining extensions.  

## Recurring execution

If environment already setup as per first step, just execute:

 source venv/bin/activate

## Download

python fsmirror.py download

## To verify:

python fsmirror.py verify

## Output:

  Crawls through the 5x Main download categories and downloads the updated versions

## to Exit virtualenv

 deactivate
