# Pyright namespace issue

This is a minimal working example of a pyright namespace issue. It requires [poetry](https://python-poetry.org/) to run the example as shown below.

This example will create a local virtual environment (`.venv`) and install two local namespace packages: `namespace-package1` and `namespace-package2` both located in the `extern` local directory. The only other dependency is `pyright`. You can inspect the `pyproject.toml` file to confirm this.

The issue is that pyright wrongly-in my opinion-shows an error for missing type stubs for the namespace package `namespace`. However, since this is a namespace packge, no files can be added to the `namespace` folders, thus the `namespace` will never have a `py.typed` file present. This seems to be an accidental omission, and should be fixed by not requiring the `py.typed` for namespace packages, or at least require that all packages inside the namespace be typed for the namespace itself to be considered typed. 

To show the issue run

```bash
poetry install
poetry run pyright ./example_script.py
```

in your shell which in my shell outputs

> \<ROOT-DIRECTORY>\pyright-namespace-issue\example_script.py  
> \<ROOT-DIRECTORY>\pyright-namespace-issue\example_script.py:1:6 - error: Stub file not found for "namespace" (reportMissingTypeStubs)  
> 1 error, 0 warnings, 0 informations
