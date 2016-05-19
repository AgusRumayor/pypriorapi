import falcon

from btree import BinaryTree
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

import btree

from trello import TrelloApi
import trelloconfig

class Collection (object):
	def on_post(self, req, resp, token):
		trello = TrelloApi(trelloconfig.api_key, token=trelloconfig.token)
		trello_token = trello.get_token_url('My App', expires='30days', write_access=True)
		storage = ZODB.FileStorage.FileStorage('trees/'+token+'.fs')
             	db = ZODB.DB(storage)
                connection = db.open()
                root = connection.root
		if hasattr(root, 'tree'):
                        tree = root.tree
                else:
                        resp.body = "Initialize first"
                        connection.close()
                        db.close()
                        storage.close()
                        return
		lst = list(btree.inorder(tree))
		connection.close()
                db.close()
                storage.close()
		if len(lst)> 0:
			id_new = trello.boards.new_list('E3LNxfKb', token)['id']
		for card in lst:
			trello.cards.new(card, id_new)
