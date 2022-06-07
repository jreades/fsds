#! /usr/bin/python

import os, re

# Convert Slideas-formatted Markdown to Reveal.js-formatted Markdown

def extract_meta(txt:str, theme:str='serif') -> str:
    meta = {'slide-format':'revealjs'}
    for arr in [s.split(':') for s in txt.split('\n')]:
        try:
            k = arr[0]
            v = arr[1]

            if k not in ['Theme','Size','Palette']:
                meta[k.lower()] = v

        except IndexError:
            pass

    output = """---
format:
  revealjs:
    theme: serif
"""
    for k,v in meta.items():
        output += f'{k}: {v}\n'
    output += '---\n'
    return output

def extract_notes(txt:str) -> str:
    notes = ['::: {.notes}']
    for l in txt.split("\n"):
        if l.startswith("^"):
            notes.append(l.replace('^ ',''))
    notes.append(':::\n')

    if len(notes)==2:
        return ""
    else:
        return "\n\n".join(notes)+"\n"

def process_split(content:str) -> str:

    output = [':::: {.columns}','::: {.column width="50%"}']
    slice_start = 1
    try:
        slice_end = content.index(next((x for x in content[slice_start:] if x.startswith('^')), None))
    except ValueError:
        slice_end = -1
    cslice  = content[slice_start:slice_end]

    for c in cslice:
        if c.startswith('+++'):
            output.append(':::')
            output.append('::: {.column width="50%"}')
        else:
            output.append(c)

    output.append(':::')
    output.append('::::\n')

    return "\n".join(output)

def format_head(txt:str) -> str:
    m = re.match(r'^#+',txt)
    # Already a level 1 header
    if m.end()==1:
        return txt
    else:
        return txt.replace('#','',1)

def process_page(txt:list, page_num:int) -> str:

    raw = txt.split("\n")

    output   = []
    title    = None
    notes    = extract_notes(txt)
    code_end = None

    for i, t in enumerate(raw):
        
        if code_end != None and i < code_end: continue
        
        if t.startswith('Layout: Split'):
            # Special format for Slideas split-screen
            output.append(process_split(raw[i:]))
            break
        elif t.startswith('```'):
            # Pass through code output as-is until we reach end of block.
            # +2 b/c we need to compensate for starting search for
            # end of clode block one *after* the start of the slice
            code_end = i+2+list(raw[i+1:]).index('```')
            #print(f'raw[{i},{code_end}]')
            #print('\n'.join(raw[i:code_end]))
            output    = output + raw[i:code_end]
        elif t.startswith('Background: ') or t.startswith('^') or t.startswith('Layout:'):
            # We've handled footnotes elsewhere, rest are irrelevant Slideas options
            pass
        elif t.startswith('#'):
            # Here we deal with things that look like headers -- if 
            # there were code comments we *should* have dealt with 
            # these using the code output block above
            if title==None and (t.startswith('# ') or t.startswith('## ')):
                # Pass through as-is
                title = t
            elif title==None and t.startswith('### '):
                # Promote to level 2
                title = t.replace('#','',1)
            elif t.startswith('## '):
                # Reveal.js doesn't seem to do subtitles so demote
                output.append(t.replace('## ','### ',1))
            elif t.startswith('### '):
                # Pass through as-is
                output.append(t)
        else:
            output.append(t)
    
    if not title:
        output.insert(0,'---\n')
    elif page_num > 1: 
        output.insert(0,title + " {.smaller}" if len(output) > 10 else title)
    
    output.append(notes)
    return "\n".join(output)

mypath = '.'
slideas_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) and f.endswith('.md')]

mypath = os.path.join('..','lectures')
reveal_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]

rm_image_params = re.compile(r'\!\[(?:inline\s?|fit\s?|left\s?|right\s?|filtered\s?|\d+\%\s?){1,}]\(')

for src in slideas_files:
    original  = os.path.getmtime(src)
    
    try:
        converted = os.path.getmtime(os.path.join('..','lectures',src.replace('.md','.qmd')))
    except FileNotFoundError:
        converted = 0

    if converted - original > 0:
        print(f"Found converted copy of {src}")
    else:
        if re.match(r'\d+\.\d+-',src):
            print(f"Converting {src}")
            with open(src,'r') as f:
                pages = f.read().split('---\n')

            content = extract_meta(pages.pop(0))
            for i, p in enumerate(pages):
                    content += process_page(p,i)
            content += '# Thank you!'
            
            content = rm_image_params.sub(r'![](', content)
            
            with open(os.path.join('..','lectures',src.replace('.md','.qmd')),'w') as f:
                f.write(content)

print('Done!')