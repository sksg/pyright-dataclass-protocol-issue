# Pyright Dataclass Protocol issue

This is a minimal working example of a pyright dataclass protocol issue. You can
use [poetry](https://python-poetry.org/) to run the example.

This example will create a local virtual environment (`.venv`) and install two
local namespace packages: `namespace-package1` and `namespace-package2` both
located in the `extern` local directory. The only other dependency is `pyright`.
You can inspect the `pyproject.toml` file to confirm this.

The issue is that pyright wrongly-in my opinion-shows an error for missing
implementations of the dataclass protocol. However, as can be seen by running
the example in python, this code works. I believe the inheritance of a protocol
should be, in effect, the same as inheriting a normal base class. In any case,
this is how it behaves.

Interestingly, when we create the type dynamically (using `type()`) the typing
works. But in fact the `__init__` is not correctly used and it fails at runtime.
This can be recreated using a dataclass decorator, and still seems rather exotic
behaviour.

To show the issue run

```bash
poetry install
poetry run pyright ./example_script.py
```

in your shell which in my shell outputs

> c:\Users\sogr\src\pyright-dataclass-protocol-issue\example_script.py
>   c:\Users\sogr\src\pyright-dataclass-protocol-issue\example_script.py:50:16 - error: Cannot instantiate abstract class "dataclass_one_prime"
>     "dataclass_one_protocol.a" is not implemented
>     "dataclass_one_protocol.b" is not implemented (reportAbstractUsage)
>   c:\Users\sogr\src\pyright-dataclass-protocol-issue\example_script.py:124:27 - error: Cannot instantiate abstract class "combined_dataclass_prime"
>     "dataclass_two_protocol.x" is not implemented
>     "dataclass_two_protocol.y" is not implemented
>     and 2 more... (reportAbstractUsage)
> 2 errors, 0 warnings, 0 informations

You can, however, run the example script and see that indeed they do work as
expected at runtime

```bash
poetry run python ./example_script.py
```

and the output is

> Method called with a=1, b=example one
> Method called with a=1, b=example one
> Expected TypeError occurred: dataclass_one_dynamic_prime.__init__() takes exactly one argument (the instance to initialize)
> Method called with a=2, b=example two
> Another method called with x=2.0, y=test
> Method called with a=2, b=example two
> Another method called with x=2.0, y=test

Notice that the dynamic creation of the dataclasses do not use the base class
`__init__` functions correctly. This might be an effect of the protocols
explicitly disallowing direct instantiation.
