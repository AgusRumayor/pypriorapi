import falcon

import json

from btree import BinaryTree
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

import btree

from trello import TrelloApi
import trelloconfig

class Boards (object):
	def on_get(self, req, resp):
		trello = TrelloApi(trelloconfig.api_key, token=trelloconfig.token)
		trello_token = trello.get_token_url('My App', expires='30days', write_access=True)
		response=trello.members.get_board('agusrumayor')
		boards= {}
		for board in response:
			boards[board['id']]=board['name']
		resp.body = json.dumps(boards)

class Lists (object):
	def on_get(self, req, resp, board):
		trello = TrelloApi(trelloconfig.api_key, token=trelloconfig.token)
		trello_token = trello.get_token_url('My App', expires='30days', write_access=True)
		response=trello.boards.get_list(board)
		lists= {}
		for lst in response:
			lists[lst['id']]=lst['name']
		resp.body = json.dumps(lists)
