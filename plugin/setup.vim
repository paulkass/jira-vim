
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"

" Make sure that all the necessary parts are in place {{{
if !has('python3')
    throw "No python3 function found. Read the jiravim-python3-compile help section for more information."
endif

" Check that all pip dependencies are installed
python3 import python.util.pip_check

" Check that Tabularize command from Tabular is available
if !exists(":Tabularize")
    set runtimepath += expand("<sfile>:p:h") . "../tabular/"
endif

" Check that credential variables are set
if !exists("g:jiraVimDomainName")
    throw "Please set 'g:jiraVimDomainName'. Refer to the 'jiravim-credentials' help tag for more information."
endif

if !exists("g:jiraVimEmail")
    throw "Please set 'g:jiraVimEmail'. Refer to the 'jiravim-credentials' help tag for more information."
endif

if !exists("g:jiraVimToken")
    throw "Please set 'g:jiraVimToken'. Refer to the 'jiravim-credentials' help tag for more information."
endif

" }}}

" Globally used python and vim functions/scripts {{{

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
"}}}
