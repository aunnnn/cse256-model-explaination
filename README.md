# cse256-model-explanation
Final project for CSE-256

Team members:
- Wirawit Rueopas (A53277204)
- Saideep Reddy Pakkeer (A53269319)


## Installation
This project is built with [Dash](https://dash.plot.ly), a Python framework for building interactive web applications.

Install Dash:
https://dash.plot.ly/installation

## To Run
`python app.py`

## Development Guideline

The project uses the grid system from [Skeleton.css](http://getskeleton.com/), with its wrapper functions in `components/utils.py`.  Basically a webpage consists of rows, where a row has 12 columns inside it.

Coding a layout goes like this:
1. Add a block that fills webpage horizonally with `Row(...)`
2. Inside `...` of `Row` you can add an array of `MultiColumn(...)` (or, simply one `Div`)
3. Inside `...` of `MultiColumn` you can add web components, e.g., `Div`

E.g., a layout with three equal columns:
```python
layout = Row([
  MultiColumn(4, Div("Column 1")),
  MultiColumn(4, Div("Column 2")),
  MultiColumn(4, Div("Column 3")),
])
```

Or a layout with two columns but the second column is 3x more wide:
a layout with one row and two equal columns:
```python
layout = Row([
  MultiColumn(3, Div("Column 1")),
  MultiColumn(9, Div("Column 2")),
])
```

That is, just makes sure array of `MultiColumn` sums up to 12.
