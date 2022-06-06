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
    notes.append(':::')

    if len(notes)==2:
        return ""
    else:
        return "\n\n".join(notes)+"\n"

def process_split(txt:str) -> str:

    content = txt.split("\n")

    output = [':::: {.columns}\n','::: {.column width="50%"}\n']
    try:
        slice_start = content.index('Layout: Split')+1
    except ValueError:
        print("Unable to located start of slice!")
        print(content)
        exit()
    try:
        slice_end = content.index(next((x for x in content[slice_start:] if x.startswith('^')), None))
    except ValueError:
        slice_end = -1
    cslice  = content[slice_start:slice_end]

    for c in cslice:
        if c.startswith('+++'):
            output.append(':::\n')
            output.append('::: {.column width="50%"}\n')
        else:
            output.append(c)

    output.append(':::\n')
    output.append('::::\n')

    return "\n".join(output)

def process_page(txt:list) -> str:
    output = []
    #print(txt)
    
    for t in txt.split("\n"):
        if t.startswith('Layout: Split'):
            output.append(process_split(txt))
            break
        elif not t.startswith("^") and not t.startswith("Layout: "):
            if t.startswith('## Resources'):
                output.append(t + " {.smaller}")
            else:
                output.append(t)

    output.append(extract_notes(txt))
    output.append("---\n")
    return "\n".join(output)

mypath = '.'
slideas_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) and f.endswith('.md')]

mypath = os.path.join('..','lectures')
reveal_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]

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

            with open(os.path.join('..','lectures',src.replace('.md','.qmd')),'w') as f:

                f.write(extract_meta(pages.pop(0)))

                for p in pages:
                    f.write(process_page(p))
                
                f.write('## Thank you!')

print('Done!')