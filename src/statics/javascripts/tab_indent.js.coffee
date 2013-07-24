$(document).ready ->
  $("body").on("keydown", "textarea[tabindent=true]", (e) ->
    if e.keyCode == 9
      e.preventDefault()
      elem = e.target
      val = elem.value
      pos = elem.selectionStart
      elem.value = val.substr(0, pos) + '\t' + val.substr(pos, val.length)
      elem.setSelectionRange(pos + 1, pos + 1)
  )
  return
