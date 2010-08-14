<%inherit file="/base.mako" />
<%def name="title()">Authenticate</%def>
${h.form(url(controller='auth', action='verify'), method='post')}
  <label for="openid_url">
    OpenID:
    <br/>
    ${h.text('openid_url', class_='openid_url')}
  </label>
  ${h.submit('login', 'Login')}
  <br/>
  <a href="http://openid.net/get-an-openid">What is this?</a>
  <a href="http://evan.prodromou.name/OpenID_Privacy_Concerns">What about privacy?</a>
${h.end_form()}
