
function! JiraVimBoardReturn(funcname)
    if exists("b:jiraVimBoardName") && b:jiraVimBoardName !=? ""
        let l:Func = function(a:funcname, [b:jiraVimBoardName])
        call l:Func()
    else
        throw "Could not find board name in the first row. Please sure the file is properly formatted" 
    endif
endfunction
