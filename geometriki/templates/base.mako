<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <title>${self.title()}</title>
    <script type="text/javascript" src="/jquery-1.4.2.min.js"></script>
    <script type="text/javascript" src="/geometriki.js"></script>
    <link rel="stylesheet" type="text/css" href="/reset-fonts-grids.css" />
    <link rel="stylesheet" type="text/css" href="/stylesheet.css" />
    <link rel="stylesheet" type="text/css" media="print" href="/print.css" />
    ${self.head_tags()}
  </head>
  <body>
    <div id="doc" class="${self.doctype()}">
      <div id="hd">${self.head()}</div> 
      <div id="bd">${self.body()}</div> 
      <div id="ft">${self.foot()}</div> 
    </div>
  </body>
</html>
<%def name="head_tags()"></%def>
<%def name="head()">
  <ul id="navigation-menu" class="menu">
		<li class="head">navigation:</li>
    ${self.navigation()}
  </ul>
  <ul id="actions-menu" class="menu">
		<li class="head">actions:</li>
    ${self.actions()}
  </ul>
  % if c.errors or c.messages or True:
  <ul id="messages">
    ${self.messages()}
    % for msg in c.messages:
    <li class="message">${msg}</li>
    % endfor
    % for err in c.errors:
    <li class="error">${err}</li>
    % endfor
  </ul>
  % endif
</%def>
<%def name="foot()">
	<a href="mailto:joshua@yellowseed.org">contact</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
	<a href="http://gitorious.org/geometriki">geometriki source code</a>
</%def>
<%def name="navigation()">
	<li><a href="${h.url('pages')}">pages</a></li>
</%def>
<%def name="actions()">
  % if c.user:
	<li><a href="${h.url(controller='auth', action='logout')}" title="${c.user}">logout</a></li>
  % else:
	<li><a href="${h.url(controller='auth', action='login')}">login</a></li>
  % endif
</%def>
<%def name="doctype()"></%def>
<%def name="messages()"></%def>
