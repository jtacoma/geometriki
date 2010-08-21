<%inherit file="/base.mako" />
<%def name="title()">Error ${c.code}: ${c.message}</%def>
<%def name="doctype()">error</%def>
<h1>Error ${c.code}</h1>
<p>${c.message}</p>
