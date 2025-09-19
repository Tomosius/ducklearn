# Charts (Vega-Lite)

The **vegalite** fence is configured via `pymdownx.superfences`.

## Bar chart

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "values": [
    {"x": "A", "y": 3},
    {"x": "B", "y": 7},
    {"x": "C", "y": 4}
  ]},
  "mark": "bar",
  "encoding": {
    "x": {"field": "x", "type": "ordinal", "title": "Category"},
    "y": {"field": "y", "type": "quantitative", "title": "Value"}
  }
}
```

## Line chart

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "values": [
    {"t": 1, "y": 2},
    {"t": 2, "y": 5},
    {"t": 3, "y": 4},
    {"t": 4, "y": 8}
  ]},
  "mark": {"type":"line", "point": true},
  "encoding": {
    "x": {"field": "t", "type": "quantitative", "title": "Time"},
    "y": {"field": "y", "type": "quantitative", "title": "Value"}
  }
}
```
