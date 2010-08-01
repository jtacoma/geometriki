<%inherit file="/pages/base.mako" />
<%def name="title()">${c.page.title}</%def>
<h1>${c.page.title}</h1>
${h.form(url('page', id=c.page.name), method='put')}
  ${h.textarea('content', c.page.get_raw_content(), rows=25)}<br/>
  <a style="float:right" href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">ReStructuredText</a>
  ${h.submit('save', 'Save')}
${h.end_form()}
