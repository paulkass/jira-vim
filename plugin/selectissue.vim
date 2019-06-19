function! JiraVimBoardIssueSelect(funcname)
    call check#CheckStorageSession()
    if -1 !=# matchstr(&filetype, g:jiraBoardFiletypePattern)  
        let l:bufferNumber = bufnr("%") 
        let l:line = getline(line("."))
        let l:issueMatch = substitute(matchstr(l:line, '\v\u+-\d+\s'), '\v\s+$', '', 'g')
        if l:issueMatch != ""
            let l:Func = function(a:funcname, [l:issueMatch])
            call l:Func()
            let b:boardBufferNumber = l:bufferNumber 
        endif
    else
        throw "The current buffer is not a board, are you sure you should be calling this command?"
    endif
endfunction

