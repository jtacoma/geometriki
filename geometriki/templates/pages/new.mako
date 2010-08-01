<%inherit file="/pages/base.mako" />
<%def name="title()">(new page)</%def>
${h.form(url('pages'), method='post')}
  ${h.text('name')}
  ${h.textarea('content', rows=25)}<br/>
  <a style="float:right" href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">ReStructuredText</a>
  ${h.submit('create', 'Create')}
${h.end_form()}
