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
GET /api/gettaxis
```

Parameter | Type  | Description
---|---|---
`lat` | **float** | *Center latitude to plot taxi positions*
`lng` | **float** | *Center longitude to plot taxi positions*

Fork and enjoy it :D.
