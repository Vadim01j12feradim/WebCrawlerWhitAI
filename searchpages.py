import requests
from bs4 import BeautifulSoup
import sys, argparse
from lib.tmp import color as _
from lib.lib import Parser
from lib.sqlscan import sqli_scan
from lib.tmp import logo
from lib.tmp import color as c
from getIgames import GetFiles
from urllib.parse import urljoin
import urllib.parse
import getimagesToTrain as gitt
import trainModel as tm
import time
import probes as HTML
if sys.version[0] in '2':
   print('\n[x] Not Supported For python 2.x Please Use Python 3.x \n')
   exit()
try:
    import mechanicalsoup
    import requests
except Exception as e:
    print('\n{}[-]{} mechanicalsoup package Not Installed\n'.format(_.R,_.W))
    print('type pip3 install mechanicalsoup')
    exit()

urls = []

class crawl(object):
      auth = {
        1:[
            'https://www.google.com',
            'class="r"><a href="/url\?q=(.*?)&amp',
            'fl'
        ],
        2:[
            'https://www.bing.com',
            'h=".*?" href="(h.*?")',
            "b_widePag sb_bp"
        ]
      }
      def __init__(
        self,
        dork = "dead",
        proxy = None                
      ):  
          self.dork = dork #esta es la busqueda
          self.proxy = proxy
      def _urlValidation(self,url):
          try:
              parsedUrl = urllib.parse.urlparse(url)
              if parsedUrl.scheme and parsedUrl.netloc:
                #   print("Valid url")
                  return True
              else:
                #   print("Invalid url")
                  return False
          except ValueError:
            #   print("Invalid url")
              return False
      def Bing(self):
                bing = Parser(
                    self.dork,
                    crawl.auth[2][0],
                    crawl.auth[2][1],
                    crawl.auth[2][2],
                    proxy = self.proxy
                )
                bing.request()
                for url in dir(bing):
                    if 'go.microsoft.com' in url or 'bing.com' in url:
                        pass
                    else:
                        urls.append(url)       
      def Google(self):
          google = Parser(
            self.dork,
            crawl.auth[1][0],
            crawl.auth[1][1],
            crawl.auth[1][2],
            proxy = self.proxy
          )
          google.request()
          for url in dir(google):
              if 'go.microsoft.com' in url or 'bing.com' in url:
                 pass
              else:
                 urls.append(url) 
# theme = "billie eilish"
# theme = "Dwayne Johnson" m
theme =  "ariana grande"
gitt.searchData(theme,"yes")
gitt.searchData(theme,"no")
tm.trainModel()
_ = crawl(theme)
_.Bing()
_.Google()
numberOfPages = 50
HTML.init()
# _.DucDuckGo()
# urls = []
# u ="https://drive.google.com/drive/u/1/folders/1k-xZwRev8bDaUxdd7mI4eCbOh725K55W"
# urls.append(u)
urls_visited= []
if urls != []:
    while len(urls):
        url = urls[0]
        print('- {}'.format(url))
        urls_visited.append(url)
        urls.pop(0)
        try:
            r = requests.get(url)
            # Show html format
            # time.sleep(5)
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            if(GetFiles(url).search()):
                title = title = soup.find('title').text
                HTML.addTitle(title)
                md = soup.find('meta', attrs={'name': 'date'}) or soup.find('meta', attrs={'name': 'datePublished'})
                if md:
                    md = md['content']
                else:
                    md = "Date not especified"
                HTML.addDate(md)
                aut = soup.find('meta', attrs={'name': 'author'})
                if aut:
                    aut = aut['content']
                else:
                    aut = "Author no especified"
                HTML.addAut(aut)
                HTML.addLinkPage(url)
                dc = soup.find('meta', attrs={'name': 'description'})

                # Obtener el contenido de la etiqueta
                dc = dc['content']
                HTML.addDescription(dc)


            #Get all links
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href']) # join domain to path
                if full_url not in urls and full_url not in urls_visited:
                    if _._urlValidation(full_url):
                        urls.append(full_url)
                        # print("PUSH: ",full_url)
                # else:
                #     print("VISITED: ",full_url)
                # links.append(full_url)
            # print("Links: ",urls)


            #Header of page
            # print(r.headers) #show headers

            # Redirections to end in url finally
            # for redirect in r.history:
            #     print(redirect.url, redirect.status_code)
            # print(r.url, r.status_code)
            print("==============================  ( "+str(numberOfPages)+" ) ========================")
            numberOfPages -= 1
            if(numberOfPages == 0):
                break
        except Exception as e:
                 print("Has error in read page")
else:
    print('\n{}[-]{} No Url Found !\n'.format(c.R,c.W))

HTML.end()

# 143 not sleep