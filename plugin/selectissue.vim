function! JiraVimBoardIssueSelect(funcname)
    let s:line = getline(line("."))
    let s:issueMatch = substitute(matchstr(s:line, '\v\u+-\d+\s'), '\s$', '', '')
    if s:issueMatch != ""
        let Func = function(a:funcname, [s:issueMatch])
        call Func()
    endif
endfunction

