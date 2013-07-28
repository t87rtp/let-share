(function() {
  $(document).ready(function() {
    var $num_box_base, $target, $wrap, end_line, lines, pre_lines, refresh, scroll, select_lines, start_line;
    $target = $("textarea[linenumber=true]");
    lines = function() {
      return $target.val().split(/\n/).length;
    };
    $wrap = $("<ul>").appendTo("#line_number_wrap");
    scroll = function() {
      return $wrap.css({
        position: "absolute",
        top: -$target.scrollTop() + "px",
        left: "0px",
        width: "100%"
      });
    };
    scroll();
    $num_box_base = $("<li>").addClass("num_box").css({
      height: $target.css("line-height"),
      "line-height": $target.css("line-height"),
      "font-size": $target.css("font-size")
    });
    refresh = function() {
      var i, num_box, _results;
      $wrap.empty();
      i = 1;
      _results = [];
      while (lines() + 1 > i) {
        num_box = $num_box_base.clone().html(i).appendTo($wrap);
        _results.push(++i);
      }
      return _results;
    };
    refresh();
    pre_lines = lines();
    $target.on("keyup", function(e) {
      if (pre_lines !== lines()) {
        refresh();
      }
      return pre_lines = lines();
    });
    $target.on("scroll", function(e) {
      return scroll();
    });
    select_lines = function(s_line, e_line) {
      var a_str, b_str, each_lines, i, value;
      value = $target.val();
      each_lines = value.match(/.*\n/g);
      each_lines.push(value.substr(value.lastIndexOf("\n") + 1));
      b_str = "";
      a_str = "";
      i = 0;
      while (i < s_line) {
        b_str += each_lines[i];
        ++i;
      }
      i = 0;
      while (i <= e_line) {
        a_str += each_lines[i];
        ++i;
      }
      $target[0].focus();
      return $target[0].setSelectionRange(b_str.length, a_str.length);
    };
    start_line = null;
    end_line = null;
    $wrap.on("mousedown", ".num_box", function(e) {
      e.preventDefault();
      start_line = $wrap.children(".num_box").index(this);
      return select_lines(start_line, start_line);
    });
    $wrap.on("mousemove", ".num_box", function(e) {
      e.preventDefault();
      if (start_line === null && end_line === null) {
        return;
      }
      end_line = $wrap.children(".num_box").index(this);
      if (start_line <= end_line) {
        return select_lines(start_line, end_line);
      } else {
        return select_lines(end_line, start_line);
      }
    });
    $("body").on("mouseup", function(e) {
      start_line = null;
      return end_line = null;
    });
  });

}).call(this);
