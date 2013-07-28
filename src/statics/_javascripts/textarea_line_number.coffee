# 「linenumber=true」と指定したtextareaで、
# 行番号を表示し、行番号をクリックorドラッグすると行選択できるように。
$(document).ready ->
  $target = $("textarea[linenumber=true]")
  lines = ->
    $target.val().split(/\n/).length
  
  $wrap = $("<ul>")
    .appendTo("#line_number_wrap")
  scroll = ->
    $wrap.css(
      position: "absolute"
      top: -$target.scrollTop() + "px"
      left: "0px"
      width: "100%"
    )
  scroll()

  
  $num_box_base = $("<li>")
    .addClass("num_box")
    .css(
      height: $target.css("line-height")
      "line-height": $target.css("line-height")
      "font-size": $target.css("font-size")
    )
  
  refresh = ->
    $wrap.empty()
    i = 1
    while lines() + 1 > i
      num_box = $num_box_base.clone()
        .html(i)
        .appendTo($wrap)
      ++i
  refresh()
  
  pre_lines = lines()
  $target.on("keyup", (e) ->
    if pre_lines != lines()
      refresh()
    pre_lines = lines()
  )
  $target.on("scroll", (e) ->
    scroll()
  )
  
  select_lines = (s_line, e_line) ->
    value = $target.val()
    each_lines = value.match(/.*\n/g)
    each_lines.push(value.substr(value.lastIndexOf("\n")+1))
    b_str = ""
    a_str = ""
    i = 0
    while i < s_line
      b_str += each_lines[i]
      ++i
    i = 0
    while i <= e_line
      a_str += each_lines[i]
      ++i
    $target[0].focus()
    $target[0].setSelectionRange(b_str.length, a_str.length)
  
  start_line = null
  end_line = null
  $wrap.on("mousedown", ".num_box", (e) ->
    e.preventDefault()
    start_line = $wrap.children(".num_box").index(this)
    select_lines(start_line, start_line)
  )
  $wrap.on("mousemove", ".num_box", (e) ->
    e.preventDefault()
    if start_line == null and end_line == null
      return
    end_line = $wrap.children(".num_box").index(this)
    if start_line <= end_line
      select_lines(start_line, end_line)
    else
      select_lines(end_line, start_line)
  )
  $("body").on("mouseup", (e) ->
    start_line = null
    end_line = null
  )
  return
