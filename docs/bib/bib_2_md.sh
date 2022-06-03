#! /bin/sh
pandoc -t markdown_strict --filter=pandoc-citeproc --standalone Template.md -o Bibliography.md
