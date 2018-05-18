from easy_search.core.crawler.server.data.mongodb.SearchEngineContext import SearchEngineContext
from easy_search.core.crawler.server.manager.document.elasticsearch.ElasticDocumentManager import ElasticDocumentManager
from easy_search.core.crawler.server.manager.document.solr.SOLRDocumentManager import SOLRDocumentManager
from easy_search.core.crawler.server.rest.base_http_handler.BasicHTTPServer import BasicHTTPServer
from easy_search.core.crawler.server.rest.flask.FlaskServer import FlaskServer
from easy_search.core.crawler.server.rest.pyramid.PyramidServer import PyramidServer
from easy_search.interfaces.crawler.index.IndexDocument import IndexDocument

context = SearchEngineContext("mongodb://192.168.163.129", "crawler_test")
document_manager = ElasticDocumentManager(context, '192.168.163.129:9200', 'test')
#document_manager = SOLRDocumentManager(context, 'http://192.168.163.129:8983/solr', 'test')


server = FlaskServer(__name__, IndexDocument, context, document_manager)
#server = PyramidServer(IndexDocument, context, document_manager)
#server = BasicHTTPServer(IndexDocument, context, document_manager)

if __name__ == '__main__':
    server.run(debug=True)
