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

from geometriki.lib.rst import rst2html, rst2json, rst2data

_JAVASCRIPT_TEMPLATE = r"""
geometriki.pages["%(name)s"] = {
    "name": "%(name)s",
    "data": %(json)s
};
if (!("page" in geometriki) || typeof(geometriki.page) == "undefined")
    geometriki.page = geometriki.pages["%(name)s"];
$(function () {
    geometriki.message("Script loaded for <strong>" + geometriki.page.name + "</strong>.");
});"""

_JAVASCRIPT_ERROR_TEMPLATE = r"""$(function () {
    geometriki.error("Failed to generate script for <strong>%(name)s</strong>.");
});"""

class Page (object):

    def __init__(self, name, title=None, content=None):
        self.name = name
        self.title = title or name

    def _get_path(self):
        return os.path.join(config['pages_dir'], self.name)

    def exists(self):
        return self.name and os.path.exists(self._get_path())

    def get_raw_content(self):
        if '/' in self.name or self.name.startswith('.'):
            raise Exception("Invalid page name: %r" % self.name)
        if hasattr(self, 'content'): return self.content
        if not self.exists(): return None
        return codecs.open(self._get_path(), 'r', 'utf-8').read()

    def get_formatted_content(self):
        content = self.get_raw_content()
        formatted = rst2html(content)
        return formatted

    def get_data(self):
        content = self.get_raw_content()
        data = rst2data(content)
        return data

    def get_json_content(self):
        content = self.get_raw_content()
        if content:
            json = rst2json(content)
        else:
            json = 'null'
        return json

    def get_javascript(self):
        try:
            json = self.get_json_content()
            script = _JAVASCRIPT_TEMPLATE % dict(name=self.name, json=json)
        except:
            script = _JAVASCRIPT_ERROR_TEMPLATE % dict(name=self.name)
        return script

    def get_timestamp(self):
        if self.exists():
            return repr(os.stat(self._get_path()).st_mtime)
        else:
            return ''

    def has_changes(self):
        return hasattr(self, 'content')

    def save(self):
        if '/' in self.name or self.name.startswith('.'):
            raise Exception("Invalid page name: %r" % self.name)
        if hasattr(self, 'content'):
            _ensure_pages_dir()
            f = codecs.open(self._get_path(), mode='w', encoding='utf-8')
            f.write(self.content)
            f.close()
            del self.content

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

def get_page_list():
    pages_dir = config['pages_dir']
    page_names = [unicode(filename, 'utf-8') for filename in os.listdir(pages_dir) if not filename.startswith('.')]
    pages = [Page(filename) for filename in page_names]
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
