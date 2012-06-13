from __future__ import unicode_literals, print_function
from common import *

import unittest
class _(unittest.TestCase):
    def setUp(self):
        debug("setUp")
    
    def test1(self):
        debug("test1")
        
    def tearDown(self):
        debug("tearDown")

if __name__ == "__main__":
    debug("__main__")

