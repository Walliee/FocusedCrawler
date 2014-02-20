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

# Extensions to be avoided
excludedExtentions = ['.png', '.jpg', '.jpeg', '.pdf', '.mp3', '.wmv', '.svg', '.ogg', '.ogv', '.py', '.tar.gz', '.ppt', '.zip', '.rar', '.ps']
excludedExtensions = set(excludedExtentions)    # Making set for easy membership test

errorcount = 0
query = 'Torsten Suel'  # Initial query for focused crawler
top10urls = gQuery.googleSearch(query)

urls = MyPriorityQueue()    # Queue for storing URLs yet to be visisted
visited = {}    # Dictionary structure for storing visited URLs

for i in range(len(top10urls)): # Adding top 10 results to Queue
    urls.put(top10urls[i],1)

br = mechanize.Browser()
newurl = ""    
f = open('visited.txt','w+')
g = open('queue.txt', 'w+')

while not urls.empty() and len(visited) < 1000:     # Crawl till queue empty or target visited count is reached
    try:
        for item in list(urls.queue):
            g.write(unicode(item) + "\n")
        g.write("#######################################################\n")
        url = urls.get()    # Fetch URL with highest possible priority while preserving insertion order
        
        #print urls.qsize()
        match = re.match(r'javascript:+', url)      # Check for Javascript
        if not visited.has_key(url) and match is None:
            print "adding to visited : " + url
            f.write("adding to visited : " + unicode(url)+"\n")
            f.flush()
            visited[url] = time.time()
            print len(visited)
            br.open(url, timeout=10.0)
            for link in br.links():
                newurl = urlparse.urljoin(link.base_url, link.url)      # Converting relative URLs to Absolute ones
                newurl = unicode(urlnorm.norm(newurl))      # Normalizing URL
                print "out: " + newurl
                disassembled = urlparse.urlsplit(newurl)
                filename, file_ext = splitext(basename(disassembled.path))      # Finding file extension for filtering exclusions
                file_ext = file_ext.lower()
                if(file_ext not in excludedExtensions and disassembled.scheme in ['http', 'https'] and disassembled.fragment == '' ):
                    print "in : " +newurl
                    priority = priorityCalculator.searchPage(newurl, query)
                    urls.put(newurl, priority)      # Adding URL to queue with calculated priority
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






    

