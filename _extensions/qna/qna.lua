local function render_quarto_tab_orig(tbl, tabset)
  local content = quarto.utils.as_blocks(tbl.content)
  local title = quarto.utils.as_inlines(tbl.title)
  local inner_content = pandoc.List()
  inner_content:insert(pandoc.Header(tabset.level, title))
  inner_content:extend(content)
  return pandoc.Div(inner_content)
end

local function render_quarto_tab(tbl, hlevel)
  local content = quarto.utils.as_blocks(tbl.content)
  local title = quarto.utils.as_inlines(tbl.title)
  local inner_content = pandoc.List()
  inner_content:insert(pandoc.Header(hlevel, title))
  inner_content:extend(content)
  return pandoc.Div(inner_content)
end

function Div(div)
  if not div.classes:includes("qna") then 
    return
  end

  raw = {}
  local div_num = 0
  local header_level = 0

  -- print("~~~~~ Q&A ~~~~~")
  -- for key, value in pairs(div) do
  --   print(key, value)
  -- end
  -- print("~~~~~~~~~~~~~~")

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
        return -- {}
      end,
      Div = function(div)
        -- print("~~~~ Div ~~~~")
        -- print(div.content)
        if next(div.classes) ~= nil and (div.classes:includes('cell') or div.classes:includes('cell-output')) then
          return -- {}
        else
          table.insert(raw[div_num].content, div)
        end
      end,
      CodeBlock = function(code)
        table.insert(raw[div_num].content, code)
      end,
      Para = function(para)
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
        -- print("~~~~ Header ~~~~", header.content)
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
    table.remove(raw,2)
  elseif quarto.doc.is_format("pdf") then
    table.remove(raw,1)
  elseif quarto.doc.is_format("html") then 
    -- do nothing
  else
    print("No output format detected.")
  end
  
  if #raw == 1 then
    local resources = {}
    local content   = {}
    
    -- print("~~~~~")
    -- for key, value in pairs(raw[1].content) do
    --   print(key, value)
    -- end
    -- print("~~~~~")

    cb = pandoc.CodeBlock(raw[1].content[1].text, pandoc.Attr('', {'python','cell-code'}, {}))
    cd = pandoc.Div(cb, pandoc.Attr('', {'cell'}, {}))
    if (raw[1].content[2] ~= nil and raw[1].content[2].t == 'CodeBlock') then
      co = pandoc.Div(raw[1].content[2].text, pandoc.Attr('', {"cell-output", "cell-output-stdout"}, {}))
      table.insert(cd.content,co)
    end
    hd = pandoc.Header(header_level, raw[1].title, pandoc.Attr('', {'qna-question'}, {}))

    resources[1] = hd
    resources[2] = cd

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
