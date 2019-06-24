
setl buftype=nofile
setl hidden

" For formatting comments
let b:commentPattern = '\v^[[:alnum:][:space:]]+\[[[:alnum:][:punct:]]+\]'
onoremap <silent> <buffer> ncc :<c-u>execute "normal! V/" b:commentPattern <cr>
