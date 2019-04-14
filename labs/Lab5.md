# Lab 5

### Daniel Gisolfi

## Crafting a Compiler

### 8.1 

The two data structures most commonly used to implement symbol tables in production compilers are binary search trees and hash tables. What are the advantages and disadvantages of using each of these data structures for symbol tables? 

> Although hash lookup times are quicker being an O(1) lookup time for a known key, the inefficiency in terms of memory is a large disadvantage for the hashtable. In comparison, the binary search tree has a relatively slower lookup time of O(n) however the tree is far more memory-efficient as they do not reserve more memory than needed.

### 8.3

Describe two alternative approaches to handling multiple scopes in a symbol table, and list the actions required to open and close a scope for each alternative. Trace the sequence of actions that would be performed for each alternative during compilation of the program in Figure 8.1. 

>When handling scope whith a symbol table the two approches available are static and dynamic. With static scoping, the structure of the program determines what variables are being refered to while with dynamic scoping, the runtime state of the program stack determines what variable you are referring to. In the case of figure 8.1, the re decleration variable x is handled differently in dynamic scoping depending on the current stack of the runtime while in static scoping in every case the initial x or global x is now redeclared within the new scope.