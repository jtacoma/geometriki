<%inherit file="/pages/base.mako" />
<%def name="title()">Pages</%def>
% for page in c.all_pages:
    <div><a href="${url('page', id=page.name)}">${page.title}</a></div>
% endfor
