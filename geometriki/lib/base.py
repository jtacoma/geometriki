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
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect
from pylons.templating import render_mako as render

class BaseController(WSGIController):

    def __before__(self, action, **params):
        c.user = session.get('user')
        c.messages = session.get('messages', [])
        c.errors = session.get('errors', [])
        session['messages'] = []
        session['errors'] = []
        session.save()

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)

    def _authorize(self):
        user = session.get('user')
        if not user:
            redirect(url(controller='auth', action='login'))
