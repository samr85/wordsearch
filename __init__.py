import os
from tornado.web import StaticFileHandler
from .wordsearchSolver import wordsearchSolver

requests = [
    # Match against anything specified after regexWordList, treating the entire rest of the string as the regex
    (r"/wordsearchSolver", wordsearchSolver),
    (r"/static/wordsearchSolver/(.*)", StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static/wordsearchSolver")})
]
