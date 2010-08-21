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

import openid.consumer.consumer
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from geometriki.lib.base import BaseController, render
from geometriki.lib.helpers import url

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def login(self):
        # Return a rendered template
        return render('/auth/login.mako')

    def verify(self):
        form_openid = unicode(request.params.get('openid_url'))
        consumer = openid.consumer.consumer.Consumer(session, None)
        try:
            oid_request = consumer.begin(form_openid)
        except openid.consumer.consumer.DiscoveryFailure, exception:
            c.errors.append(exception[0])
            return render('/auth/login.mako')
        if oid_request is None:
            c.errors.append('No openid services found for ' + form_openid)
            return render('/auth/login.mako')
        return_to = request.url.replace('verify', 'process')
        # if oid_request.shouldSendRedirect():
        url = oid_request.redirectURL(return_to, return_to)
        return redirect(url)

    def process(self):
        consumer = openid.consumer.consumer.Consumer(session, None)
        return_to = request.url
        info = consumer.complete(request.params, return_to)
        display_identifier = info.getDisplayIdentifier()
        if info.status == openid.consumer.consumer.FAILURE and display_identifier:
            c.errors.append(display_identifier + ' : ' + info.message)
            return render('/auth/login.mako')
        elif info.status == openid.consumer.consumer.SUCCESS:
            session['user'] = display_identifier
            session['messages'].append('Logged in as ' + display_identifier)
            target = session.get('post_login_redirect', '/')
            if target:
                session['post_login_redirect'] = ''
            session.save()
            redirect(target)
        elif info.status == openid.consumer.consumer.CANCEL:
            c.errors.append('Cancelled.')
            return render('/auth/login.mako')
        elif info.status == openid.consumer.consumer.SETUP_NEEDED:
            c.errors.append('Setup needed: ' + info.setup_url)
            return render('/auth/login.mako')
        else:
            c.errors.append('Verification failed.')
            return render('/auth/login.mako')

    def logout(self):
        if 'user' in session:
            del session['user']
            session['messages'].append('Logged out')
            session.save()
        redirect(url(controller='auth', action='login'))
