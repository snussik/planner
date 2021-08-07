# Planner class

## Generating the datetimes list in the set bounds of period and time

## Installing
`pip install git+https://github.com/snussik/planner.git`

## Useing

```python
p = Planner(
    period='week',
    timerange=[(12,13), (14,15), (16,17)],
    frequency='daily',
    min_max_interval=(3600, 7200)
)

print(p.post_intervals)
```