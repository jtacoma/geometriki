# This file is part of geometriki.
#
# geometriki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# geometriki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with geometriki, in a file named COPYING. If not,
# see <http://www.gnu.org/licenses/>.
from helloworld.tests import *

class TestPagesController(TestController):

    def test_index(self):
        response = self.app.get(url('pages'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_pages', format='xml'))

    def test_create(self):
        response = self.app.post(url('pages'))

    def test_new(self):
        response = self.app.get(url('new_page'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_page', format='xml'))

    def test_update(self):
        response = self.app.put(url('page', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('page', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('page', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('page', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('page', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_page', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('edit_page', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_page', id=1, format='xml'))
