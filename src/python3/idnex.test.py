import uuid

from easy_search.core.server.index.manager.elasticsearch.ElasticDocumentManager import ElasticDocumentManager
from easy_search.core.server.index.manager.solr.SOLRDocumentManager import SOLRDocumentManager
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.index.communication.request.common.RangeCriteria import RangeCriteria
from easy_search.interfaces.server.index.communication.request.common.SearchCriteria import SearchCriteria


class TestDocument(IndexDocument):
    def __init__(self, unique_id: str, text: str, title: str, count: int) -> None:
        super().__init__(unique_id)
        self.text = text
        self.title = title
        self.count = count


docs = ElasticDocumentManager('192.168.163.129:9200', 'documents')
#docs = SOLRDocumentManager('http://192.168.163.129:8983/solr', 'test')
docs.index_object_type = TestDocument

unique_id = uuid.uuid4()
text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sodales commodo nulla.' \
    'Aliquam commodo mauris nec efficitur pharetra. Mauris iaculis erat id ultricies varius.' \
    ' Quisque diam enim, vulputate a blandit eget, interdum sit amet nisl. Pellentesque feugiat' \
    ' justo eu lobortis euismod. Cras eu efficitur eros. Suspendisse sed libero ante. Morbi sed' \
    ' ornare sapien. Fusce urna nulla, varius eu arcu sed, blandit vestibulum dolor. Nunc dapibus' \
    ' luctus erat sed posuere. Nullam iaculis quam ligula, sit amet elementum est vestibulum in' \
    '. Morbi vitae libero ac libero vestibulum vestibulum vitae egestas nisi.'
document = TestDocument(unique_id.hex,
                        text,
                        'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur', 10)
docs.add(document)

query = SearchQuery()
query.add_search_criteria(SearchCriteria('text', 'consectetur blandit'))
query.add_search_criteria(SearchCriteria('text', 'dolor dolorem', 2))
query.add_range_criteria(RangeCriteria('count', str(5), str(15)))
result = docs.search(query)
print(vars(result))
