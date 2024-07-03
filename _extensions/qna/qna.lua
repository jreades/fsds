function Div(div)
  if not div.classes:includes("qna") then 
    return
  end

  raw = {}
  local div_num = 0
  local header_level = 0

  div:walk({
      Block = function(block)
        print('vvvv')
        print("Unknown block of type " .. block.t)
        if next(block.classes) ~= nil then
          print("Has classes: ")
          print(block.classes)
        end 
        print("Has attributes: ")
        for k,v in pairs(block.attributes) do
          print(k)
          print(v)
        end
        print('^^^^')
      end,
      RawBlock = function(r)
        return
      end,
      BlockQuote = function(bl)
        return
      end,
      Table = function(tbl)
        resource_attr = pandoc.Attr('', {'cell-output','cell-output-display'}, {})
        d = pandoc.Div(pandoc.Div(tbl), resource_attr)
        table.insert(raw[div_num].content, d)
        return {}
      end,
      Div = function(div)
        if next(div.classes) ~= nil and (div.classes:includes('cell') or div.classes:includes('cell-output')) then
          return {}
        else
          table.insert(raw[div_num].content, div)
        end
      end,
      CodeBlock = function(code)
        -- print(code.attr)
        -- print(code.text)
        local resource_attr = pandoc.Attr('', {'cell','code'}, {})
        -- print(code.classes)
        if not code.classes:includes('code') then 
          code.classes:insert('code')
          code.classes:insert('cell')
        end
        -- print(code.classes)
        table.insert(raw[div_num].content, code) -- pandoc.Div(code, resource_attr))
      end,
      Para = function(para)
        -- print("-----")
        -- print(raw)
        -- print(para)
        -- print("-----")
        table.insert(raw[div_num].content, para)
        -- table.insert(raw[#raw].content, para)
      end,
      BulletList = function(bl)
        table.insert(raw[div_num].content, bl)
      end,
      OrderedList = function(ol)
        table.insert(raw[div_num].content, ol)
      end,
      Plain = function(pl)
        return pl -- table.insert(raw[div_num].content, pl)
      end,
      Header = function(header)
        if header_level == 0 then
          header_level = header.level
        end
        if header.level == header_level then
          div_num = div_num + 1
          raw[div_num] = {}
          raw[div_num]['title'] = header.content
          raw[div_num]['content'] = {}
        else
          table.insert(raw[div_num].content, header)
        end
      end
    })
  
  -- Note the critical assumption that the question
  -- is always the first tab, the answer is always
  -- the second. We remove the question *or* answer
  -- for some output formats based on filter spec
  if quarto.doc.is_format("ipynb") then
    print("Writing Notebook!!!")
    table.remove(raw,2)
  elseif quarto.doc.is_format("pdf") then
    print("Writing PDF!!!")
    table.remove(raw,1)
  end
  
  if #raw == 1 then
    local resources = {}
    local resource_attr = pandoc.Attr('', {'qna-question'}, {})
    resources[1] = pandoc.Header(header_level, raw[1].title, resource_attr)
    resources[2] = pandoc.Div(raw[1].content, resource_attr)
    return resources
  else
    tabs = {}
    for i, t in pairs(raw) do
      table.insert(tabs, quarto.Tab({title=t.title, content=t.content}) )
    end

    return quarto.Tabset({
      level = 3,
      tabs = pandoc.List( tabs ),
      attr = pandoc.Attr("", {"panel-tabset", "qna-question"}) -- this shouldn't be necessary but it's the bug I mentioned.
    })
  end
end
