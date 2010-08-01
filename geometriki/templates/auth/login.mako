<%inherit file="/base.mako" />
<%def name="title()">Authenticate</%def>
${h.form(url(controller='auth', action='verify'), method='post')}
  <label for="openid_url">
    OpenID:
    <a href="http://openid.net/get-an-openid">What is this?</a>
    <br/>
    ${h.text('openid_url', class_='openid_url')}
  </label>
  ${h.submit('login', 'Login')}
${h.end_form()}
