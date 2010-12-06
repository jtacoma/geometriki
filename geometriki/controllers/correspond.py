"""Controller for correspondence explorations.
"""

import logging

from formencode.variabledecode import variable_decode
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import json

from geometriki.lib.base import BaseController, render
from geometriki.model.correspond import CorrespondForm
from geometriki.model.pages import get_page, get_page_list, PageCreateForm, PageUpdateForm

log = logging.getLogger(__name__)

class CorrespondController(BaseController):
    """This controller exposes table correspondence functions.
    """

    def _keys_for_select(self):
        keys_for_select = []
        for page in get_page_list():
            data = page.get_data()
            meta = data.get('meta', {})
            keys = meta.keys()
            for key in keys:
                name = u'%s.%s' % (page.name, key)
                title = u'%s %s' % (page.title, key)
                keys_for_select.append([name, title])
        return keys_for_select

    def _pages_for_select(self):
        pages_for_select = []
        for page in get_page_list():
            pages_for_select.append([page.name, page.title])
        return pages_for_select

    def index(self):
        """Here we simply display a basic page to begin the correspondence process.
        """
        c.pages_for_select = self._pages_for_select()
        c.pages = []
        c.keys_for_select = self._keys_for_select()
        c.input_keys = []
        c.output_keys = []
        return render('/correspond/index.mako')

    def dictionary(self, input_keys=None, output_keys=None):
        """Calculate dictionary for selected keys and input text.
        """
        schema = CorrespondForm()
        try:
            form_result = schema.to_python(variable_decode(request.params))
        except formencode.Invalid, error:
            error_message = unicode(error)
            return error_message
        c.pages_for_select = self._pages_for_select()
        c.pages = form_result.get('pages')
        c.keys_for_select = self._keys_for_select()
        c.input_keys = form_result.get('input_keys')
        c.input_keys_json = json.dumps(c.input_keys, ensure_ascii=False)
        c.output_keys = form_result.get('output_keys')
        c.output_keys_json = json.dumps(c.output_keys, ensure_ascii=False)
        c.key_pages = list(set([key.split('.')[0] for key in c.input_keys +
                                c.output_keys]))
        return render('/correspond/dictionary.mako')
