/* Ok, there's nothing much here yet.  There probably will be though, some day...  */
geometriki = {
  version: "0.1.8",
  message: function(content) {
    $("#messages").append("<li>" + content + "</li>");
  },
  error: function(content) {
    $("#messages").append("<li class=\"error\">" + content + "</li>");
  },
};
