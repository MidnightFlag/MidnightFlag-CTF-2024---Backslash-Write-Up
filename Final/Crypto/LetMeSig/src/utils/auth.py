from functools import wraps
from flask import request, redirect, url_for
from base64 import b64decode
import sys

from utils.database import database
from utils.ecdsa import ecdsa

def unpack_token(token):
	try:
		user, sig = b64decode(token.encode()).decode().split(':')
		return user, sig	
	except:
		return None, None
		
def is_logged(user, sig):
	try:
		return ecdsa.verify(msg=user.encode(), sig=sig)
	except Exception as ex:
		print(ex, file=sys.stdout)
		return False

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		go_login = redirect(url_for('login'))
		try:
			token = request.cookies.get('token')
			if not token:
				return go_login

			user, sig = unpack_token(token)
			if not user or not sig:
				return go_login

			if not is_logged(user, sig):
				return go_login

			return f(*args, **kwargs)
		except Exception as ex:
			print(ex, sys.stdout)
			return go_login

		return decorated
	return decorated