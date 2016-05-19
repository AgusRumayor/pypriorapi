import falcon
from falcon_cors import CORS
import order

cors = CORS(allow_origins_list=['http://localhost:8080'], allow_methods_list=['POST', 'GET', 'PUT'])
api = application = falcon.API(middleware=[cors.middleware])

collection = order.Collection()
api.add_route('/order/', collection)
#api.add_route('/order/{token}/{left}/{right}', collection)
api.add_route('/order/{token}', collection)
