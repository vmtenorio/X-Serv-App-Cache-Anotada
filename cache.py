
import webapp
from urllib import request, error

class cache(webapp.webApp):

    def __init__(self, hostname, port):
        self.cache = {}
        self.httpServer = {}
        self.httpApp = {}
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

    def getServerHTTP(self, f, url):
        index = url.find("/", 8) # 8 para saltarse el http:// y buscar el recurso
        if index == -1: #Si no ha encontrado una barra es que pide el recurso principal /
            resource = "/"
        else:
            resource = url[index:]
        petition = "GET " + resource + " HTTP/1.1"
        response = "Status Code: " + str(f.getcode()) + "\n\nAsked URL: " + f.geturl()
        http = "<h1>Petition:</h1>\n\n" + petition + "\n\n<h1>Response:</h1>\n\n" + response
        return bytes(http,'utf-8')

    def getAppHTTP(self, req, html):
        response = "<h1>Request:</h1>\n\n" + req + "<h1>Response:</h1>\n\nHTTP/1.1 200 OK \r\n\r\nBODY:\n\n" + str(html)
        return bytes(response,'utf-8')

    def addRefs(self, html, rec):
        indexStartBody = html.find("<body")
        strBody = html[indexStartBody:]
        indexEndBody = strBody.find(">")
        start = html[:indexStartBody+indexEndBody+1]
        end = html[indexStartBody+indexEndBody+1:]
        refs = ("<a href='http:/" + rec + "'>Pagina original</a>" +
        "<br><a href='" + rec + "'>Recargar</a>" +
        "<br><a href='httpServer" + rec + "'>HTTP Servidor</a>" +
        "<br><a href='httpApp" + rec + "'>HTTP Cliente</a>")
        htmlRef = start + refs + end
        return bytes(htmlRef, 'utf-8')

    def process(self, met, rec, req):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        if met == None or rec == None:
            return ("400 Bad Request", bytes("<html><body><h1>That is not a valid URL</h1></body></html>", 'utf-8'))
        if met != "GET":
            return ("405 Method Not Allowed", bytes("<html><body><h1>Method not allowed</h1></body></html>", 'utf-8'))
        if rec.startswith("/httpServer"):
            pageIndex = rec.find("/",2)
            try:
                response = self.httpServer[rec[pageIndex:]]
            except KeyError:
                return ("400 Bad Request", bytes("<html><body><h1>URL Not Asked Yet</h1></body></html>", 'utf-8'))
            return ("200 OK", response)
        if rec.startswith("/httpApp"):
            pageIndex = rec.find("/",2)
            try:
                response = self.httpApp[rec[pageIndex:]]
            except KeyError:
                return ("400 Bad Request", bytes("<html><body><h1>URL Not Asked Yet</h1></body></html>", 'utf-8'))
            return ("200 OK", response)
        if rec in self.cache.keys():
            return ("200 OK", self.cache[rec])
        else:
            url = "http:/" + rec
            try:
                f = request.urlopen(url)
                html = f.read().decode('utf-8', 'ignore')
            except error.URLError:
                return ("400 Bad Request", bytes("<html><body><h1>That is not a valid URL</h1></body></html>", 'utf-8'))
            html = self.addRefs(html, rec)
            self.httpServer[rec] = self.getServerHTTP(f, url)
            self.httpApp[rec] = self.getAppHTTP(req, html)
            self.cache[rec] = html

            return ("200 OK", html)

if __name__ == '__main__':
    testCache = cache('localhost', 1234)
