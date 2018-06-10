from easy_search.core.server.index.manager.elasticsearch.ElasticDocumentManager import ElasticDocumentManager
from easy_search.core.server.job.data.mongodb.SearchEngineContext import SearchEngineContext
from easy_search.core.server.rest.base_http_handler.BasicHTTPServer import BasicHTTPServer
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument

class TestDocument(IndexDocument):
    def __init__(self, unique_id: str, text: str, title: str, count: int) -> None:
        super().__init__(unique_id)
        self.text = text
        self.title = title
        self.count = count

context = SearchEngineContext("mongodb://192.168.163.129", "crawler_test")
document_manager = ElasticDocumentManager('192.168.163.129:9200', 'documents')
#document_manager = SOLRDocumentManager('http://192.168.163.129:8983/solr', 'test')


#server = FlaskServer(__name__, IndexDocument, context, document_manager)
#server = PyramidServer(IndexDocument, context, document_manager)
server = BasicHTTPServer(TestDocument, context, document_manager)

if __name__ == '__main__':
    server.run_dev("127.0.0.1", debug=True)
