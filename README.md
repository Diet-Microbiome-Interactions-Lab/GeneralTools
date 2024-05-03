# General Tools (for Bioinformatics)
## A DMIL-Supported Resource out of Purdue University

Here we present simple tools for common bioinformatic use-cases, as well as other convenient functionality for your everyday command-line hacker. Our tools are split up into a few parts (or cabinets), mostly for our own sanity, but hopefully so it makes accessing the tool you need more intuitive. Within each specific tool cabinet (to milk the toolshed analogy), we follow some simple rules to make extending the package functionality relatively simple.

The philosophy is to
- easy CLI
- lab level config
- logging and tractability
  - checksums? - 


### who is this for and why
this is focused on being a CLI for people who are not good at CLIs. it is not intended as a python api

## top 3 example usages

```
mycli hello hello
```


## First, let's dive into each section of our tools.

### **alignmentTools**
Tools that relate to alignment, which is the processing of sticking one sequence onto another in places that look like it should fit - or something like that.

### **annotationTools**
Tools that relate to annotation, which is the process of using a database, or some other external reference, to add extra metadata, or layers, to your data. For example, a gene can be annotated with a known function from a previously-established database

### **bashTools**
Small tools to use in your bash shell to help you noodle around and move things. These primarily relate to filesystem manipulations and viewing.

### **fastaTools**
Fasta/FastQ files are some of the most common in bioinformatics, so they have their own cabinet of tools! Feel like a magician and perform many complex permutations on your files.

example usage

### **miscTools**
Tools that do not yet have a cabinet, but if enough tools come about in a particular domain, let's go ahead and give them their own. Some of these tools are 1-off and only used in niche applications, but thats cool.

### **pipelineTools**
Tools that involve 3 or more steps, which require a little more logging and control in order to ensure we don't bust computer screen with error messages.

## Second, let's talk about our File Validation

Often times we get a file in our hands of a known type, but...how confident are we that the file exactly adheres to the type specification? For example, we might encounter a fasta file that has a *V* in the sequence, which may not be a big deal, but shoving the file into a pipeline may error out because a particular program determines the fasta file to be invalid. Or perhaps there's a pesky extra space in a file and another program was tricked into thinking the remaining file was empty and the program terminates early; we probably never would know that our program did not finish correctly! (This has happened to me before). 

TODO: show these problems in practice - known tools or workflows that failed. any estimates on how often do these failures come up?

So here's our solution - which is meant to be an open-source, collaborative effort - let's create validation classes that scrub our files to be squeeky clean (and add additional logging) before performing any work on them.
There's a module called FileTypes, which contains Python classes that validate as many bioinformatics file types as possible. Each described file has the following capabilities:
- Validate the particular file either with soft (check extension) or hard (check contents) mode
- Define the **Preferred Filename**, which removes ambiguity in file naming and extension.
  - For example, .fna, .fasta, .fa, .fasta.gz, etc., will be coerced to *'.fasta.gz'*. This allows us to control not only the validation but also the naming of the file, which is helpful when we release automated analyses connected via **SnakeMake** (shhhh, it's not released yet...**)
- Rewriting functionality, which allows you write a new validated file or transform to another file type
- A ton of properties that describe the file. For example, in a BAM file, how many reads are aligned? Or in a gff3 file, where are the XX1 genes located?
  - This is the meat and potatoes (as we say in the midwest US) of the general toolset, allowing us immediate access to any sort of defining property of our file with a couple keystrokes
- Subsetting functionality, or rewriting a new file based on a filtering condition. For example, you may want to write the 10 largest sequences, or sequences > 2000 basepairs to a new file in a fasta.


## Installation
TODO

```
pip install packagename
```

## Contributor Guide

All skill levels are welcome: maybe this will be your first time writing python or first time programming

0.x - experimental. we are seeing if anyone likes this and going from there, so no formal guide just yet

example - https://github.com/amplication/amplication?tab=readme-ov-file#contributing

## Dependencies


## Related Projects / Prior Art
see also / similar projects / inspiration - section

## release strategy
schedule, maintenance, set expectations
using semantic versioning
test process - we have unit tests

## roadmap
- main features you expect/hope to implement

## License
This project is licensed under the terms of the MIT license.
