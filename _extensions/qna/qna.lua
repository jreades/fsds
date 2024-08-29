-- Supports:
-- qna:
--   pdf: answer
--   html: both
--   ipynb: question
-- pandoc.utils.stringify might be useful

local pdf_target   = nil
local ipynb_target = nil
local html_target  = nil

Meta = function(meta) 
  local qnaMeta = meta.qna
  if qnaMeta ~= nil and type(qnaMeta) == 'table' then
    if qnaMeta.pdf ~= nil then
      -- print(qnaMeta.pdf)
      pdf_target = pandoc.utils.stringify(qnaMeta.pdf)
    else
      pdf_target = "answer"
    end
    if qnaMeta.html ~= nil then
      -- print(qnaMeta.html)
      html_target = pandoc.utils.stringify(qnaMeta.html)
    else
      html_target = "both"
    end
    if qnaMeta.ipynb ~= nil then
      -- print(qnaMeta.ipynb)
      ipynb_target = pandoc.utils.stringify(qnaMeta.ipynb)
    else
      ipynb_target = "question"
    end
  end
  -- print('PDF Target: ', pdf_target)
  -- print('HTML Target: ', html_target)
  -- print('IPYNB Target: ', ipynb_target)
  -- print("End")
end

function Div(div)
  if not div.classes:includes("qna") then 
    return
  end

  raw = {}
  local div_num = 0
  local header_level = 0

  -- print("~~~~~ Q&A div found ~~~~~")
  -- for key, value in pairs(div) do
  --   print(key, value)
  -- end
  -- print('PDF Target: ', pdf_target)
  -- print('IPYNB Taget: ', ipynb_target)
  -- print('HTML Target: ', html_target)
  -- print("~~~~~~~~~~~~~~~~~~~~~~~~~")

  div:walk({
    traverse = topdown,
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
        -- Do nothing
      end,
      Plain = function(pl)
        -- print('Plain called')
        -- print(pl.content)
        -- print(pl.tag)
        return pl -- table.insert(raw[div_num].content, pl)
      end,
      BlockQuote = function(bl)
        -- This is kind of weird but basically div:walk
        -- also walks into the paragraph block *inside*
        -- the Blockquote, and Blockquote is only called
        -- after the Para function is called. So we have
        -- to go back and remove the excess output from
        -- the stack before adding the Blockquote back in.
        for i=1,#bl.content do
          table.remove(raw[div_num].content,#raw[div_num].content)
        end
        table.insert(raw[div_num].content, pandoc.BlockQuote(bl.content))
      end,
      Table = function(tbl)
        resource_attr = pandoc.Attr('', {'cell-output','cell-output-display'}, {})
        d = pandoc.Div(pandoc.Div(tbl), resource_attr)
        table.insert(raw[div_num].content, d)
      end,
      Div = function(div)
        -- print("~~~~ Div ~~~~")
        -- print(div.content)
        if next(div.classes) ~= nil and (div.classes:includes('cell') or div.classes:includes('cell-output')) then
          return
        else
          table.insert(raw[div_num].content, div)
        end
      end,
      CodeBlock = function(code)
        table.insert(raw[div_num].content, code)
      end,
      Para = function(para)
        table.insert(raw[div_num].content, para)
      end,
      BulletList = function(bl)
        table.insert(raw[div_num].content, bl)
      end,
      OrderedList = function(ol)
        table.insert(raw[div_num].content, ol)
      end,
      -- Notice that the header forces a new div
      -- container so this is where div_num is 
      -- incremented. Everything after this, and
      -- up to the next header, forms part of the 
      -- same div.
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
    -- print("ipynb")
    -- print("  Target: ", ipynb_target)
    -- print("  Question: ", ipynb_target == "question")
    if ipynb_target == "question" then
      table.remove(raw,2)
    elseif ipynb_target == "answer" then 
      table.remove(raw,1)
    else
      -- do nothing
    end
  elseif quarto.doc.is_format("pdf") then
    -- print("pdf")
    -- print("  Target: ", pdf_target)
    -- print("  Question: ", pdf_target == "question")
    if pdf_target == "question" then
      table.remove(raw,2)
    elseif pdf_target == "answer" then 
      table.remove(raw,1)
    else
      -- do nothing
    end
  elseif quarto.doc.is_format("html") then 
    -- print("html")
    -- print("  Target: ", html_target)
    -- print("  Question: ", html_target == "question")
    if html_target == "question" then
      table.remove(raw,2)
    elseif html_target == "answer" then 
      table.remove(raw,1)
    else
      -- do nothing
    end
  else
    print("No output format detected.")
  end
  
  if #raw == 1 then
    local resources = {}
    
    -- print("~~~~~")
    -- for key, value in pairs(raw[1].content) do
    --   print(key, value)
    -- end
    -- print("~~~~~")

    hd = pandoc.Header(header_level, raw[1].title, pandoc.Attr('', {'qna-question'}, {}))
    resources[1] = hd

    local nxt = nil

    for key, value in pairs(raw[1].content) do 
      -- print("~~~~~~~~~~~")
      -- print("Key: ", key)
      -- print("Value: ", value)
      -- print("Type: ", value.t)

      if value.t == 'CodeBlock' then 
        -- Basically, check here to see if we're on the next
        -- key in a code block which is most likely the code
        -- block's *output* (we save a ref to the 'next' item).
        -- So next should only have a value if we just *saw*
        -- a code block and processed its output as well.
        if nxt ~= nil then
          nxt = nil
        
        else
          -- Create a code div (cd)
          cd = pandoc.Div(value, pandoc.Attr('', {'cell'}, {}))
          -- print(" > cd: ", cd)

          -- We seem to have to assume that if the next 'thing'
          -- is a code block then it has to be output. I can't
          -- figure out how to get Lua to do this properly by
          -- checking the class of the next output to see if 
          -- it's new code in a separate block or output of code.
          nxt = raw[1].content[key+1]
          -- If the next thing looks like it is likely code output
          if (nxt ~= nil and nxt.t == 'CodeBlock' and nxt.text ~= nil) then

            -- Create the code output (co)
            co = pandoc.Div(nxt, pandoc.Attr('', {"cell-output", "cell-output-stdout"}, {}))
            -- print(" > co: ",co)
            
            -- And insert it into the code div
            table.insert(cd.content,co)
          else
            nxt = nil
          end
          -- Add it to the resources stack
          resources[#resources+1] = cd
        end
      else
        resources[#resources+1] = value
      end
    end

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

-- Notice that we need to enforce processing of Meta
-- before the Div filter can work, otherwise the meta
-- values haven't been set before the filtering happens.
return {
  { Meta = Meta },
  { Div = Div},
}