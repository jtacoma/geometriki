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

    def index(self, format='html'):
        """GET /pages: All items in the collection"""
        # url('pages')
        c.all_pages = get_page_list()
        return render('/pages/index.mako')

    def create(self):
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
        preview = form_result.get('preview')
        if page.get_timestamp() and form_result.get('timestamp') != page.get_timestamp():
            c.errors.append('This page was modified while you were editing it: your changes cannot be saved.')
            preview = True
        if preview:
            c.page = page
            c.timestamp = form_result.get('timestamp')
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
        # for html format, show page even if it does not exist:
        if format=='html':
            c.page = page
            return render('/pages/show.mako')
        # otherwise, if page does not exist, it is a 404:
        if not page.exists() and not session.get('user', ''): abort(404)
        if format=='js':
            response.content_type = 'text/javascript'
            script = page.get_javascript()
            return script
        elif format=='json':
            response.content_type = 'application/json'
            json = page.get_json_content()
            return json
        elif format=='play':
            c.page = page
            c.text = request.GET.get('text', '')
            return render('/pages/play.mako')
        elif format=='txt':
            response.content_type = 'text/plain'
            return page.get_raw_content()
        elif format=='words-js':
            response.content_type = 'text/javascript'
            json = page.get_words_js()
            return json
        elif format=='yaml':
            response.content_type = 'text/plain'
            json = page.get_json_content()
            return json

    def edit(self, id, format='html'):
        """GET /pages/id/edit: Form to edit an existing item"""
        # url('edit_page', id=ID)
        self._authorize()
        c.page = get_page(id)
        c.timestamp = c.page.get_timestamp()
        return render('/pages/edit.mako')
