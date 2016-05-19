import falcon
from falcon_cors import CORS
import order
import upload

cors = CORS(allow_origins_list=['http://localhost:8080'], allow_methods_list=['POST', 'GET', 'PUT'])
api = application = falcon.API(middleware=[cors.middleware])

order_collection = order.Collection()
upload_collection = upload.Collection()

api.add_route('/order/', order_collection)
api.add_route('/order/{token}', order_collection)
api.add_route('/upload/{token}', upload_collection)
