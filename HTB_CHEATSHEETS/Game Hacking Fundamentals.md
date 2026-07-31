**Data Movement Instructions**

| Instruction | Description                            | Example      |
| ----------- | -------------------------------------- | ------------ |
| MOV         | Move data from one location to another | MOV eax, ebx |
| PUSH        | Push a value onto the stack            | PUSH eax     |
| POP         | Pop a value from the stack             | POP eax      |

**Arithmetic Instructions**

| Instruction | Description               | Example      |
| ----------- | ------------------------- | ------------ |
| ADD         | Add two operands          | ADD eax, ecx |
| SUB         | Subtract two operands     | SUB edx, eax |
| INC         | Increment an operand by 1 | INC eax      |
| DEC         | Decrement an operand by 1 | DEC ebx      |

**Control Flow Instructions**

| Instruction | Description                      | Example            |
| ----------- | -------------------------------- | ------------------ |
| CALL        | Call a function                  | CALL _functionName |
| RET         | Return from a function           | RET                |
| JMP         | Unconditional jump to a location | JMP _label         |
| JE          | Jump if equal                    | JE _label          |
| JNE         | Jump if not equal                | JNE _label         |
| JG          | Jump if greater                  | JG _label          |
| JGE         | Jump if greater or equal         | JGE _label         |
| JL          | Jump if less                     | JL _label          |
| JLE         | Jump if less or equal            | JLE _label         |

**Comparison and Conditional Set Instructions**

| Instruction | Description             | Example      |
| ----------- | ----------------------- | ------------ |
| CMP         | Compare two operands    | CMP eax, ebx |

**Miscellaneous Instruction**

| Instruction | Description  | Example |
| ----------- | ------------ | ------- |
| NOP         | No operation | NOP     |