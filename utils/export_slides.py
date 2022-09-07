#! /Users/jreades/opt/anaconda3/bin/python

# Convert Reveal.js slides to PDF and PNG
# You will need to have installed decktape for
# this script to work. Documentation for that 
# is available here: https://github.com/astefanutti/decktape
# But it boils down to `npm install -g decktape`

import os, re
import subprocess

# The 'remote path' is the path in a running 
# Quarto instance. The 'reveal path' is where
# to find the *same content* locally. We do 
# this because we are going to read in the 
# local directory to find all the .qmd files, 
# and then turn around and request those *same*
# files in their rendered format from the Quarto
# server. Otherwise you'd have to have a way to
# navigate the remote web site and, depending on
# how you've structured the site, that might be
# quite difficult. This assumes that most of your
# talks will be in the same folder because that's
# fairly logical in a teaching contenxt.
print(f"Working in: {os.getcwd()}")
remote_path = 'lectures'
reveal_path = os.path.join('docs',remote_path) 
export_path = os.path.join('export')

# Other configuration parameters
quarto_url = 'http://localhost:4200'

# All the potential reveal files... 
reveal_files = [f for f in os.listdir(reveal_path) if os.path.isfile(os.path.join(reveal_path,f))] 

# And everything on the exported site
slides = [f for f in os.listdir(export_path) if os.path.isdir(os.path.join(export_path,f)) and f.endswith('.pdf') ]

for src in reveal_files:

    print(f"Source reveal.js slide deck: {src}")

    # Where are we sending the output (the PNG files)
    sub_dir = os.path.join(export_path,src.replace('.html',''))
    #print(f"Writing to sub directory: {sub_dir}")

    # When was the original last modified?
    original = os.path.getmtime(os.path.join(reveal_path,src))
    #print(f"  Has mod time {original}")

    # When was the output last modified (if it exists)?
    # The reason we're looking for a PDF file even though
    # we *want* PNG files is that Decktape seems to generate
    # a PDF even when all we're trying to do is make PNGs. 
    # THe *one* useful outcome of this is that it's easy to
    # check (down below) the last modified date of the PDF
    # against the original QMD file to see which is more 
    # recently-modified.
    try:
        converted = os.path.getmtime(os.path.join(sub_dir,src.replace('.html','.pdf')))
        #print(f"Converted PDF file: {os.path.join(sub_dir,src.replace('.html','.pdf'))}")
        #print(f"  Has mod time {converted}")
    except FileNotFoundError:
        converted = 0
        #print(f"  Has not been created yet.")

    # Now check the last modified of the input and
    # output files to see if we need to update the
    # output.
    if converted - original > 0:
        print(f"Found recent converted copy of {src}")
    else:
        # Notice the assumption here that all lectures/files
        # to be converted start with this regex!
        if re.match(r'\d+\.\d+-',src):

            #print(f"Converting {src}")

            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

            # Access the Quarto server
            reveal_url = "/".join([quarto_url,remote_path,src])
            #print(f"URL: {reveal_url}")

            # Call Decktape -- slightly annoyingly this also 
            # creates a PDF file even if we ask it not to do so.
            call = ['/usr/local/bin/decktape',
                '--screenshots', '--screenshots-format', 'png', '--screenshot-size', "'1280x720'",
                '--screenshots-directory', f"./{sub_dir}", 'reveal',
                reveal_url, src.replace('.html','.pdf')]
            #print("  ", " ".join(call))
            subprocess.run(call)

            # Even more annoyingly it doesn't *seem* to be possible
            # to tell it where to save the PDF it is creating as part
            # of the PNG-creation process!
            try:
                os.rename(src.replace('.html','.pdf'), os.path.join(sub_dir,src.replace('.html','.pdf')))
            except FileNotFoundError:
                print(f"Couldn't move file {src.replace('.html','.pdf')} to {sub_dir}")
            
print('Done!')
