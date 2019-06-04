function! JiraVimBoardIssueSelect(funcname)
    call check#CheckStorageSession()
    let l:line = getline(line("."))
    let l:issueMatch = substitute(matchstr(l:line, '\v\u+-\d+\s'), '\v\s+$', '', 'g')
    if l:issueMatch != ""
        let l:Func = function(a:funcname, [l:issueMatch])
        call l:Func()
    endif
endfunction

