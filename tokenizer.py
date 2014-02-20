from nltk.tokenize.punkt import PunktWordTokenizer
#from nltk.tokenize import regexp_tokenize
from bs4 import BeautifulSoup
import mechanize
from nltk.corpus import stopwords
import string

stopset = set(stopwords.words('english'))

def contentTokenizer ( url ):
    response = mechanize.urlopen(url)
    soup = BeautifulSoup(response.read())
    s = soup.findAll(text=True)
    #print s
    punct = set(string.punctuation)
    s = ''.join(x for x in s if x not in punct)
    s = s.lower()
    tokens = PunktWordTokenizer().tokenize(s)
    tokens = [w for w in tokens if not w in stopset]
    return tokens

def stringTokenizer ( s ):
    #string = "cat & dog"
    punct = set(string.punctuation)
    s = ''.join(x for x in s if x not in punct)
    s = s.lower()
    s = unicode(s)
    tokens = PunktWordTokenizer().tokenize(s)
    tokens = [w for w in tokens if not w in stopset]
    return tokens
