# GCC visibility

## Preface

By default, the linker exports all functions (and global variables).

There are 3 methods to make them hidden, using gcc :
* Adding `__attribute__ ((visibility ("hidden")))` before the function declaration
* Adding compilation flag `-fvisibility=hidden`
* Adding [version-script](https://www.gnu.org/software/gnulib/manual/html_node/LD-Version-Scripts.html) to the linker flags. One may use `-Wl,--version-script=` flag to the _compiler flags_.

The visibility attribute in the code may appear in the definition or in the declaration, equivalently.

If there is a mismatch between definition's and declaration's visibility attribute, the compiler will emit a warning :
`warning: ‘int foo()’: visibility attribute ignored because it conflicts with previous declaration [-Wattributes]`
and will ignore the second one.


What happens when they disagree ?

## Checking

The tiny python script creates a cpp file with a single method, and compile it as a shared object.

Then, it uses `nm` to find if the method (foo) was exported (` T `, aberration for text symbol) or internal (` t `) refer [man nm](https://linux.die.net/man/1/nm).

It changes the visibility, using 3 methods mentioned above, and creates a 3x3x3 matrix of results.


## Results :


|       Definition attribute     |  Compiler flags |  Version script | Result |
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

Unfortunately, I couldn't find more compact rules.

## Some tips [source](https://gcc.gnu.org/wiki/Visibility):

* The compiler may do some optimizations, based on the visibility, so telling the compiler is better.
* When exporting C++ symbols, it's much easier to use the code attributes (name mangling, implicit methods).
* In windows, the only way to export symbols is using code attributes (`__declspec(dllexport)` and `__declspec(dllimport)`).
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