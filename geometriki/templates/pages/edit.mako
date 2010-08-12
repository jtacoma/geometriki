<%inherit file="/pages/base.mako" />
<%def name="title()">${c.page.title}</%def>
<h1>${c.page.title}</h1>

%if c.page.has_changes():
  <em>preview:</em>
  ${c.page.get_formatted_content() | n}
%endif

${h.form(url('page', id=c.page.name), method='put')}
  ${h.textarea('content', c.page.get_raw_content(), rows=25)}<br/>
  <a style="float:right" href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">ReStructuredText</a>
  ${h.submit('preview', 'Preview')}
  ${h.submit('save', 'Save')}
${h.end_form()}
