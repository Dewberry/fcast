# plotMediumRange
```python
plotMediumRange(df: pandas.core.frame.DataFrame, comid: int, flow: bool = True)
```

Function for plotting medium range forecasts. Set `flow = False` if plotting stage. `df` is the output of `ShortRange.get_streamflow()`.