# GCC visibility

## Methods

By default, the linker exports all functions (and variables).

There are 3 methods to make file hidden, using gcc :
* Adding `__attribute__ ((visibility ("hidden")))` before the declaration
* Adding compilation flag `-fvisibility=hidden`
* Adding [version-script](https://www.gnu.org/software/gnulib/manual/html_node/LD-Version-Scripts.html) to the linker. On may use `-Wl,--version-script=` flag to the compiler.


What happens when they disagree ?

## Results :


|       Definition      |  compiler flags |  version script | Result |
|:----------:|:-------------:|:------:|:------:|
| hidden |  * | * | t  |
| default |  * | - | T(Exported) |
| default |  - | global | T(Exported) |
| default |  - | local | t  |
| - |  default | - | T(Exported)  |
| - |  hidden | * | t  |
| - |  - | - | T(Exported)  |
| - |  default | global | T(Exported)  |
| - |  * | local | t |



## Raw results :
```

{('attr def', 'no script', '-f def'): 'T',
 ('attr def', 'no script', '-f hidd'): 'T',
 ('attr def', 'no script', 'no -f'): 'T',
 ('attr def', 'script global', '-f def'): 'T',
 ('attr def', 'script global', '-f hidd'): 'T',
 ('attr def', 'script global', 'no -f'): 'T',
 ('attr def', 'script local', '-f def'): 't',
 ('attr def', 'script local', '-f hidd'): 't',
 ('attr def', 'script local', 'no -f'): 't',
 ('attr hid', 'no script', '-f def'): 't',
 ('attr hid', 'no script', '-f hidd'): 't',
 ('attr hid', 'no script', 'no -f'): 't',
 ('attr hid', 'script global', '-f def'): 't',
 ('attr hid', 'script global', '-f hidd'): 't',
 ('attr hid', 'script global', 'no -f'): 't',
 ('attr hid', 'script local', '-f def'): 't',
 ('attr hid', 'script local', '-f hidd'): 't',
 ('attr hid', 'script local', 'no -f'): 't',
 ('no attr', 'no script', '-f def'): 'T',
 ('no attr', 'no script', '-f hidd'): 't',
 ('no attr', 'no script', 'no -f'): 'T',
 ('no attr', 'script global', '-f def'): 'T',
 ('no attr', 'script global', '-f hidd'): 't',
 ('no attr', 'script global', 'no -f'): 'T',
 ('no attr', 'script local', '-f def'): 't',
 ('no attr', 'script local', '-f hidd'): 't',
 ('no attr', 'script local', 'no -f'): 't'}
 ```