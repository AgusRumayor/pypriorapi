import falcon
from falcon_cors import CORS
import order
import upload
import trellohandler

cors = CORS(allow_all_origins=True,allow_origins_list=['http://localhost:8000', 'http://localhost:8080', 'http://52.34.119.6'], allow_methods_list=['POST', 'GET', 'PUT'])
api = application = falcon.API(middleware=[cors.middleware])

order_collection = order.Collection()
upload_collection = upload.Collection()
board_collection = trellohandler.Boards()
lists_collection = trellohandler.Lists()

api.add_route('/order/', order_collection)
api.add_route('/order/{token}', order_collection)
api.add_route('/upload/{token}', upload_collection)
api.add_route('/trello/', board_collection)
api.add_route('/trello/{board}', lists_collection)
