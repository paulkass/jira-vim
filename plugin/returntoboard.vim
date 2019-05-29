
function! JiraVimBoardReturn(funcname)
    call check#CheckStorageSession()
    if exists("b:jiraVimBoardName") && b:jiraVimBoardName !=? ""
        let l:Func = function(a:funcname, [b:jiraVimBoardName])
        call l:Func()
    else
        throw "Could not identify the board name. Please specify the b:jiravimBoardName for proper board return."
    endif
endfunction
