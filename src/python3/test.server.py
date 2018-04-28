from core.src.crawler.server.data.mongodb.SearchEngineContext import SearchEngineContext
from core.src.crawler.server.rest.base_http_handler.BasicHTTPServer import BasicHTTPServer
from core.src.crawler.server.rest.flask.FlaskServer import FlaskServer
from core.src.crawler.server.rest.pyramid.PyramidServer import PyramidServer

context = SearchEngineContext("mongodb://192.168.163.129", "crawler_test")
#server = FlaskServer(__name__, context)
#server = PyramidServer(context)
server = BasicHTTPServer(context)

if __name__ == '__main__':
    server.run(debug=True)
