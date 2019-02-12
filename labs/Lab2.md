# Lab 2

### Daniel Gisolfi

## Crafting a Compiler

#### 3.3 Write regular expressions that define the strings recognized by the FAs in Figure 3.33 on page 107. 

1. (ab|ba)*(aba|bab)^+^
2. (a(b|(c)^+^)(d)*
3. (a(b)^+^c)

#### 3.4

1. (a|(bc)*d)+

    | NFA STATE                 | DFA STATE | TYPE   | a    | b    | c    | d    |
    | ------------------------- | --------- | ------ | ---- | ---- | ---- | ---- |
    | {0,1,3,4,7}               | A         |        | B    | C    |      | D    |
    | {2,9,10,11,13,14,17,20}   | B         | accept | E    | F    |      | G    |
    | {5}                       | C         |        |      |      | H    |      |
    | {8,9,10,11,13,14,17,20}   | D         | accept | E    | F    |      | G    |
    | {10,11,12,13,14,17,19,20} | E         | accept | E    | F    |      | G    |
    | {15}                      | F         |        |      |      | I    |      |
    | {10,11,13,14,17,18,19,20} | G         | accept | E    | F    |      | G    |
    | {4,6,7}                   | H         |        |      | C    |      | D    |
    | {14,16,17}                | I         |        |      | F    |      | G    |

2. ((0|1)*(2|3)+)|0011

    | NFA STATE                | DFA STATE | TYPE   | 0    | 1    | 2    | 3    |
    | ------------------------ | --------- | ------ | ---- | ---- | ---- | ---- |
    | {0,1,2,3,5,8,9,11,21}    | A         |        | B    | C    | D    | E    |
    | {2,3,4,5,7,8,9,11,22}    | B         |        | F    | C    | D    | E    |
    | {2,3,5,6,7,8,9,11}       | C         |        | G    | C    | D    | E    |
    | {10,13,14,15,17,20,26}   | D         | accept |      |      | H    | I    |
    | {12,13,14,15,17,20,26}   | E         | accept |      |      | H    | I    |
    | {2,3,4,5,7,8,9,11,23}    | F         |        | G    | J    | D    | E    |
    | {2,3,4,5,7,8,9,11}       | G         |        | G    | C    | D    | E    |
    | {14,15,16,17,19,20,26}   | H         | accept |      |      | H    | I    |
    | {14,15,17,18,19,20,26}   | I         | accept |      |      | H    | I    |
    | {2,3,5,6,7,8,9,11,24}    | J         |        | G    | K    | D    | E    |
    | {2,3,5,6,7,8,9,11,25,26} | K         | accept | G    | C    | D    | E    |

3. (aNot(a))*aaa
    | NFA STATE | DFA STATE | TYPE   | N    | a    | o    | t    |
    | --------- | --------- | ------ | ---- | ---- | ---- | ---- |
    | {0,1,7}   | A         |        |      | B    |      |      |
    | {2,8}     | B         |        | C    | D    |      |      |
    | {3}       | C         |        |      |      | E    |      |
    | {9}       | D         |        |      | F    |      |      |
    | {4}       | E         |        |      |      |      | G    |
    | {10}      | F         | accept |      |      |      |      |
    | {5}       | G         |        |      | H    |      |      |
    | {1,6,7}   | H         |        |      | B    |      |      |

#### 3.15

![NFA](/Users/daniel/git/Compyler/labs/imgs/3-15NFA.png)



## Dragon

#### 3.3.4 Most languages are case sensitive, so keywords can be written only  one way, and the regular expressions describing their lexeme is very  simple. However, some languages, like SQL, are case insensitive, so a  keyword can be written either in lowercase or in uppercase, or in any  mixture of cases. Thus, the SQL keyword SELECT can also be written  select, Select, or sElEcT, for instance. Show how to write a regular expression for a keyword in a case­ insensitive language. Illustrate the idea by writing the expression for "select" in SQL.

```python
# Regex...
[Ss][Ee][Ll][Ee][Cc][Tt]
# in python...
ignorecase = re.compile('select', re.IGNORECASE)
```

