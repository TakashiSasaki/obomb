from config import *

class _Test(TestCase):
    def setUp(self):
        debug("setUp")
    
    def test1(self):
        debug("test1")
        
    def tearDown(self):
        debug("tearDown")

if __name__ == "__main__":
    debug("__main__")

