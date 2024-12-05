XML Schema Definition (XSD) for an Equipment Register.

For background information about XSD, please see the following overview
provided by the [World Wide Web Consortium](https://www.w3.org/)

* [XML Schema Part 0: Primer](https://www.w3.org/TR/xmlschema-0/)
* [XML Schema Part 1: Structures](https://www.w3.org/TR/xmlschema-1/)
* [XML Schema Part 2: Datatypes](https://www.w3.org/TR/xmlschema-2/)

and the [XML Schema Tutorial](https://www.w3schools.com/xml/schema_intro.asp)
provided by [w3schools](https://www.w3schools.com/).

The documentation for the Equipment-Register schema is available
[here](https://mslnz.github.io/equipment-register-schema/).

## Contributing Guide
[Python](https://www.python.org/) is required to run the tests and to build the documentation.
[Java](https://www.java.com/) is also required to build the documentation.
[Git](https://git-scm.com/) is required to interact with the repository.

### Prerequisites
If you know how to install Java, Git, Python and Python packages (`pytest`,  `lxml` and `GTC`
are required) you can skip this section entirely (or only install what you do not have).

The remainder of the _Contributing Guide_ assumes that you have executed every
command and did not deviate.

Running the following commands will:
1. Install Git
2. Install Java
3. Install Python
4. Install the Python dependencies (If you are familiar with
[virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments),
you should install the packages into one &ndash; otherwise ignore this _virtual environment_ stuff.)

You could also manually install each program (links above) rather than running
the following `winget` commands.

Open a terminal (i.e., PowerShell or Command Prompt &ndash; _you may need to open
an elevated terminal if you are using an ITS-managed computer_) and run each command sequentially
to install Git, Java and Python

```console
winget install Git.Git
```
```console
winget install Oracle.JDK.23
```
```console
winget install Python.Python.3.13
```

You must now restart (close then re-open) your terminal so that the executable
for these installed programs becomes available to use.

Next, install the Python dependencies _(perhaps you first need to activate your [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)?)_
```console
pip install pytest lxml GTC
```

Finally, clone the repository
```console
git clone https://github.com/MSLNZ/equipment-register-schema.git
```
and change directory, `cd`, into the root directory of the repository
```console
cd equipment-register-schema
```

### Testing
To run the tests, execute the following command from the root directory
of the repository

```console
pytest
```

### Documentation
To build the documentation, execute the following command from the root directory
of the repository

```console
python build_docs.py
```

See [docs/README](https://github.com/MSLNZ/equipment-register-schema/tree/main/docs#readme)
for information about the build process.
