import falcon

import json

from btree import BinaryTree
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

import btree

from trello import TrelloApi

class Boards (object):
	def on_get(self, req, resp):
		trello = TrelloApi('6eae854c8007ec32e40d67fb5ee455a7', token='6bcbba6ff807dfc62316d45ad7b00d7bce44e7c257a3574a7482f3dc666ad79d')
		trello_token = trello.get_token_url('My App', expires='30days', write_access=True)
		response=trello.members.get_board('agusrumayor')
		boards= {}
		for board in response:
			boards[board['id']]=board['name']
		resp.body = json.dumps(boards)

class Lists (object):
	def on_get(self, req, resp, board):
		trello = TrelloApi('6eae854c8007ec32e40d67fb5ee455a7', token='6bcbba6ff807dfc62316d45ad7b00d7bce44e7c257a3574a7482f3dc666ad79d')
		trello_token = trello.get_token_url('My App', expires='30days', write_access=True)
		response=trello.boards.get_list(board)
		lists= {}
		for lst in response:
			lists[lst['id']]=lst['name']
		resp.body = json.dumps(lists)
