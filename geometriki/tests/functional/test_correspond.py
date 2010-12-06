from geometriki.tests import *

class TestCorrespondController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='correspond', action='index'))
        # Test response...
