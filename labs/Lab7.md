# Lab 7

### Daniel Gisolfi

## Dragon

### 6.3.1

Determine the typ es and relative addresses for the identi􏰁ers in the following sequence of declarations􏰖:

```
float x;
record {float x; float y;} p;
record {int tag; float x; float y;} q;
```

|  ID  |   Type   | Line |
| :--: | :------: | :--: |
|  x   |  float   |  1   |
|  x   |  float   |  2   |
|  y   |  float   |  2   |
|  p   | record() |  2   |
| tag  |   int    |  3   |
|  x   |  float   |  3   |
|  y   |  float   |  3   |
|  q   | record() |  3   |

