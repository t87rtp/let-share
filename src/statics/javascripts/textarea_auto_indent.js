(function() {
  $(document).ready(function() {
    $("body").on("keydown", "textarea[autoindent=true]", function(e) {
      var before_pos, elem, indent, pos, val;
      if (e.keyCode === 13) {
        e.preventDefault();
        elem = e.target;
        val = elem.value;
        pos = elem.selectionStart;
        before_pos = val.substr(0, pos);
        indent = before_pos.substring(before_pos.lastIndexOf("\n") + 1).match(/^[\t| ]*/)[0];
        elem.value = val.substr(0, pos) + "\n" + indent + val.substr(pos, val.length);
        return elem.setSelectionRange(pos + indent.length + 1, pos + indent.length + 1);
      }
    });
  });

}).call(this);
