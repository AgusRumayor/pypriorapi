import falcon
from falcon_cors import CORS
import order
import upload
import trellohandler

cors = CORS(allow_origins_list=['http://localhost:8080'], allow_methods_list=['POST', 'GET', 'PUT'])
api = application = falcon.API(middleware=[cors.middleware])

order_collection = order.Collection()
upload_collection = upload.Collection()
board_collection = trellohandler.Boards()
lists_collection = trellohandler.Lists()
cards_collection = trellohandler.Cards()

api.add_route('/order/', order_collection)
api.add_route('/order/{token}', order_collection)
api.add_route('/upload/{token}', upload_collection)
api.add_route('/board/', board_collection)
api.add_route('/list/{board}', lists_collection)
api.add_route('/card/{lst}', cards_collection)
