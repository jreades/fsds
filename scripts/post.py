print("~" * 50)
msg = """Don't forget to also generate the answer PDFs using:\n    quarto render --profile pracs practicals\nThese are generated to `_answers` using the `prac` profile while the web content is in `_site`."""
print(msg)
print("~" * 50)
print("To publish once you've rendered run: `quarto publish gh-pages --no-render`")
