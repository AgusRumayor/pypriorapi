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

class Collection (object):
	def on_post(self, req, resp):
		# req.stream corresponds to the WSGI wsgi.input environ variable,
        	# and allows you to read bytes from the request body.
        	#
        	# See also: PEP 3333
        	if req.content_length in (None, 0):
            		# Nothing to do
  	          	return

        	body = req.stream.read()
        	if not body:
            		raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        	try:
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
        	tree.jresp = {'remain':tree.unordered_list, 'item':tree.current.getNodeValue(), 'compare':tree.next, 'token':token,
		'PUT':[{"lt":"/order/%s/%s/%s"%(urllib.quote(token), tree.current.getNodeValue(), tree.next)}, 
		{"gt":"/order/%s/%s/%s"%(urllib.quote(token), tree.next, tree.current.getNodeValue())}]}
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
		print lst
		resp.body = json.dumps(lst)
		
	def on_put(self, req, resp, token, left, right):
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
		print "Nodo"+tree.current.getNodeValue()
		if left == tree.current.getNodeValue():
			if tree.current.getRightChild() == None:
				tree.current.insertRight(right)
				tree.current = tree.treeroot
				if len(tree.unordered_list)>0:
					tree.next = tree.unordered_list.pop()
				else:
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
					tree.next = "None"
			else:
				tree.current = tree.current.getLeftChild()
				print "2"+tree.current.getNodeValue()
		tree.jresp = {'remain':tree.unordered_list, 'item':tree.current.getNodeValue(), 'compare':tree.next, 'token':token,
		'PUT':[{"lt":"/order/%s/%s/%s"%(urllib.quote(token), tree.current.getNodeValue(), tree.next)},
		{"gt":"/order/%s/%s/%s"%(urllib.quote(token),tree.next, tree.current.getNodeValue())}]}
		transaction.commit()
		connection.close()
		db.close()
                storage.close()
		resp.body = json.dumps(tree.jresp)
