import webapp
import urllib.request

class cache(webapp.webApp):

    def __init__(self, hostname, port):
        self.cache = {}
        webapp.webApp.__init__(self, hostname, port)

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        lista = request.split()
        met = lista[0]
        rec = lista[1]
        return (met, rec)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        if parsedRequest[0] != "GET":
            return ("400 Bad Request", "<html><body><h1>Method not allowed</h1></body></html>")
        if parsedRequest in self.cache.keys():
            return ("200 OK", cache[parsedRequest[1]])
        else:
            url = "http:/" + parsedRequest[1]
            f = urllib.request.urlopen(url)
            html = f.read()
            self.cache[parsedRequest[1]] = html
            return ("200 OK", str(html))

if __name__ == '__main__':
    testCache = cache('localhost', 1234)
