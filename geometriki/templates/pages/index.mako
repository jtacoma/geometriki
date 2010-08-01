<%inherit file="/pages/base.mako" />
<%def name="title()">Pages</%def>
<%def name="actions()">
<a href="${url('new_page')}">create page</a>
${parent.actions()}
</%def>
% for page in c.all_pages:
    <div><a href="${url('page', id=page.name)}">${page.title}</a></div>
% endfor
