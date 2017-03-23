import webapp
from urllib import request, error

class cache(webapp.webApp):

    def __init__(self, hostname, port):
        self.cache = {}
        self.httpServer = {}
        self.httpClient = {}
        webapp.webApp.__init__(self, hostname, port)

    def parse(self, req):
        """Parse the received request, extracting the relevant information."""
        lista = req.split()
        try:
            met = lista[0]
            rec = lista[1]
        except IndexError:
            met = None
            rec = None
        return (met, rec)

    def getServerHTTP(self, f):
        return bytes("CODE" + str(f.getcode()) +
                        "Asked URL: " + f.geturl(),'utf-8')

    def getClientHTTP(self, f):
        return bytes(str(f.getcode()) + f.geturl(),'utf-8')

    def addRefs(self, html, rec):
        indexStartBody = html.find("<body")
        strBody = html[indexStartBody:]
        indexEndBody = strBody.find(">")
        start = html[:indexStartBody+indexEndBody+1]
        end = html[indexStartBody+indexEndBody+1:]
        refs = ("<a href='http:/" + rec + "'>Pagina original</a>" +
        "<br><a href='" + rec + "'>Recargar</a>" +
        "<br><a href='httpServer" + rec + "'>HTTP Servidor</a>" +
        "<br><a href='httpClient" + rec + "'>HTTP Cliente</a>")
        htmlRef = start + refs + end
        return bytes(htmlRef, 'utf-8')

    def process(self, met, rec):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        if met == None or rec == None:
            return ("400 Bad Request", bytes("<html><body><h1>That is not a valid URL</h1></body></html>", 'utf-8'))
        if met != "GET":
            return ("405 Method Not Allowed", bytes("<html><body><h1>Method not allowed</h1></body></html>", 'utf-8'))
        if rec.startswith("/httpServer"):
            pageIndex = rec.find("/",2)
            return ("200 OK", self.httpServer[rec[pageIndex + 1:]])
        if rec.startswith("/httpClient"):
            pageIndex = rec.find("/",2)
            return ("200 OK", self.httpClient[rec[pageIndex + 1:]])
        if rec in self.cache.keys():
            return ("200 OK", self.cache[rec])
        else:
            url = "http:/" + rec
            try:
                f = request.urlopen(url)
                html = f.read().decode('utf-8')
            except error.URLError:
                return ("400 Bad Request", bytes("<html><body><h1>That is not a valid URL</h1></body></html>", 'utf-8'))
            html = self.addRefs(html, rec)
            self.httpServer[rec] = self.getServerHTTP(f)
            self.httpClient[rec] = self.getClientHTTP(request)
            self.cache[rec] = html

            return ("200 OK", html)

if __name__ == '__main__':
    testCache = cache('localhost', 1234)
