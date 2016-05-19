import falcon
import msgpack
import json
from btree import BinaryTree
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
import uuid
import urllib
import btree
from pprint import pprint
class Collection (object):
	def on_post(self, req, resp):
		# req.stream corresponds to the WSGI wsgi.input environ variable,
        	# and allows you to read bytes from the request body.
        	#
        	# See also: PEP 3333
        	if req.content_length in (None, 0):
            		# Nothing to do
  	          	print "nothin"
			return
        	body = req.stream.read()
        	if not body:
            		raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        	try:
			pprint(body)
            		req.context['doc'] = json.loads(body.decode('utf-8'))
			token = str(uuid.uuid4())
                	storage = ZODB.FileStorage.FileStorage('trees/'+token+'.fs')
                  	db = ZODB.DB(storage)
                	connection = db.open()
                	root = connection.root
			unordered_list = req.context['doc']['data']
                	root.tree = BinaryTree(unordered_list.pop())
			tree = root.tree
			tree.unordered_list = unordered_list
			#tree.setList()
			if len(unordered_list) <2:
				raise falcon.HTTPBadRequest('Empty request body', 'We need more than 2 data elements')
        	except (ValueError, UnicodeDecodeError):
            		raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
		tree.current = tree
		tree.treeroot = tree.current
		tree.next = tree.unordered_list.pop()
        	tree.ordered = False
		tree.jresp = {'remain':tree.unordered_list, 'item':tree.current.getNodeValue(), 'compare':tree.next, 'token':token, 'ordered':tree.ordered,
		'links':[{"self":"/order/"},
		{'order':'/order/%s'%(urllib.quote(token))},
		{'lt':'/order/%s/%s/%s'%(urllib.quote(token), tree.current.getNodeValue(), tree.next)}, 
		{'gt':'/order/%s/%s/%s'%(urllib.quote(token), tree.next, tree.current.getNodeValue())}]}
		transaction.commit()
		connection.close()
		db.close()
		storage.close()
		resp.body = json.dumps(tree.jresp)
	
	def on_get(self, req, resp, token):
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
		tree.jresp = {'data':lst, 'item':tree.current.getNodeValue(), 'compare':tree.next, 'token':token, 'ordered':tree.ordered,
                'links':[{"new":"/order/"},
                {"self":"/order/%s"%(urllib.quote(token))},
                {"lt":"/order/%s/%s/%s"%(urllib.quote(token), tree.current.getNodeValue(), tree.next)},
                {"gt":"/order/%s/%s/%s"%(urllib.quote(token), tree.next, tree.current.getNodeValue())}]}
		transaction.commit()
		connection.close()
                db.close()
                storage.close()
		resp.body = json.dumps(tree.jresp)
		
	def on_put(self, req, resp, token):
		if req.content_length in (None, 0):
                        # Nothing to do
                        return

                body = req.stream.read()
                if not body:
                        raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

                try:
                        req.context['doc'] = json.loads(body.decode('utf-8'))
			left = req.context['doc']['left']
			right = req.context['doc']['right']
		except (ValueError, UnicodeDecodeError):
                        raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
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
		if tree.next not in [left, right]:
			resp.body = json.dumps(tree.jresp)
			connection.close()
			db.close()
                	storage.close()
			return
		if left == tree.current.getNodeValue():
			if tree.current.getRightChild() == None:
				tree.current.insertRight(right)
				tree.current = tree.treeroot
				if len(tree.unordered_list)>0:
					tree.next = tree.unordered_list.pop()
				else:
					tree.ordered = True
					tree.next = "None"
			else:
				tree.current = tree.current.getRightChild()
		elif right == tree.current.getNodeValue():
			if tree.current.getLeftChild()== None:
				tree.current.insertLeft(left)
				tree.current = tree.treeroot
				if len(tree.unordered_list)>0:
					tree.next = tree.unordered_list.pop()
				else:
					tree.ordered = True
					tree.next = "None"
			else:
				tree.current = tree.current.getLeftChild()
		tree.jresp = {'remain':tree.unordered_list, 'item':tree.current.getNodeValue(), 'compare':tree.next, 'token':token, 'ordered':tree.ordered,
		'links':[{"new":"/order/"},
                {"order":"/order/%s"%(urllib.quote(token))},
                {"lt":"/order/%s/%s/%s"%(urllib.quote(token), tree.current.getNodeValue(), tree.next)},
                {"gt":"/order/%s/%s/%s"%(urllib.quote(token), tree.next, tree.current.getNodeValue())}]}
		transaction.commit()
		connection.close()
		db.close()
                storage.close()
		resp.body = json.dumps(tree.jresp)
