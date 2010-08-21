geometriki = {};
geometriki.pages = {};

function isEmpty(item) { for(var i in item) { return false; } return true; }

geometriki.message = function(content) {
  $("#messages").append("<li>" + content + "</li>");
};

geometriki.error = function(content) {
  $("#messages").append("<li class=\"error\">" + content + "</li>");
};

geometriki.play_begin = function(initial_text) {
  geometriki.update_index_from_page();
  if (!("index" in geometriki) || isEmpty(geometriki.index))
    geometriki.error("Failed to build index for <strong>" + geometriki.page.name + "</strong>: maybe it has no well-formed table.");
  else
  {
    $("#play").append("<input class=\"play-input\" value=\"" + initial_text + "\" /><div id=\"play-output\" />");
    $("input.play-input").focus();
    $(".play-input").keyup(geometriki.play_respond);
    $(".play-input").mouseup(geometriki.play_respond);
    geometriki.play_respond();
  }
};

geometriki.play_respond = function() {
  $("#play-output").empty();
  var spell = $(".play-input").val();
  if (spell) {
    $("#play-output").append("<table><thead><th>&nbsp;</th></thead><tbody valign=\"top\"/></table>");
    for (name in geometriki.page.data.meta)
      $("#play-output thead").append("<th>" + name + "</th>");
    totals = {}
    subtotals = {}
    for (i in spell) {
      symbol = spell[i];
      row = "<td>" + symbol + "</td>";
      if (symbol in geometriki.index) {
        meaning = geometriki.index[symbol];
        for (name in geometriki.page.data.meta)
        {
          attribute = name in meaning ? meaning[name] : null;
          row += "<td>" + attribute + "</td>";
          if (typeof(attribute) == "number")
          {
            totals[name] = (name in totals ? totals[name] : 0) + attribute;
            subtotals[name] = (name in subtotals ? subtotals[name] : 0) + attribute;
          }
        }
      }
      $("#play-output tbody").append("<tr>" + row + "</tr>");
      if (!isEmpty(subtotals) && (!(symbol in geometriki.index) || (i*1+1) >= spell.length)) {
        row = "<td>&nbsp;</td>";
        for (name in geometriki.page.data.meta)
          if (name in subtotals)
            row += "<td>" + subtotals[name] + "</td>";
          else
            row += "<td>&nbsp;</td>";
        $("#play-output tbody").append("<tr class=\"subtotals\">" + row + "</tr>");
        subtotals = {};
      }
    }
    if (totals) {
      row = "<td>&nbsp;</td>";
      for (name in geometriki.page.data.meta)
        if (name in totals)
          row += "<td>" + totals[name] + "</td>";
        else
          row += "<td>&nbsp;</td>";
      $("#play-output tbody").append("<tr class=\"totals\">" + row + "</tr>");
    }
  } else {
    $("#play-output").append("<span>(enter some spell)</span>");
  }
};

geometriki.update_index = function(all_records, key_names) {
  var index = {};
  for (record_index in all_records)
  {
    var record = all_records[record_index];
    for (key_index in key_names)
    {
      key = key_names[key_index];
      if (key in record)
      {
        value = record[key];
        if (typeof(value) == "object")
          for (value_index in value)
            index[value[value_index]] = record;
        else
          index[value] = record;
      }
    }
  }
  geometriki.index = index;
};

geometriki.update_index_from_page = function() {
  if (!("page" in geometriki && typeof(geometriki.page) != "undefined" && "data" in geometriki.page))
  {
      geometriki.error("Page scripts were not loaded or failed to initialize.");
      return;
  }
  var data = geometriki.page.data;
  if (!("meta" in data && "records" in data)) return;
  var keys = [];
  for (property in data.meta) {
    keys.push(property);
    break;
  }
  geometriki.update_index(data.records, keys);
};
