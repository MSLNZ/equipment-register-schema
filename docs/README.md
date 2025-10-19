Run the `build_docs.py` script (in the root directory of this repository) to build the documentation locally during development. The online docs are managed by GitHub Actions (see the files in the `.github/workflows` directory) and are stored in the `gh-pages` branch.

The `build_docs.py` Python script depends on having [Java] installed and available on the `PATH` environment variable of your operating system.

To test if you have [Java] installed and configured properly, open a terminal and execute

```shell
java -version
```

You should see the following (however, your version of [Java] may be different)

```console
java version "25" 2025-09-16 LTS
Java(TM) SE Runtime Environment (build 25+37-LTS-3491)
Java HotSpot(TM) 64-Bit Server VM (build 25+37-LTS-3491, mixed mode, sharing)
```

If [Java] is not installed, then, on Windows, you can install it by running

```shell
winget install Oracle.JDK.25
```

and then open a new terminal. You could also [download][Java] it to manually install it.

The built documentation files are saved to the `docs/build/develop` directory by running the `build_docs.py` script. Open the `index.html` file in a web browser to view the docs.

## index.html
eXtensible Stylesheet Language (XSL) is a styling language for XML documents. By using an XSL Transform (XSLT) application, an XML document is transformed into other formats, for example, HTML or JSON.

The `equipment-register.xsd` file is transformed into the `index.html` file by applying the `xs3p-msl.xsl` style.

The `xs3p-msl.xsl` file has a long history of development. The original `xs3p.xsl` file was developed by [DSTC Pty Ltd](https://en.wikipedia.org/wiki/Distributed_Systems_Technology_Centre), and it was hosted by [FiForms](https://xml.fiforms.org/xs3p/) (link may now be broken). The file was [modernized](https://github.com/bitfehler/xs3p) and the *MSL* version is based off the more-modern version.

To change the structure and content of `index.html` you must edit `xs3p-msl.xsl` and to change the stylesheet you must edit `css/index.css`, then re-run the `build_docs.py` script to see the changes (after a page refresh).

## diagram.svg
The `diagram.svg` file is an interactive tree diagram that visualises the structure of the `equipment-register.xsd` file in a web browser. The `bin/xsdvi.jar` program creates the `diagram.svg` file.

The original source code for *xsdvi* is available at [sourceforge](https://xsdvi.sourceforge.net/) (the documentation is written in Czech). It was [forked](https://github.com/metanorma/xsdvi) to fix some bugs and to add new features. The source code in `bin/xsdvi` is based on *some* of the changes that were made in the fork, but with further customizations.

The stylesheet for the SVG diagram is located at `css/diagram.css`. To change the SVG style (e.g., colours, fonts), you must edit `css/diagram.css`.

To change the content of `diagram.svg`, you must modify the source code in the `bin/xsdvi` directory, rebuild `xsdvi.jar` using [ant](https://ant.apache.org/)

```shell
cd bin/xsdvi
ant clean
ant
```

and then re-run the `build_docs.py` script.

Running the *ant* command will overwrite the `bin/xsdvi.jar` file. `bin/xsdvi.jar` depends on [Xerces2](https://mvnrepository.com/artifact/xerces/xercesImpl) (version 2.12.2 is included in `bin/xercesImpl.jar`).

[Java]: https://www.oracle.com/java/technologies/downloads/
