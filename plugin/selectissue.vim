function! <SID>JiraVimBoardIssueSelect(funcname)
    let l:funcname = JiraVimTrimHelper(a:funcname)
    call check#CheckStorageSession()
    if -1 !=# matchstr(&filetype, g:jiraBoardFiletypePattern)  
        let l:bufferNumber = bufnr("%") 
        let l:line = getline(line("."))
        let l:issueMatch = JiraVimTrimHelper(matchstr(l:line, '\v\u+-\d+\s'))
        if l:issueMatch != ""
            execute l:funcname " " l:issueMatch
            let b:boardBufferNumber = l:bufferNumber 
        endif
    else
        throw "The current buffer is not a board, are you sure you should be calling this command?"
    endif
endfunction

command -nargs=1 -complete=command JiraVimBoardIssueSelect call <SID>JiraVimBoardIssueSelect(<q-args>)
