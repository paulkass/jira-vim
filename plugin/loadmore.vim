
function! JiraVimLoadMore()
    call check#CheckStorageSession()

    let l:moreline = line(".")

    silent execute 'normal! ?\v^-+' . "\<cr>"
    normal! k
    let l:categoryName = matchstr(getline("."), '\v^\u+')
    let l:first_issue_line = line(".") + 2

    " Move the cursor back to the more line
    execute ":" . l:moreline
    
    set modifiable
    execute "python3 sys.argv = [\"" . l:categoryName . "\", " . l:moreline . "]"
    execute "python3 python.boards.more.JiraVimLoadMore(sessionStorage)"
    set nomodifiable
endfunction
