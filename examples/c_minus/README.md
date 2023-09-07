# C-- language

## Semantic Analysis

## Runtime Environment

### Memory
- Code Area

- Global/Static Area

- Stack
  
  - free space

- Heap

### Procedure Activation Record
- Arguments

- Bookkeeping information, including return address

- Local data

- Local temporaries


## P-code
| P-code | Description |
|-|-|
| ldc_i32 n| load constant n and push onth the stack|
| lod_i32 a| load value of variable a and push onto the stack|
| add_i32 | pops two 32-bit integers from the stack, add them, and push the result |
| sub_i32 | 32-bit integer subtraction|
| mul_i32 | 32-bit integer multiplication |
| div_i32 | 32-bit integer division |
| sto_i32 | store top to address |
| equ_i32 | test for equaility |
| grt_i32 | pop and compare top two values, push boolean result (greater than) |
| les_i32 | pop and compare top two values, push boolean result (less than) |
| fjp | false jump |
| ujp | unconditional jump |
| stp | stop |





