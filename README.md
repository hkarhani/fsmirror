# FS Mirror Utility

Useful utility to keep your FS images, documentations and Plugins up to date.

## prepare the virualenv

```
 sudo pip install virtualenv
```
#### First time Setup

 Inside your cloned directory execute the following (Linux / MacOS):

```
 virtualenv venv --system-site-packages
 source venv/bin/activate
 pip install -r requirements.txt
```

For Windows execute the following:

```
 virtualenv venv --system-site-packages
 .\venv\Scripts\activate
 pip install -r requirements.txt
```
## Input:

Edit "config.yaml" file by editing ForeScout User / Pass Account provided by your ForeScout Account Manager  
```
description: Please fill user and password fields in the following. You may customize sections / extensions if needed.
user:   <-- Enter the Given User
password: <-- Enter the Given Password
sections:
    - product_download   # you can deselect Category by adding '#' in front of the line
    - installation_guides
    - user_manuals
    - plugins
    - plugins_modules
extensions:
    - .pdf
    - .fpi
    - .img
    - .iso
url: https://updates.forescout.com/support/index.php?url=counteract

```
You can select which files extensions to use: begin by downloading the .pdf and comment the remaining extensions.  

## Recurring execution

If environment already setup as per first step, just execute:

Linux / MacOS:
 ```
   source venv/bin/activate
 ```
 Windows:

 ```
   .\venv\Scripts\activate
 ```

## Download
```
 python fsmirror.py download
```
## To verify:
```
 python fsmirror.py verify
```
## Output:

  Crawls through the 5x Main download categories and downloads the updated versions

## to Exit virtualenv
```
 deactivate
```
