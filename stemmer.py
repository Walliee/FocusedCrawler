import Stemmer

def stemmer ( array ):
    stemmer = Stemmer.Stemmer('english')
    #result = stemmer.stemWords(array)
    #print result
    return stemmer.stemWords(array)