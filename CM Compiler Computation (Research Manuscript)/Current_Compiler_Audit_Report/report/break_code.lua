local function esc(c)
  local m = {['\\']='\\textbackslash{}',['{']='\\{',['}']='\\}',['_']='\\_',['%']='\\%',['$']='\\$',['&']='\\&',['#']='\\#',['~']='\\textasciitilde{}',['^']='\\textasciicircum{}'}
  return m[c] or c
end
function Code(el)
  if not FORMAT:match('latex') then return nil end
  local out = {}
  local run = 0
  for i=1,#el.text do
    local c=el.text:sub(i,i)
    table.insert(out,esc(c))
    run=run+1
    if c=='_' or c=='/' or c=='-' or c=='.' or (#el.text>30 and run>=10) then
      table.insert(out,'\\allowbreak{}')
      run=0
    end
  end
  return pandoc.RawInline('latex','\\texttt{'..table.concat(out)..'}')
end
