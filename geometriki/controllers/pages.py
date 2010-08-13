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
import json
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from geometriki.lib.base import BaseController, render
from geometriki.model.pages import get_page, get_page_list, PageCreateForm, PageUpdateForm

log = logging.getLogger(__name__)

class PagesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('page', 'pages')
    json_args = dict(ensure_ascii=False, indent=2, sort_keys=True)

    def index(self, format='html'):
        """GET /pages: All items in the collection"""
        # url('pages')
        c.all_pages = get_page_list()
        if format=='json':
            response.content_type = 'application/json'
            return json.dumps([{'name': p.name} for p in c.all_pages], **self.json_args)
        elif format=='yaml':
            response.content_type = 'text/x-yaml'
            return json.dumps([{'name': p.name} for p in c.all_pages], **self.json_args)
        elif format=='txt':
            response.content_type = 'text/plain'
            return '\n'.join([p.name for p in c.all_pages])
        else:
            return render('/pages/index.mako')

    def create(self, *args, **kwargs):
        """POST /pages: Create a new item"""
        # url('pages')
        self._authorize()
        schema = PageCreateForm()
        try:
            form_result = schema.to_python(dict(request.params))
        except formencode.Invalid, error:
            error_message = unicode(error)
            return error_message
        name = form_result.get('name')
        page = get_page(name)
        page.content = form_result.get('content')
        if form_result.get('preview'):
            c.page = page
            return render('/pages/new.mako')
        else:
            page.save()
            redirect(url(controller='pages', action='show', id=name))

    def new(self, format='html', id=''):
        """GET /pages/new: Form to create a new item"""
        # url('new_page')
        self._authorize()
        c.page = get_page(id)
        return render('/pages/new.mako')

    def update(self, id, *args, **kwargs):
        """PUT /pages/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('page', id=ID),
        #           method='put')
        # url('page', id=ID)
        self._authorize()
        schema = PageUpdateForm()
        try:
            form_result = schema.to_python(dict(request.params))
        except formencode.Invalid, error:
            error_message = unicode(error)
            return error_message
        page = get_page(id)
        page.content = form_result.get('content')
        if form_result.get('preview'):
            c.page = page
            return render('/pages/edit.mako')
        else:
            page.save()
            redirect(url(controller='pages', action='show', id=id))

    def delete(self, id):
        """DELETE /pages/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('page', id=ID),
        #           method='delete')
        # url('page', id=ID)
        self._authorize()
        return 'Sorry, this is not implemented yet.'

    def show(self, id, format='html'):
        """GET /pages/id: Show a specific item"""
        # url('page', id=ID)
        page = get_page(id)
        if not page.exists():
            redirect(url(controller='pages', action='new', id=id))
        elif format=='json':
            response.content_type = 'application/json'
            data = page.get_structured_content()
            return json.dumps(data, **self.json_args)
        elif format=='yaml':
            response.content_type = 'text/plain'
            data = page.get_structured_content()
            return json.dumps(data, **self.json_args)
        elif format=='txt':
            response.content_type = 'text/plain'
            return page.get_raw_content()
        else:
            c.page = page
            return render('/pages/show.mako')

    def edit(self, id, format='html'):
        """GET /pages/id/edit: Form to edit an existing item"""
        # url('edit_page', id=ID)
        self._authorize()
        c.page = get_page(id)
        return render('/pages/edit.mako')
