from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlsplit, urlparse, urlunparse, urljoin
from urllib.error import HTTPError, URLError
from multiprocessing import Queue
from multiprocessing.context import Process
from multiprocessing import Pool
links = set()
nbHTMLError = 0
nbURLError = 0
nbLoops = 0
nbunknownError = 0
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


def crawl(myUrl, depth, maxdepth):
    print(myUrl)
    print(depth)
    print(maxdepth)
    if myUrl in links:
        nbLoops+=1
        #print('already seen ' + str(nbLoops))
    elif depth>maxdepth:
        nbMaxDepths+=1
        #print('reached max depth' + str(nbMaxDepths))
    else:
        global nbHTMLError
        global nbURLError
        global nbunknownError
        print('crawling depth ' + str(depth) + ' : ' + str(myUrl))
        links.add(myUrl)
        try :
            response = urlopen(myUrl)
        except HTTPError:
            nbHTMLError+=1
        except URLError:
            nbURLError+=1
        except:
            nbunknownError+=1
        else:
            html = response.read()
            parser = parseHTML()
            parser.feed(html.decode('latin-1'))

            for currentLink in parser.localLinks:
                if currentLink[0 : 4] != "http":
                    queue.put((urljoin(myUrl,currentLink),depth+1,maxdepth))
                else:
                    queue.put(currentLink,depth+1,maxdepth)


        print('already seen      : ' + str(nbLoops))
        print('reached max depth : ' + str(nbMaxDepths))
        print('http error        : ' + str(nbHTMLError))
        print('url error         : '+ str(nbURLError))
        print('unknown error     : '+ str(nbunknownError))
        print (queue.qsize())

        test = "yeah"
        '''while(test!=None):
            print(test)
            test = queue.get(True, 2)
            print (queue.qsize())'''



def crawlController(myUrl,depth,maxdepth):
    global links
    global nbLoops
    global nbMaxDepths
    global nbHTMLError
    global nbURLError
    global nbunknownError
    print("entered controller")
    queue = Queue()

    queue.put((myUrl,depth,maxdepth))
    with Pool() as pool:
        while True:
            qval = queue.get()
            print(qval)
            p = pool.apply_async(crawl,args=qval)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-d','--depth',type=int,default=3,help='max number of jumps')
    args = parser.parse_args()
    crawlController(args.url,0,args.depth)
    print("DONE !")
