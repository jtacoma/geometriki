<%inherit file="/pages/base.mako" />
<%def name="title()">${c.page.title}</%def>
<%def name="head_tags()">
  <script type="text/javascript" src="${url('page', id=c.page.name)}.js"></script>
  <script type="text/javascript">
    $(function() {
      geometriki.play_begin("${c.text}");
    });
  </script>
  ${parent.head_tags()}
</%def>
<%def name="actions()">
<li><a href="${url('page', id=c.page.name)}">view</a></li>
<li><a href="${url('edit_page', id=c.page.name)}">edit</a></li>
${parent.actions()}
</%def>
<%def name="messages()">
<noscript><li class="error">Javascript is required to use this page.</li></noscript>
</%def>
<div id="play">
</div>
