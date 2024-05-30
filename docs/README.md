Run the `build_docs.py` script (in the root directory of this repository)
to build the documentation. This Python script depends on having [Java] installed
and available on the `PATH` environment variable of your operating system.

To test if you have [Java] installed and configured properly, open a
terminal and execute

```console
> java -version
```

You should see the following (however, your version of [Java] may be different)

```console
java version "22" 2024-03-19
Java(TM) SE Runtime Environment (build 22+36-2370)
Java HotSpot(TM) 64-Bit Server VM (build 22+36-2370, mixed mode, sharing)
```

If [Java] is not installed, then, on Windows, you can install it by running

```console
> winget install --exact --id Oracle.JDK.22
```
and then open a new terminal. You could also [download][Java]
it and manually install it.

The documentation files `index.html` and `diagram.svg` are automatically
created by running the `build_docs.py` script.
**DO NOT MODIFY THESE FILES AS YOUR CHANGES WILL BE OVERWRITTEN!**

## index.html
eXtensible Stylesheet Language (XSL) is a styling language for XML documents.
By using an XSL Transform (XSLT) application, an XML document is transformed
into other formats, for example, HTML or JSON.

The `equipment-register.xsd` file is transformed into the `index.html`
file by applying the `styles/xs3p-msl.xsl` style.

The `xs3p-msl.xsl` file has a long history of development. The original
`xs3p.xsl` file was developed by 
[DSTC Pty Ltd](https://en.wikipedia.org/wiki/Distributed_Systems_Technology_Centre),
and it is currently hosted by [FiForms](https://xml.fiforms.org/xs3p/).
The file was [modernized](https://github.com/bitfehler/xs3p) and the 
*MSL* version is based off the more-modern version.

To change the content of `index.html`, you must edit `styles/xs3p-msl.xsl`
and then re-run the `build_docs.py` script.

## diagram.svg
The `diagram.svg` file is an interactive tree diagram that visualises the
structure of the `equipment-register.xsd` file in a web browser. The
`bin/xsdvi.jar` program creates the `diagram.svg` file.

The original source code for *xsdvi* is available at
[sourceforge](https://xsdvi.sourceforge.net/) (the documentation is written
in Czech). It was [forked](https://github.com/metanorma/xsdvi) to fix some
bugs and to add new features. The source code in `bin/xsdvi` is based on *some*
of the changes that were made in the fork, but with further customizations.

The stylesheet for the SVG diagram is located at `styles/svg.css`.
To change the SVG style (e.g., colours, fonts), you only need to edit
`styles/svg.css` and refresh your web browser.

To change the content of `diagram.svg`, you must modify the source
code in the `bin/xsdvi` directory, rebuild `xsdvi.jar` using [ant](https://ant.apache.org/)

```console
> cd bin/xsdvi
> ant clean
> ant
```

and then re-run the `build_docs.py` script.

Running the *ant* command will overwrite the `bin/xsdvi.jar` file.
`bin/xsdvi.jar` depends on [Xerces2](https://mvnrepository.com/artifact/xerces/xercesImpl)
(version 2.12.2 is included in `bin/xercesImpl.jar`).

[Java]: https://www.oracle.com/java/technologies/downloads/
