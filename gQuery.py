from pygoogle import pygoogle
import urlnorm

def googleSearch ( searchString ):
    g = pygoogle(searchString)
    g.pages = 2
    urls = g.get_urls()
    urls = urls[:10]
    for i in range(len(urls)):
        urls[i]=urlnorm.norm(urls[i])

    return urls


