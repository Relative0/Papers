function Table(t)
  if #t.colspecs == 5 then
    local widths = {0.40, 0.10, 0.12, 0.12, 0.26}
    for i = 1, 5 do
      t.colspecs[i][2] = widths[i]
    end
  end
  return t
end
