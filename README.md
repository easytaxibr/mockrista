
Simple Server for Mock
----------------------

A simple python server to mock random taxi position for appliance test on Easy Taxi

Usage
-----

```shel
python simpleserver.py <port> <ip>
```

End-points
----------

```shel
GET /api/taxi-position/the-taxi
```
Parameter | Type | Description
---|---|---
`session` | **int** | *Any given number just to make the session
control. If you want a constant taxi position just provide the same
number in all your requests*

```shel
GET /api/gettaxis
```

Parameter | Type  | Description
---|---|---
`lat` | **float** | *Center latitude to plot taxi positions*
`lng` | **float** | *Center longitude to plot taxi positions*

Fork and enjoy it :D.
