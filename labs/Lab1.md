# Lab 1

### Daniel Gisolfi

## Crafting a Compiler

#### 1.11 How does MOSS differ from other approaches for detecting possible plagiarism?

Differing from just reading the text in the files and looking for similarities, MOSS compiles the code and actually compares the tokens of the Abstract syntax tree, which allows it to even compare different languages.

#### 3.1 Assume the following text is presented to a C scanner: 

```c
main(){
 const float payment = 384.00; float bal;
 int month = 0;
 bal=15000;
 while (bal>0){ 
        printf("Month: %2d Balance: %10.2f\n", month, bal); bal=bal-payment+0.015*bal;
        month=month+1; 
	} 
} 
```

What token sequence is produced? For which tokens must extra infor- mation be returned in addition to the token code? 

Tokens: T_FUNCTION, T_L_PAREN, T_R_PAREN, T_L_BRACKET, T_CONST, T_TYPE, T_ID, T_ASSIGN_OP, T_DIGIT, T_TYPE, T_ID, T_EOL, T_TYPE, T_ID, T_ASSIGN_OP, T_DIGIT, T_EOL, T_ID, T_ASSIGN_OP, T_DIGIT, T_EOL, T_WHILE, T_L_PAREN, T_ID, T_GREATER_THAN, T_DIGIT, T_L_PAREN, T_L_BRACKET, T_PRINTF, T_L_PAREN, T_STRING, T_ID, T_ID, T_R_PAREN, T_EOL, T_ID,T_ASSIGN_OP, T_SUBTRACT_OP, T_ID,T_ADD_OP, T_DIGIT, T_ID, T_EOL, T_ID, T_ASSIGN_OP, T_ID, T_DIGIT, T_EOL, T_R_BRACKET, T_R_BRACKET

## Dragon

#### 1.1.4 A compiler that translates a high-level language into another high-level language is called a *source-to-source* translator. What advantages are there to using C as a target language for a compiler?

C is an old and popular language meaning  there are many compilers available and on many operating systems.

#### 1.6.1 For the block-structured C code below, indicate the values assigned to w, x, y, and z.

``` c
int w, x, y, z;
int i = 4; int j = 5;
{
  int j = 7;
  i = 6;
  w = i + j;
}
x = i + j;
{
  int i = 8;
  y = i + j;
}
z = i + j;
```

**x = 11, w = 13,  y = 13, z = 11**