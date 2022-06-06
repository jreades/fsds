#! /usr/bin/python

# Convert Slideas-formatted Markdown to Reveal.js-formatted Markdown

def update_meta(txt:str, theme:str='serif') -> str:
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
    return output

def extract_notes(txt:str) -> str:
    notes = ['::: {.notes}']
    for l in txt.split("\n"):
        if l.startswith("^"):
            notes.append(l.replace('^ ',''))
    notes.append(':::')
    return "\n\n".join(notes)

def process_page(txt:str) -> str:

    print(txt)

    print(extract_notes(txt))
    output = "---"

fn = '5.4-Pandas'

with open(f'{fn}.md','r') as f:
    pages = f.read().split('---')

meta = update_meta(pages.pop(0))

print(process_page(pages[1]))