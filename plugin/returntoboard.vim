
function! JiraVimBoardReturn(funcname)
    let s:boardName = substitute(matchstr(getline("1"), '\v^\s?\u+-'), '\v[\s-]+', '', 'g')
    if s:boardName != ""
        let s:Func = function(a:funcname, [s:boardName])
        call s:Func()
    else
        throw "Could not find board name in the first row. Please sure the file is properly formatted" 
    endif
endfunction
