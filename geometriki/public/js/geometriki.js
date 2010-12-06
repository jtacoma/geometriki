geometriki = {};
geometriki.pages = {};
geometriki.words = {};
geometriki.indices = {};

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
  var spell = $(".play-input").val();
  if (spell) {
    var thead = "<thead><tr><th>&nbsp;</th>";
    for (var name in geometriki.page.data.meta)
      thead += "<th>" + name + "</th>";
    thead += "</tr></thead>";
    var totals = {}
    var subtotals = {}
    var tbody = "";
    for (var i=0; i<spell.length; ++i) {
      var symbol = spell[i];
      var row = "<td>" + symbol + "</td>";
      if (symbol in geometriki.index) {
        var meaning = geometriki.index[symbol];
        for (var name in geometriki.page.data.meta)
        {
          var attribute = name in meaning ? meaning[name] : null;
          row += "<td>" + attribute + "</td>";
          if (typeof(attribute) == "number")
          {
            totals[name] = (name in totals ? totals[name] : 0) + attribute;
            subtotals[name] = (name in subtotals ? subtotals[name] : 0) + attribute;
          }
        }
      }
      tbody += "<tr>" + row + "</tr>";
      if (!isEmpty(subtotals) && ((!(symbol in geometriki.index) && symbol.trim().length==0) || (+i+1) >= spell.length)) {
        var subrow = "<td>&nbsp;</td>";
        for (name in geometriki.page.data.meta)
          if (name in subtotals)
            subrow += "<td>" + subtotals[name] + "</td>";
          else
            subrow += "<td>&nbsp;</td>";
        tbody += "<tr class=\"subtotals\">" + subrow + "</tr>";
        subtotals = {};
      }
    }
    if (totals && tbody) {
      var totalrow = "<td>&nbsp;</td>";
      for (var name in geometriki.page.data.meta)
        if (name in totals)
          totalrow += "<td>" + totals[name] + "</td>";
        else
          totalrow += "<td>&nbsp;</td>";
      tbody += "<tr class=\"totals\">" + totalrow + "</tr>";
    }
    var extra = "";
    if (!tbody) {
      extra = "<span class=\"error\">Oops, there seems to be a bug in this page's javascript.</span>";
    }
    tbody = "<tbody valign=\"top\">" + tbody + "</tbody>";
    var table = "<table>" + thead + tbody + "</table>";
    $("#play-output").html(table + extra);
  } else {
    $("#play-output").html("<span>(enter some text)</span>");
  }
};

geometriki.get_index = function(all_records, key_names) {
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
  return index;
};

geometriki.update_indices_from_pages = function() {
  $.each(geometriki.pages, function(page_name, page) {
    var data = geometriki.page.data;
    if (!("meta" in data && "records" in data)) return;
    var keys = [];
    for (property in data.meta) {
      keys.push(property);
      break;
    }
    geometriki.indices[page_name] = geometriki.get_index(data.records, keys);
  });
}

geometriki.update_index_from_page = function() {
  var data = geometriki.page.data;
  if (!("meta" in data && "records" in data)) return;
  var keys = [];
  for (property in data.meta) {
    keys.push(property);
    break;
  }
  geometriki.index = geometriki.get_index(data.records, keys);
};

geometriki.get_map = function(name) {
  var dot = name.indexOf(".");
  var page_name = name.substring(0, dot);
  var column_name = name.substring(dot+1);
  var page = geometriki.pages[page_name];
  var values = {};
  $.each(page.data.records, function(index, record) {
    values.push(record[column_name]);
  });
  return {name:name, values:values};
};

geometriki.build_dictionary = function(_, table_names) {
  geometriki.update_indices_from_pages();
  var dictionary = {};
  $.each(table_names, function(table_name_index, table_name) {
    var dot = table_name.indexOf(".");
    var page_name = table_name.substring(0, dot);
    var attribute_name = table_name.substring(dot+1);
    var index = geometriki.indices[page_name];
    $.each(geometriki.words, function(source_name, source) {
      var spell_list = source.data;
      $.each(spell_list, function(spell_index, spell) {
        var sum = 0;
        var relevant = false;
        $.each(spell, function(symbol_index, symbol) {
          if (symbol in index) {
            var meaning = index[symbol];
            var value = parseInt(meaning[attribute_name]);
            sum += value;
            relevant = true;
          }
        });
        if (relevant) {
          if (!(sum in dictionary)) dictionary[sum] = {};
          if (!(table_name in dictionary[sum])) dictionary[sum][table_name] = [];
          dictionary[sum][table_name].push(spell);
        }
      });
    });
  });
  geometriki.dictionary = dictionary;
  geometriki.message("Dictionary built.");
  var keys = [];
  $.each(dictionary, function(key, value) {
    keys.push(key);
  });
  var sortNumber = function (a, b) { return a - b; };
  keys.sort(sortNumber);
  var html = "<dl>";
  $.each(keys, function(index, key) {
    value = dictionary[key];
    html += "<dt class='key'>" + key + "</dt>";
    $.each(value, function(table_name, matching_words) {
      $.each(matching_words, function(index, word) {
        html += "<dd>" + word + "</dd>";
      });
    });
  });
  html += "</dl>";
  $("#dictionary").html(html);
  geometriki.message("Dictionary formatted.");
};
