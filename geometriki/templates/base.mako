<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" href="/reset-fonts-grids.css" />
    <link rel="stylesheet" type="text/css" href="/stylesheet.css" />
    <link rel="stylesheet" type="text/css" media="print" href="/print.css" />
    ${self.head_tags()}
  </head>
  <body>
    <div id="doc">
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
  % if c.errors or c.messages:
  <ul id="messages">
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
	[powered by <a href="http://pypi.python.org/pypi/geometriki">geometriki</a>]
</%def>
<%def name="navigation()">
	<li><a href="${h.url('pages')}">pages</a></li>
</%def>
<%def name="actions()">
	<li><a href="mailto:joshua@yellowseed.org">feedback</a></li>
  % if c.user:
	<li><a href="${h.url(controller='auth', action='logout')}" title="${c.user}">logout</a></li>
  % else:
	<li><a href="${h.url(controller='auth', action='login')}">login</a></li>
  % endif
</%def>
