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
| ldc n| load constant n and push onth the stack|
| lod a| load value of variable a and push onto the stack|
| adi | pops two integers from the stack, add them, and push the result |
| sbi | integer subtraction|
| mpi | integer multiplication |
| sto | store top to address |
| equ | test for equaility |
| grt | pop and compare top two values, push boolean result (greater than) |
| fjp | false jump |
| ujp | unconditional jump |
| stp | stop |





