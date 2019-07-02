
function! <SID>JiraVimLoadMore()
    call check#CheckStorageSession()

    let l:moreline = line(".")

    silent execute 'normal! ?\v^-+$' . "\<cr>"
    normal! k
    let l:categoryName = matchstr(getline("."), '\v^(\u+\s?)+')
    let l:first_issue_line = line(".") + 2

    " Move the cursor back to the more line
    execute ":" . l:moreline
    
    execute "python3 sys.argv = [\"" . l:categoryName . "\", " . l:moreline . "]"
    if &filetype ==# "jirasprintview"
        execute "python3 python.sprints.more.JiraVimLoadMore(sessionStorage)"
    elseif &filetype ==# "jiraboardview" || &filetype ==# "jirakanbanboardview"
        execute "python3 python.boards.more.JiraVimLoadMore(sessionStorage)"
    elseif &filetype ==# "jirasearchview"
        execute "python3 python.search.more.JiraVimLoadMore(sessionStorage)"
    else
        throw "Not a valid target for loading more issues"
    endif
endfunction

command JiraVimLoadMore call <SID>JiraVimLoadMore()
