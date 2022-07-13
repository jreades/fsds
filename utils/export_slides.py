#! /Users/jreades/opt/anaconda3/bin/python

# Convert Reveal.js slides to PDF and PNG
# You will need to have installed decktape for
# this script to work. Documentation for that 
# is available here: https://github.com/astefanutti/decktape

import os, re
import subprocess

print(f"Working in: {os.getcwd()}")
remote_path = 'lectures'

reveal_path = os.path.join('docs',remote_path) # Because we're hosting on GitHub pages
reveal_files = [f for f in os.listdir(reveal_path) if os.path.isfile(os.path.join(reveal_path,f))] and f.startswith('3.1')]
#print(reveal_files)

export_path = os.path.join('export')
slides = [f for f in os.listdir(export_path) if os.path.isdir(os.path.join(export_path,f)) and f.endswith('.pdf') ]

for src in reveal_files:

    print(f"Source reveal.js slide deck: {src}")

    original  = os.path.getmtime(os.path.join(reveal_path,src))

    #print(f"  Has mod time {original}")

    sub_dir = os.path.join(export_path,src.replace('.html',''))
    #print(f"Writing to sub directory: {sub_dir}")
    
    try:
        #print(f"Converted PDF file: {os.path.join(sub_dir,src.replace('.html','.pdf'))}")
        converted = os.path.getmtime(os.path.join(sub_dir,src.replace('.html','.pdf')))
        #print(f"  Has mod time {converted}")
    except FileNotFoundError:
        #print(f"  Has not been created yet.")
        converted = 0

    if converted - original > 0:
        print(f"Found recent converted copy of {src}")
    else:
        if re.match(r'\d+\.\d+-',src):
            #print(f"Converting {src}")

            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

            # Access the Quarto server
            reveal_url = "/".join(['http://localhost:4200',remote_path,src])
            #print(f"URL: {reveal_url}")

            # Call Decktape
            call = ['/usr/local/bin/decktape',
                '--screenshots', '--screenshots-format', 'png', '--screenshot-size', "'1280x720'",
                '--screenshots-directory', f"./{sub_dir}", 'reveal',
                reveal_url, src.replace('.html','.pdf')]
            #print("  ", " ".join(call))
            subprocess.run(call)

            try:
                os.rename(src.replace('.html','.pdf'), os.path.join(sub_dir,src.replace('.html','.pdf')))
            except FileNotFoundError:
                print(f"Couldn't move file {src.replace('.html','.pdf')} to {sub_dir}")
            

print('Done!')
