import stemmer
import tokenizer
import math

def calcPriority( queryTf ):
    priority = len(queryTf)+1
    for tag in queryTf:
        if queryTf[tag] != 0:
            priority -=1
    return priority
    

url = "http://en.wikipedia.org/wiki/The_Big_Bang_Theory"
#string = "cats & Dogs"

def searchPage( url, string):
    tokens = stemmer.stemmer(tokenizer.contentTokenizer(url))
    print "Calculating priority for : " + url
    token_set = set(tokens)
    tf = {}
    queryTf = {}
    for word in token_set:
        tf[word] = float(tokens.count(word)) / len(tokens)
    #print tokenCount            
    searchTags = stemmer.stemmer(tokenizer.stringTokenizer(string))
    for tag in searchTags:
        if tf.has_key(tag):
            queryTf[tag] = tf.get(tag)
        else:
            queryTf[tag] = 0
    #print queryTf
    priority = calcPriority(queryTf)
    #print "Priority for " + url + " - " + priority        
    return priority
            
    #print queryCount            
        
#print searchPage(url, "Big Bang theory cast sheldon")
#print searchPage(url, "Big armadillo hello lol this")
#print searchPage(url, "hello")

 
    