import falcon

from btree import BinaryTree
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

import btree

from trello import TrelloApi

class Collection (object):
	def on_post(self, req, resp, token):
		trello = TrelloApi('6eae854c8007ec32e40d67fb5ee455a7', token='6bcbba6ff807dfc62316d45ad7b00d7bce44e7c257a3574a7482f3dc666ad79d')
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
