# 「autoindent=true」と指定したtextareaで、
# リターンキー押下前にカーソルのあった行のインデントと同じインデントを新しい行の頭に追加する。
$(document).ready ->
  $("body").on("keydown", "textarea[autoindent=true]", (e) ->
    if e.keyCode == 13
      e.preventDefault()
      elem = e.target
      val = elem.value
      pos = elem.selectionStart
      before_pos = val.substr(0, pos)
      indent = before_pos.substring(before_pos.lastIndexOf("\n") + 1).match(/^[\t| ]*/)[0]
      elem.value = val.substr(0, pos) + "\n" + indent + val.substr(pos, val.length)
      elem.setSelectionRange(pos + indent.length + 1, pos + indent.length + 1)
  )
  return
