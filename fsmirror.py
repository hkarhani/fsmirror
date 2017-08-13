#!/usr/bin/env python
import os
import sys
import yaml
import shutil
import requests 
from requests.auth import HTTPBasicAuth
from BeautifulSoup import BeautifulSoup
from more_itertools import unique_everseen
from urlparse import urljoin

class FSMirror(object):
    """ForeScout Mirror Utility main class:

    Attributes:
        user: UserName used to access updates web site.
        password: Password used to access updates web site.
        url (optional): default base URL: https://updates.forescout.com/support/index.php?url=counteract
        categories (auto-populated): [{cateory:'', url:'', folder:''}]

    """

    def __init__(self, user, password, extensions=['.pdf', '.iso', '.img', '.fpi'], 
                 url='https://updates.forescout.com/support/index.php?url=counteract'):
        """Returns FSMirror object with credentials provided, with url override capability."""
        self.user = user
        self.password = password 
        self.url = url
        self.extensions = extensions 
        self.initCategories()

    def initCategories(self, category = None):
        """Populates categories list. """
        if category == None: 
            self.categories = []
            r = requests.get(self.url, auth=HTTPBasicAuth(self.user, self.password))
            data = r.text
            soup = BeautifulSoup(data)
            _urls = []
            _urlFilters = ['section=', 'version=']

            for link in soup.findAll('a'):
                href = link.get('href')
                for ext in _urlFilters:
                    if str(href).find(ext)!=-1:
                        _urls.append(str(href))

            _uniqueUrls = list(unique_everseen(_urls))

            for link in _uniqueUrls:
                _tmpUrl = urljoin(self.url, link)
                path, p1 = os.path.split(_tmpUrl)
                if p1.find('section=')!=-1 and p1.find('version=')!=-1: 
                    dest_section = p1[p1.find('section=')+8:p1.find('&', p1.find('section='))]
                    dest_version = p1[p1.find('version=')+8:len(p1)]
                    dest_folder = dest_section+"_"+dest_version
                _cat = {'category': dest_section, 'url': _tmpUrl, 'folder': dest_section, 'version':dest_version}
                self.categories.append(_cat)
                
            # to implement individual category update in future release
        
        return self.categories
    
    def getCategories(self):
        """Extracts a list of populated categories (name only)."""
        if self.categories == None: 
            return None
        
        _catList = []
        for cat in self.categories:
            _catList.append(cat['category'])
        
        return _catList
    
    def getCategory(self, category=None):
        """Extract a Category by its category name."""
        if category == None: 
            return None 
        
        for cat in self.categories: 
            if cat['category'] == category: 
                return cat 
        
        return None 
    
    def downloadCategories(self):
        for cat in self.categories:
            self.downloadCategory(cat['category'])
    
    def verifyCategories(self):
        for cat in self.categories:
            self.verifyCategory(cat['category'])
            
    def downloadCategory(self, category):
        _cat = self.getCategory(category)
        
        if _cat == None:
            return None 
        
        print "\nDownloading from %s:" % category 
        _r = requests.get(_cat['url'], auth=HTTPBasicAuth(self.user, self.password))
        _data = _r.text
        _soup = BeautifulSoup(_data)
        _urls = []
        for link in _soup.findAll('a'):
            href = link.get('href')
            for ext in self.extensions:
                if str(href).find(ext)!=-1 and str(href).startswith('/'):
                    _urls.append(str(href))
        _uniqueUrls = list(unique_everseen(_urls))
        print len(_uniqueUrls)
        
        _uniqueUrlsNorm = [] 
        
        if not os.path.isdir(os.path.join(os.getcwd(), _cat['folder'])):
            print "\nCreating directory: %s" % _cat['folder']
            os.mkdir(os.path.join(os.getcwd(), _cat['folder']))
        
        dest_url = os.path.join(os.getcwd(), _cat['folder'])
        
        for link in _uniqueUrls:
            path,file_=os.path.split(link)
            sourceURL = urljoin(_cat['url'], link)

            path,version_=os.path.split(path)
            if file_.find(version_)==-1:
                path, version_major = os.path.split(path)
                path, plugin_name = os.path.split(path)
                if file_.find(version_major)==-1:
                    destURL = "%s/%s-%s-%s" %(dest_url, plugin_name, version_, file_)
                else: 
                    destURL = "%s/%s" %(dest_url, file_)
            else: 
                destURL = "%s/%s" %(dest_url, file_)
            
            #print destURL
            self.downloadFile(sourceURL, destURL)
            
        print "\nFinished updating %s." % category
    
    def verifyCategory(self, category):
        _cat = self.getCategory(category)
        
        if _cat == None:
            return None 
        
        print "\nVerifying from %s:" % category 
        _r = requests.get(_cat['url'], auth=HTTPBasicAuth(self.user, self.password))
        _data = _r.text
        _soup = BeautifulSoup(_data)
        _urls = []
        for link in _soup.findAll('a'):
            href = link.get('href')
            for ext in self.extensions:
                if str(href).find(ext)!=-1 and str(href).startswith('/'):
                    _urls.append(str(href))
        _uniqueUrls = list(unique_everseen(_urls))
        print "\nVerifying: %d files." % len(_uniqueUrls)
        
        _uniqueUrlsNorm = [] 
        
        if not os.path.isdir(os.path.join(os.getcwd(), _cat['folder'])):
            print "\nCreating directory: %s" % _cat['folder']
            os.mkdir(os.path.join(os.getcwd(), _cat['folder']))
        
        dest_url = os.path.join(os.getcwd(), _cat['folder'])
        
        for link in _uniqueUrls:
            path,file_=os.path.split(link)
            sourceURL = urljoin(_cat['url'], link)

            path,version_=os.path.split(path)
            if file_.find(version_)==-1:
                path, version_major = os.path.split(path)
                path, plugin_name = os.path.split(path)
                if file_.find(version_major)==-1:
                    destURL = "%s/%s-%s-%s" %(dest_url, plugin_name, version_, file_)
                else: 
                    destURL = "%s/%s" %(dest_url, file_)
            else: 
                destURL = "%s/%s" %(dest_url, file_)
            
            #print destURL
            try: 
                result = self.verifyFile(sourceURL, destURL)
                if not result: 
                    path, _file = os.path.split(destURL)
                    print "\nFile %s is either corrupted or not existing!" % _file
                else: 
                    print ".",
            except:
                print "\nError while verfying file: %s " % destURL
            
        print "\nFinished verifying %s." % category
            
    def downloadFile(self, url, destFile):
        """Downloads the specified URL and saves the content in destFile. """
        if os.path.isfile(destFile): 
            # Adds auto-files version/size-checking in the future
            print ".", 
            #print "%s: File exists!" % destFile
            return True 
        else: 
            path, _file = os.path.split(destFile)
            print "\nDownloading %s..." %(_file)

        response = requests.get(url, auth=HTTPBasicAuth(self.user, self.password), stream=True)

        with open(destFile, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print "."

        del response
    
    def verifyFile(self, url, destFile):
        """Compares the Size of the file specified in URL and the size of the saved destFile."""
        if os.path.isfile(destFile): 
            # Adds auto-files Checksum in the future
            _fileSize = os.path.getsize(destFile)
            #print "%s: File exists - Size: %s" % (destFile, _fileSize)
        else: 
            return False 

        respFileSize = requests.get(url, auth=HTTPBasicAuth(self.user, self.password), stream=True).headers['Content-length']
        #print "URL file has size: %d" % int(respFileSize)
        return int(respFileSize) == int(_fileSize)



if __name__ == "__main__":
    """Main function in case this module is executed. By default loads configuration from config.yaml."""

    args = sys.argv[1:]
    
    if len(args) > 0: 
        if args[0] == 'verify':
            with open("config.yaml", 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    #print(config)
                except yaml.YAMLError as exc:
                    print(exc)
                
                fsm = FSMirror(user=config['user'], password=config['password'], extensions=config['extensions'], url=config['url'])
                fsm.verifyCategories()

        elif args[0] == 'download':
            with open("config.yaml", 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    #print(config)
                except yaml.YAMLError as exc:
                    print(exc)
                
                fsm = FSMirror(user=config['user'], password=config['password'], extensions=config['extensions'], url=config['url'])
                fsm.downloadCategories()
            

    


