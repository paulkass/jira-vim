
function! <SID>JiraVimSprintOpen(name)
    let l:name = JiraVimTrimHelper(a:name)
    echo "Loading sprint " . l:name
    call check#CheckStorageSession()

    execute "python3 sys.argv = [\"" . l:name . "\"]"
    execute "python3 python.sprints.open.JiraVimSprintOpen(sessionStorage, False)" 
endfunction

command! -nargs=1 JiraVimSprintOpen call <SID>JiraVimSprintOpen(<q-args>)
