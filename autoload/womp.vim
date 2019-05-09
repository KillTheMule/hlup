if ! exists('s:jobid')
  let s:jobid = 0
endif

  let s:scriptdir = resolve(expand('<sfile>:p:h') . '/..')
  "let s:bin = s:scriptdir . '/files/redir.sh' 
  let s:bin = s:scriptdir . '/womp.py'

function! womp#connect()
  let result = s:StartJob()

  if 0 == result
    echoerr "Womp: cannot start rpc process"
  elseif -1 == result
    echoerr "Womp: rpc process is not executable: " . s:bin
    echoerr s:bin
  else
    let s:jobid = result
    echom "Result was" . s:jobid
    call s:ConfigureJob(result)
  endif
endfunction

function! womp#do_something()
  if s:jobid > 0
    return rpcrequest(s:jobid, 'do_something')
  else
    return "a"
endfun

function! womp#stop()
  call s:StopJob()
endfunction

function! s:ConfigureJob(jobid)
  augroup womp
    autocmd!
    autocmd VimLeavePre * :call s:StopJob()
  augroup END
endfunction

let s:stderr_chunks = ['']
function! s:OnStderr(id, data, event) dict
  let s:stderr_chunks[-1] .= a:data[0]
  call extend(s:stderr_chunks, a:data[1:])
endfunction

function! s:StartJob()
  if 0 == s:jobid
    let id = jobstart([s:bin], { 'rpc': v:true, 'on_stderr': function('s:OnStderr') })
    echom "Started"
    echom id
    return id
  else
    return 0
  endif
endfunction

function! s:StopJob()
  call writefile(s:stderr_chunks, "stderr")
  if 0 < s:jobid
    augroup womp
      " clear all previous autocommands
      autocmd!
    augroup END
      echom s:jobid

    call rpcnotify(s:jobid, 'quit')
    let result = jobwait([s:jobid], 500)[0]

    if -1 == result
      "kill the job
      call jobstop(s:jobid)
    endif

  endif
  "
  " reset job id back to zero
  let s:jobid = 0
endfunction
