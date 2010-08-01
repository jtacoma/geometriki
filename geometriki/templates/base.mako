<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" href="/reset-fonts-grids.css" />
    <link rel="stylesheet" type="text/css" href="/stylesheet.css" />
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
      <div id="navigation-menu">
        navigation:
        ${self.navigation()}
      </div>
      <div id="actions-menu">
        actions:
        ${self.actions()}
      </div>
</%def>
<%def name="foot()"></%def>
<%def name="navigation()">
      <a href="${h.url_for('pages')}">pages</a>
</%def>
<%def name="actions()">
  <a href="mailto:joshua@yellowseed.org">feedback</a>
  % if c.user:
    <a href="${h.url_for(controller='auth', action='logout')}">logout ${c.user}</a>
  % else:
    <a href="${h.url_for(controller='auth', action='login')}">login</a>
  % endif
</%def>
