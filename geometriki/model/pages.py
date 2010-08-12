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
import codecs
import os

import formencode
from pylons import config

from geometriki.lib.helpers import rst2html, rst2data

class Page (object):

    def __init__(self, name, title=None, content=None):
        self.path = os.path.join(config['pages_dir'], name)
        self.name = name
        self.title = title or name

    def exists(self):
        return os.path.exists(self.path)

    def get_raw_content(self):
        if hasattr(self, 'content'): return self.content
        if not self.exists(): return None
        return codecs.open(self.path, 'r', 'utf-8').read()

    def get_formatted_content(self):
        content = self.get_raw_content()
        formatted = rst2html(content)
        return formatted

    def get_structured_content(self):
        content = self.get_raw_content()
        data = rst2data(content)
        return data

    def has_changes(self):
        return hasattr(self, 'content')

    def save(self):
        if hasattr(self, 'content'):
            _ensure_pages_dir()
            f = codecs.open(self.path, mode='w', encoding='utf-8')
            f.write(self.content)
            f.close()
            del self.content

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

def get_page_list():
    pages_dir = config['pages_dir']
    pages = [Page(filename) for filename in os.listdir(pages_dir) if not filename.startswith('.')]
    pages.sort(lambda a, b: cmp(a.name, b.name))
    return pages

def get_page(name):
    return Page(name)

def _ensure_pages_dir():
    pages_dir = config['pages_dir']
    if not os.path.exists(pages_dir):
        os.makedirs(pages_dir)

class PageUpdateForm (formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = False
    content = formencode.validators.String()

class PageCreateForm (formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = False
    name = formencode.validators.String()
    content = formencode.validators.String()
