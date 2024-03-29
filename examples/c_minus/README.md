# C-- language

An interpreter language with C-like syntax.

File tree

- [tests](tests): test codes written in C--
- [c_minus.gram](c_minus.gram): C-- grammar to generate parser
- [c_minus.lex](c_minus.lex): C-- tokens to generate lexer
- [code_generator.py](code_generator.py): This file generates machine code to be executed by [runenv.py](runenv.py)
- [runenv.py](runenv.py): Runtime environment to execute machine code.
- [ut_cmm.py](ut_cmm.py): C-- unit test.

Automatically generated files

- [cmm_lexer.py](cmm_lexer.py): C-- lexer
- [cmm_parser.py](cmm_parser.py): C-- parser
- [cmm_parser_table.py](cmm_parser_table.py): C-- parser table


## Semantic Analysis

## Runtime Environment

### Memory
- Code Area

- Global/Static Area

- Stack (grows downward)
  
  - free space

- Heap (grows upward)


### Functiona call process

```C++
int add(int a, int b)
{
    int c = a + b;
    return c;
}
```

call add(10, 20)

```
ldc 0 ; memory for return value [bp-12]
mst   ; push 0    -> reserve memory for pc (bp-8)
      ; push bp   -> store bp (bp-4)
      ; mark bp
      ; sp: not changed

ldc 10  ; argument 1, bp+0
ldc 20  ; argument 2, bp+4

cup add ; bp = marked bp
        ; [bp-8] = pc
        ; pc = addr(add)

add:
lda 0
lda 4
add
sto bp-12  ; return value
ret   ; pc = [bp-8]
      ; sp = bp - 8 (bp and pc)
      ; bp = [bp-4]

```
### Array
```C++
int a[10];

a[0] = 10;
// ind
//
//
```

### Procedure Activation Record
- Arguments

- Bookkeeping information, including return address

- Local data

- Local temporaries


## P-code
| P-code | Description |
|-|-|
| ldc_i32 *n*| load constant *n* and push onto the stack|
| lda *var*| load address of variable *var* and push onto the stack|
| lod_i32 *var*| load value of variable *var* and push onto the stack|
| ind_i32 *index*| pops address of an array from stack, add offset to the address, push value at the resulting location (indirect load). pop addr -> push *(*addr* + *index* * 4) |
| ixa *s*| indexed address. pop *addr*, pop *index* -> push (*addr* + *s* * *index*) |
| add_i32 | pops two 32-bit integers from the stack, add them, and push the result |
| sub_i32 | 32-bit integer subtraction|
| mul_i32 | 32-bit integer multiplication |
| div_i32 | 32-bit integer division |
| sto_i32 | Pop *addr* and 32-bit integer *val*. Then store to *(*addr*) = *val* |
| stn_i32 | read value at the top of the stack and store to address (stack preserved) |
| ent | entry |
| mst | mark stack (push 0 (for pc), push bp, marked_bp=sp)*.|
| cup | call user procedure (bp=marked_bp, sto bp-8)|
| csp | call standard (built-in) procedure (bp=marked_bp, sto bp-8)|
| ret | return (pop pc, sp=bp, pop bp)|
| equ | test if two values equal |
| jmp | unconditional jump |
| jpt | jump if true |
| jpf | jump if false|
| stp | stop |

- i32: 32-bit integer
- f32: 32-bit single precision floating point
- *: marked_bp is saved not to pop function arguments from stack at the end of the function call.

## Standard Procedure
Currently implemented standard (build-in) procedures are described in the table.

| Function | Description |
| - | - |
| printf | printf. |


## Directives

| Macro | Description |
| - | - |
| .global {size} | define the size of global/static area |
| .data | define the start of data section |
| db {addr} {values} | define bytes. |
| .code | define the start of code section |







