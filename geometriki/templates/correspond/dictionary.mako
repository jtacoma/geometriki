<%inherit file="/pages/base.mako" />
<%def name="title()">Correspond</%def>

<%def name="head_tags()">
  % for page_name in c.pages:
    <script type="text/javascript" src="${url(controller='pages',id=page_name,action='show')}.words-js"></script>
  % endfor
  % for page_name in c.key_pages:
    <script type="text/javascript" src="${url(controller='pages',id=page_name,action='show')}.js"></script>
  % endfor
  <script type="text/javascript">
    $(function() {
      geometriki.build_dictionary(${c.input_keys_json | n}, ${c.output_keys_json | n});
    });
  </script>
  ${parent.head_tags()}
</%def>

<%def name="messages()">
<noscript><li class="error">Javascript is required to use this page.</li></noscript>
</%def>

${h.form(url(controller="correspond", action="dictionary"), method="get")}
  <label for="pages">Input Texts:</label>
  ${h.select("pages", c.pages, c.pages_for_select, multiple=True)}
  <label for="input_keys">Input Keys:</label>
  ${h.select("input_keys", c.input_keys, c.keys_for_select, multiple=True)}
  <label for="output_keys">Output Keys:</label>
  ${h.select("output_keys", c.output_keys, c.keys_for_select, multiple=True)}
  ${h.submit("submit", "Submit")}
${h.end_form()}

<div id="dictionary">
</div>
