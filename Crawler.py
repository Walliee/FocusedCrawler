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
import stemmer
import tokenizer
import hashlib
#from bs4 import BeautifulSoup, SoupStrainer

# Extensions to be avoided
excludedExtentions = ['.png', '.jpg', '.jpeg', '.pdf', '.mp3', '.wmv', '.svg', '.ogg', '.ogv', '.py', '.tar.gz', '.gz', '.ppt', '.zip', '.rar', '.ps', '.ppsx']
excludedExtensions = set(excludedExtentions)    # Making set for easy membership test

errorcount = 0
query = 'Nasir Memon'  # Initial query for focused crawler
searchTags = stemmer.stemmer(tokenizer.stringTokenizer(query))  # Stemming and tokenizing search query to avoid duplicate effort
print "Search tokens : "
print searchTags

top10urls = gQuery.googleSearch(query)

urls = MyPriorityQueue()    # Queue for storing URLs yet to be visisted
visited = {}    # Dictionary structure for storing visited URLs

for i in range(len(top10urls)): # Adding top 10 results to Queue
    urls.put(top10urls[i],1)

br = mechanize.Browser()
newurl = ""    
f = open('visited.txt','w+')
g = open('queue.txt', 'w+')
h = open('error.txt', 'w+')


while not urls.empty() and len(visited) < 100:     # Crawl till queue empty or target visited count is reached
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
            s = hashlib.sha1()
            s.update(url)
            fileloc = "Downloads/" + s.hexdigest() + ".txt"     #downloading html
            j = open(fileloc, 'w+')
            j.writelines(br.response().read())
            j.close()
            #j.write("###################################################################################")
            for link in br.links():
                newurl = urlparse.urljoin(link.base_url, link.url)      # Converting relative URLs to Absolute ones
                newurl = unicode(urlnorm.norm(newurl))      # Normalizing URL
                print "out: " + newurl
                disassembled = urlparse.urlsplit(newurl)
                filename, file_ext = splitext(basename(disassembled.path))      # Finding file extension for filtering exclusions
                file_ext = file_ext.lower()
                if(file_ext not in excludedExtensions and disassembled.scheme in ['http', 'https'] and disassembled.fragment == '' ):
                    print "in : " +newurl
                    if not urls.inQueue(newurl):        # Checking to see if URL has already been queued once
                        priority = priorityCalculator.searchPage(newurl, searchTags)
                        urls.put(newurl, priority)      # Adding URL to queue with calculated priority
                        if len(visited) >=100:
                            break
    except mechanize.RobotExclusionError as e:
        print "mechanize error({0}): {1}".format(e.errno, e.strerror)
        try:
            print unicode(newurl)
            errorcount += 1
            #h.write(errorcount +" \n ")
            h.write("Page disallowed by robots.txt  : ")
            h.write(unicode(newurl) + "\n")
            h.flush()
        except:
            print "Error error"
    except:
        print "other error"
    
    
print visited
print len(visited)
sorted_x = sorted(visited.items(), key=lambda x: x[1])
print sorted_x
print errorcount
f.close()
g.close()
h.close()







    

