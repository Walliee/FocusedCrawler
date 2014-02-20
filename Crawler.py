import urllib2
import urlparse
import gQuery
import urlnorm
from MyPriorityQueue import MyPriorityQueue
import time
import mechanize
import mimetypes
from os.path import splitext, basename
import priorityCalculator
import re
#from bs4 import BeautifulSoup, SoupStrainer


excludedExtentions = ['.png', '.jpg', '.jpeg', '.pdf', '.mp3', '.wmv', '.svg', '.ogg', '.ogv', '.py', '.tar.gz', '.ppt', '.zip', '.rar', '.ps']
excludedExtensions = set(excludedExtentions)
errorcount = 0
query = 'Torsten Suel'
top10urls = gQuery.googleSearch(query)
urls = MyPriorityQueue()
visited = {}
for i in range(len(top10urls)):
    urls.put(top10urls[i],1)

br = mechanize.Browser()
newurl = ""    
f = open('visited.txt','w+')
g = open('queue.txt', 'w+')
while not urls.empty() and len(visited) < 1000:
    try:
        for item in list(urls.queue):
            g.write(unicode(item) + "\n")
        g.write("#######################################################\n")
        url = urls.get()
        
        #print urls.qsize()
        match = re.match(r'javascript:+', url)
        if not visited.has_key(url) and match is None:
            print "adding to visited : " + url
            f.write("adding to visited : " + unicode(url)+"\n")
            f.flush()
            visited[url] = time.time()
            print len(visited)
            br.open(url, timeout=10.0)
            for link in br.links():
                newurl = urlparse.urljoin(link.base_url, link.url)
                newurl = unicode(urlnorm.norm(newurl))
                print "out: " + newurl
                disassembled = urlparse.urlsplit(newurl)
                filename, file_ext = splitext(basename(disassembled.path))
                file_ext = file_ext.lower()
                if(file_ext not in excludedExtensions and disassembled.scheme in ['http', 'https'] and disassembled.fragment == '' ):
                    print "in : " +newurl
                    priority = priorityCalculator.searchPage(newurl, query)
                    urls.put(newurl, priority)
                    if len(visited) >=1000:
                        break
    except:
        print "error 1"
        try:
            print unicode(newurl)
            errorcount += 1
        except:
            print "Error error"
    
    
print visited
print len(visited)
sorted_x = sorted(visited.items(), key=lambda x: x[1])
print sorted_x
print errorcount
f.close()
g.close()






    

