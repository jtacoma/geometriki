<%inherit file="/pages/base.mako" />
<%def name="title()">(new page)</%def>

%if c.page and c.page.has_changes():
  <em>preview:</em>
  ${c.page.get_formatted_content() | n}
%endif

${h.form(url('new_page'), method='post')}
  ${h.text('name', c.page.name)}
  ${h.textarea('content', c.page.get_raw_content(), rows=25)}<br/>
  <a style="float:right" href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">ReStructuredText</a>
  ${h.submit('preview', 'Preview')}
  ${h.submit('create', 'Create')}
${h.end_form()}
