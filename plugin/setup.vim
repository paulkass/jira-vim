
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"

" Import all scripts with functions here
python3 import python.boards.open
python3 import python.boards.more
python3 import python.issues.open
python3 import python.sprints.open
python3 import python.sprints.more

" Set some global constants
let g:jiraBoardFiletypePattern = '\vjira\a*boardview'

" Some Plug-in specific Helper functions
function! JiraVimTrimHelper(string)
    let l:arg = substitute(a:string, '\v^\s+', "", "")
    let l:arg = substitute(l:arg, '\v\s+$', "", "")
    return l:arg
endfunction
