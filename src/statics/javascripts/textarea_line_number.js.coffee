# 「autoindent=true」と指定したtextareaで、
# リターンキー押下前にカーソルのあった行のインデントと同じインデントを新しい行の頭に追加する。
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
  
  i = 1
  while lines() + 1 > i
    num_box = $num_box_base.clone()
      .html(i)
      .appendTo($wrap)
    ++i

  
  $target.on("keydown", (e) ->
    console.log e.keyCode
  )
  $target.on("scroll", (e) ->
    scroll()
  )
  return
