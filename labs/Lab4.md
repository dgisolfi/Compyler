# Lab 4

### Daniel Gisolfi

## Crafting a Compiler

### 4.9

Compute First and Follow sets for the nonterminals of the following grammar. 
$$
S→a S e\\
→B\\
B→b B e\\
→C \\
C→c C e \\
→d
$$

|      | First Set | Follow Set          |
| ---- | --------- | ------------------- |
| S    | {aSe, B}  | {B, bBe, C, cCe, d} |
| B    | {C, cCe}  | {d}                 |
| C    | {d}       | epsilon             |



### 5.10

if expr then if expr then other else other 

**tree 1**

```
-[S]
--[Stmt]
---[if]
---[expr]
---[then]
---[Stmt]
----[if] 
----[expr]
----[then]
----[other]
---[else]
---[Stmt]
----[other]
--[$]
```

**tree 2**

```
-[S]
--[Stmt]
---[if]
---[expr]
---[then]
---[Stmt]
----[other]
-----[if] 
-----[expr]
-----[then]
-----[other]
----[else]
----[Stmt]
-----[other]
--[$]
```

## Dragon

### 4.4.3

```
 S -> A
 A -> (S) S A | ε
```

| S    | S -> A              | S -> A | S -> A |
| ---- | ------------------- | ------ | ------ |
| A    | A -> (S) S A A -> ε | A -> ε | A -> ε |