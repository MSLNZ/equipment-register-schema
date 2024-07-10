The XML Schema Definition for an Equipment Register does not validate _everything_.
For example, it validates that the `sha256` checksum value of a file has the correct
checksum length and that the checksum only contains the allowed alphanumeric characters,
but, the Schema does not validate that the checksum value is correct for the file.
For these additional validation steps, another tool must be used.

The files in this `tools` directory may be used to provide additional validation
mechanisms for various programming languages.

## Python

The `validate.py` module may be used to provide additional validation to the
_content_ of an XML element.

There are four functions available:
* _load_schema_: Load the XSD file. By default, it is assumed that the Schema file
  (equipment-register.xsd) is located in the current working directory.
* _next_id_: Recursively search all equipment-register files to automatically determine
  the numeric value for the next equipment ID.
* _recursive_validate_: Recursively validate all equipment-register files, starting 
  from a specified directory.
* _validate_: Validate a single equipment-register (XML) file.

The `validate.py` script also provides a command-line interface. Running the script
without specifying any arguments will show the help for the command-line tool

```
py validate.py
```

As a practical example, suppose you wanted to recursively validate all equipment
registers in a directory and print some messages about what is happening

```
py validate.py path\to\registers --verbose  
```
