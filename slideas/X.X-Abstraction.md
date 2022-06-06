Title: Abstraction
Author: Jon Reades
Theme: casa notes
Palette: Purple
Size: Wide

---
Layout: Title
# Automate All the Things

---
## Elements of Automation

The following are all integral to automation:
- Conditions
- Functions
- Exceptions

Also useful:
- Standard data format
 -Standard naming scheme

---
## Conditions

Useful for defining branching logic:
- I have two (or more) execution branches that I could follow at this point in my code, but I don't know which one I'll encounter when I automate my analysis.

For example:
- If the column is a float, continue with the analysis
- If the column is an integer, convert it to a float
- Else (the column is neither of these), pass

---
## Functions 

Useful for avoiding duplication and parameterising code:
- I need to create many charts and I want them to be output using a standardised scheme and with the same formatting.

For example, set up a function to: 
- Take as parameters: a column of data and an option to draw a line for the mean
- And output: a PDF version of your chart sized to A4, using specific fonts, and saved to your desktop using the name of the column as part of the file name (e.g. `"Summary Results for {0}".format(series.name)`)

---
## Exceptions 

Useful for trapping problems that you expect:
- I know that some of my columns won't contain numbers or might contain `NaN`s that can't be plotted; it doesn't mean there's a problem with the data that needs attention so I use an exception to cope with this.

For example:
- Try to create a plot from this column
- Except columns that throw a TypeError (which we expect to happen from time to time, so we 'trap' that error!)

---

> Abstraction knits this all together: we're not trying to solve the problem for just one column, but for as many columns as possible. 



