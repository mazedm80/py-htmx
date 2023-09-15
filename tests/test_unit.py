"""
This module contains unit tests for the Bulldoggy app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from testlib.inputs import User

from app.utils.auth import deserialize_token, serialize_token

# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_token_serialization(user: User):
  token = serialize_token(user.username)
  assert token
  assert isinstance(token, str)
  assert token != user.username

  username = deserialize_token(token)
  assert username == user.username
