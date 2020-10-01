from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlsplit, urlparse, urlunparse, urljoin
from urllib.error import HTTPError, URLError
import json
links = set()
nbHTMLError = 0
nbURLError = 0
nbLoops = 0
nbunknownErrors = 0
nbMaxDepths = 0


class parseHTML(HTMLParser):
    def __init__(self):
        self.localLinks = set()
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                # If href is defined, print it.
                if "href" in attr[0] and not attr[1] in links:
                    self.localLinks.add(attr[1])


def crawl(myUrl,depth,maxdepth):
    global links
    global nbLoops
    global nbMaxDepths
    global nbHTMLError
    global nbURLError
    global nbunknownErrors
    if myUrl in links:
        nbLoops+=1
        #print('already seen ' + str(nbLoops))
    elif depth>maxdepth:
        nbMaxDepths+=1
        #print('reached max depth' + str(nbMaxDepths))
    else:
        links.add(myUrl)
        print('crawling depth ' + str(depth) + ' : ' + str(myUrl))
        try :
            response = urlopen(myUrl)
        except HTTPError:
            nbHTMLError+=1
        except URLError:
            nbURLError+=1
        except:
            nbunknownErrors+=1
        else:
            html = response.read()
            parser = parseHTML()
            parser.feed(html.decode('latin-1'))

            for currentLink in parser.localLinks:
                if currentLink[0 : 4] != "http":
                    nextLink = urljoin(myUrl,currentLink)
                else:
                    nextLink = currentLink
                crawl(nextLink,depth+1,maxdepth)
            print('already seen      : ' + str(nbLoops))
            print('reached max depth : ' + str(nbMaxDepths))
            print('http error        : ' + str(nbHTMLError))
            print('url error         : '+ str(nbURLError))
            print('unknown error     : '+ str(nbunknownErrors))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-d','--depth',type=int,default=3,help='max number of jumps')
    args = parser.parse_args()




    crawl(args.url,0,args.depth)
    print("DONE !")
