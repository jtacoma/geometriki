<%inherit file="/pages/base.mako" />
<%def name="title()">${c.page.title}</%def>
<%def name="actions()">
<li><a href="${url('edit_page', id=c.page.name)}">edit</a></li>
${parent.actions()}
</%def>
%if c.page.exists():
  ${c.page.get_formatted_content() | n}
%else:
  There is nothing here.
  <a href="${url('edit_page', id=c.page.name)}">Write something.</a>
%endif
  
