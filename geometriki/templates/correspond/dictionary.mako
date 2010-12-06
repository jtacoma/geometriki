<%inherit file="/pages/base.mako" />
<%def name="title()">Correspond</%def>

<%def name="head_tags()">
  % for page_name in c.pages:
    <script type="text/javascript" src="${page_name}.js"></script>
  % endfor
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
