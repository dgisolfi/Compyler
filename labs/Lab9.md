# Lab 9

### Daniel Gisolfi

## Dragon

### 4.5.3

For the following input symbol string and grammar, the corresponding bottom-up parsing process is illustrated.

​     Practice the string of the grammar of 4.5.1 000111.
​     Practice the string grammar of 4.5.2 aaa*a++ .

1. 000111

```
$ 000111$ Move in
$0 00111$ Move in
$00 0111$ Move in
$000 111$ Move in
$0001 11$ 01 Statute: S -> 01
$00S 11$ Move in
$00S1 1$ 0S1 Statute: S -> 0S1
$0S 1$ Move in
$0S1 $ 0S1 Statute: S -> 0S1
$S $ accepted
```

2. aaa*a++
```
$ aaa*a++$ Move in
$a aa*a++$ a Statute: S -> a
$S aa*a++$ Move in
$Sa a*a++$ a Statute: S -> a
$SS a*a++$ Move in
$SSa *a++$ a Statute: S -> a
$SSS *a++$ Move in
$SSS* a++$ SS* Statute: S -> SS*
$SS a++$ Move in
$SSa ++$ a Statute: S -> a
$SSS ++$ Move in
$SSS+ +$ SS+ Statute: S -> SS+
$SS +$ move in
$SS+ $ SS+ Statute: S -> SS+
$S $ accepted
```

### 4.6.5

Explain the following grammar

S->AaAb|BbBa
A->ε
B->ε

It is LL(1), but not LR(1).
answer

```
I_0
S' -> .S
S -> .AaAb
S -> .BbBa
A -> .
B -> .
```
Since FOLLOW(A) = FOLLOW(B) = [a, b], a conflict occurs when the input is a or b

