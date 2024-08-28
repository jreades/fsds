#!/bin/sh
pandoc Syllabus.md \
  -H ./bib/head.tex \
  -H ./bib/chapter.tex \
  -H ./bib/refs.tex \
  -V documentclass=memoir \ 
  --pdf-engine=xelatex \
  --filter=pandoc-citeproc \
  --metadata-file=metadata.yml \
  --highlight-style=pygments \ 
  -o Syllabus.pdf
