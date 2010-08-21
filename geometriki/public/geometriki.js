geometriki = {};
geometriki.pages = {};

function isEmpty(item) { for(var i in item) { return false; } return true; }

geometriki.message = function(content) {
  $("#messages").append("<li>" + content + "</li>");
};

geometriki.error = function(content) {
  $("#messages").append("<li class=\"error\">" + content + "</li>");
};

geometriki.play_begin = function() {
  geometriki.update_index_from_page();
  if (!("index" in geometriki) || isEmpty(geometriki.index))
    geometriki.error("Failed to build index for <strong>" + geometriki.page.name + "</strong>: maybe it has no well-formed table.");
  else
  {
    $("#play").append("<input class=\"play-input\" /><div id=\"play-output\" />");
    $(".play-input").keyup(geometriki.play_respond);
    $(".play-input").mouseup(geometriki.play_respond);
    geometriki.play_respond();
  }
};

geometriki.play_respond = function() {
  $("#play-output").empty();
  var text = $(".play-input").val();
  if (text) {
    $("#play-output").append("<table><thead><th></th></thead><tbody valign=\"top\"/></table>");
    for (name in geometriki.page.data.meta)
      $("#play-output thead").append("<th>" + name + "</th>");
    for (i in text) {
      item = text[i];
      row = "<td>" + item + "</td>";
      if (item in geometriki.index) {
        record = geometriki.index[item];
        for (name in geometriki.page.data.meta)
          row += "<td>" + (name in record ? record[name] : "") + "</td>";
      }
      $("#play-output tbody").append("<tr>" + row + "</tr>");
    }
  } else {
    $("#play-output").append("<span>(enter some text)</span>");
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
