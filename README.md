# Database-ball

<img src="readme/default-view.png" alt="default-view" width=961 height=423> 

## About <i>Database-ball</i>
Database-ball provides an interactive way of analyzing all kinds of baseball statistics, from your traditional ones like batting average, home runs, and RBIs, to more advanced ones like slugging, OPS, and OPS+, to an even cooler one I created myself: the **Quality/Quantity (QQ) Metric**.

## The <i>Quality/Quantity (QQ) Metric</i>
The QQ Metric applies an "adjustment factor" to a player's [OPS+](https://www.mlb.com/glossary/advanced-stats/on-base-plus-slugging-plus) (a normalized stat measuring offensive performance) based on how many plate appearences they had. This rewards players who provide both "Quality" and "Quantity" in abundance. Here is how it's calculated:

<img src="images/qq_formula.png" alt="formula" width=514 height=107>

The graph of the adjustment factor function (the (-2^-x+1)^6) part, with the x values multiplied by 112 in order to fit the graph in a smaller frame) looks like this:

<img src="readme/adjustment_function.png" alt="adjustment function graph" width=775 height=281>

As you can see, the curve flattens out as x increases, so the adjustment factor changes less dramatically for players with a high number of plate appearences.

## Examples of the QQ Metric in action
Here is Ted Williams' QQ Metric for each season of his career.
| Year | Age | QQ Metric | PA | OPS+ |
|------|-----|-----------|----|------|
| 1939 | 20 | 146 | 677 | 160 |
 | 1940 | 21 | 146 | 661 | 162 |
 | 1941 | 22 | 204 | 606 | 235 |
 | 1942 | 23 | 196 | 671 | 216 |
 | 1946 | 27 | 196 | 672 | 215 |
 | 1947 | 28 | 189 | 693 | 205 |
 | 1948 | 29 | 168 | 638 | 189 |
 | 1949 | 30 | 179 | 730 | 191 |
 | 1950 | 31 | 104 | 416 | 168 |
 | 1951 | 32 | 149 | 675 | 164 |
 | 1952 | 33 | 0 | 12 | 273 |
 | 1953 | 34 | 4 | 110 | 268 |
 | 1954 | 35 | 159 | 526 | 201 |
 | 1955 | 36 | 130 | 417 | 209 |
 | 1956 | 37 | 131 | 503 | 172 |
 | 1957 | 38 | 189 | 547 | 233 |
 | 1958 | 39 | 139 | 517 | 179 |
 | 1959 | 40 | 50 | 331 | 114 |
 | 1960 | 41 | 108 | 390 | 190 |
  
## About the tech
I decided to use [H2O Wave](https://wave.h2o.ai/docs/guide) to make this app because of its nice data visualization features. I also liked its functional programming model and thought it would be really fun to use.
