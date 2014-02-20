import Stemmer

# Method for stemming tokens
def stemmer ( array ):
    stemmer = Stemmer.Stemmer('english')
    #result = stemmer.stemWords(array)
    #print result
    try:
        print "Stemming"
        return stemmer.stemWords(array)
    except:
        print "Stemming error"