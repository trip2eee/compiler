# C-- language

## Semantic Analysis

## Runtime Environment

### Memory
- Code Area

- Global/Static Area

- Stack (grows downward)
  
  - free space

- Heap (grows upward)

#### Functiona call process

```C
int add(int a, int b)
{
    int c = a + b;
    return c;
}
```

call add(10, 20)

```
ldc 0 ; memory for return value [bp-4]
mst   ; push return address and bp, bp=sp, sp=bp

ldc 10
ldc 20

cup add

add:
lda 0
lda 4
add
sto bp-4
ret   ; sp=bp, pop bp, pop return address and jump

```

### Procedure Activation Record
- Arguments

- Bookkeeping information, including return address

- Local data

- Local temporaries


## P-code
| P-code | Description |
|-|-|
| ldc_i32 n| load constant n and push onto the stack|
| lda_i32 addr| load value from the address and push onto the stack|
| lod_i32 a| load value of variable a and push onto the stack|
| add_i32 | pops two 32-bit integers from the stack, add them, and push the result |
| sub_i32 | 32-bit integer subtraction|
| mul_i32 | 32-bit integer multiplication |
| div_i32 | 32-bit integer division |
| sto_i32 | pop 32-bit integer and store to address |
| ent | entry |
| ret | return (pop pc, sp=bp, pop bp)|
| mst | mark stack (push bp, bp=sp, sp=bp) |
| cup | call user procedure (push pc)|
| csp | call standard (built-in) procedure |
| cmp | compare tow values |
| jmp | unconditional jump |
| jeq | jump if euqual or true |
| jne | jump if not euqual or false|
| stp | stop |

- i32 : 32-bit integer
- f32 : 32-bit single precision floating point

## Macro

| Macro | Description |
| - | - |
| db {addr} {values} | define bytes. |






