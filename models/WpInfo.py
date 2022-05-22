import json
from flask import Flask
from flask import request


from flask import Response
import pydig
import requests
import urllib.parse
import pathlib

app = Flask(__name__)
path = pathlib.Path(__file__).parent.resolve()

class WpInfo():
    def __init__(self):
        label = 'WordPress Content'
        self.label = label
        self.system = 'WordPress'
 

    def get_all_posts(self,url, route):
        api_url = url + str('/wp-json/wp/v2/'+route) 
    #    print (api_url)
        r =requests.get(api_url)
        posts_data = {}
        posts_data['url'] = api_url
        posts_data['total'] = r.headers.get('X-WP-Total')
        posts_data['pagination'] = r.headers.get(' X-WP-TotalPages')
        posts_data['posts'] = self.pagination(posts_data['pagination'], posts_data['total'], api_url)
        
        return (posts_data)




    def get_admin_url(self,url):

        api_url = url + str('/wp-admin/') 
        r =requests.head(api_url, allow_redirects=True)
        parsed_url = urllib.parse.urlparse(r.url)
        return parsed_url.path


    def pagination(self, pages, total, url):
        pagination = 1
        results = []
        if (isinstance(total, int) and isinstance(pages, int)):
            per_page = int(total) * int(pages)

            
            while int(pagination) <= int(pages):
                
                params = {'per_page': 10, 'page': pagination}
                r =requests.get(url,params=params)
                data = r.json()
                for i in data:
                    results.append(i)
                
                pagination  = pagination +1
        else:
                params = {'per_page': 10, 'page': pagination}
                r =requests.get(url,params=params)
                data = r.json()
                for i in data:
                    results.append(i)     
        return results

    def get_nwst(self,posts, field):
       # print (type(posts['posts']))
        newlist = sorted(posts['posts'], key=lambda d: d[field])
        self.nwst = newlist[0]['date']
        return self.nwst

    def get_oldest(self,posts, field):
        newlist = sorted(posts['posts'], key=lambda d: d[field], reverse=True) 
        self.oldest = newlist[0]['date']
        return self.oldest
        

class TechnicalInfo():
    def __init__(self, domain, parsed_url):
        label = 'Technische Informationen'
        self.label = label
        self.domain = domain
        self.protocol = parsed_url.scheme
        self.netloc = parsed_url.netloc

    def run(self):
        self.ip = pydig.query(self.netloc, 'A')
        self.txt = pydig.query(self.netloc, 'txt')
        headers = requests.get(self.domain).headers
        self.server = headers['Server']
       # self.link = headers['link']

        if(([x for x in self.txt if 'spf' in x])):
            self.spf = 'True'

        if(([x for x in self.txt if 'dkim' in x])):
            self.dkim = 'False'










