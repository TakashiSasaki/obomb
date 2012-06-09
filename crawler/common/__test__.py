from unittest import TestCase

class _(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        
    def test(self):
        print("_")
        pass
    
    def tearDown(self):
        TestCase.tearDown(self)
