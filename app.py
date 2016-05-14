import falcon

import order

api = application = falcon.API()

collection = order.Collection()
api.add_route('/order/', collection)
api.add_route('/order/{token}/{left}/{right}', collection)
api.add_route('/order/{token}', collection)
