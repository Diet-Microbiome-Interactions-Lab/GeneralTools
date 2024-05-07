# General Tools (for Bioinformatics)

### A Diet-Microbiome Interactions Lab-Supported Resource out of Purdue University

Here we present simple tools for common bioinformatic use-cases, as well as other convenient functionality for your everyday command-line hacker. The main functionality takes in a file and a specified type, and will validate the file plus perform any simple stats, permutations, or filters. We were tired of getting errors when shoving data that wasn't first validated into pipelines, as well as performing the same bash and python hacks to look a little deeper at our large files. Further, we wanted a way to extend file validation and hacks to custom file types in our lab. Lastly, we wanted a more robust way to configure settings and record our behavior so we could be more reproducible without expending any extra effort.

## Setup & Installation

### i) Setup (Start Here!)

This is a Python package, requiring the version of Python to be 3.6 or later (a higher number than 3.6). From your Terminal (mac) or terminal-emulator in Windows (putty, powershell, etc.), which we will refer to as your _terminal_, check if you have Python3 installed.  
`python --version`  
or  
`python3 --version`  
One of those commands should show "Python 3.6" or newer if you have python3 installed correctly. For the remaining steps, use the command (`python or python3`) that worked.

### ii) Installation

Installation should be pretty quick using the package manager _pip_. We recommend first creating and entering a virtual environment before installing our package, but this is not necessary. Perform the following command to install the package:  
`pip install danegeneraltools`  
Once this is installed, you should be able to type:  
`dane --test`  
and it should produce a nice success message for you in the terminal.

## How to use this library

### i) Getting help

One of the first things you may notice about this library is the interesting way in which you invoke it. Invocations always start with an executable from our library, such as:  
`fileflux`  
and they must always have a `type: EXAMPLE` key-value pair, as each executable is specific to the type of file it receives.

If you want to know what sort of arguments you're able to run for a particular executable, you just need to pass the word _help_ as the first positional argument (the first word _after_ fileflux), along with specifying the _type_:  
`fileflux help type: fasta`  
The `type: fasta` follows the pattern where you have a key followed by a colon (key:), then provide the name of a _value_ separated by a space, e.g., `key: value`.

Above, this will first provide a status report that consists of 4 lines, which look something like this:  
\# Success  
\## Status  
200: okay  
\## Response

Line one will tell you if the command succeeded or failed, lines 2 and 3 will give you a more specific status code, and line 4 will provide the response, which is often the part of the command output you'll be interested in.

After, it will show a list of every possible command, along with the docstring content (or help message) for each said command. These list of commands will start with 0 and go up through the last command (sorted alphabetically). Notice if you change the **type** the possible commands will change.

### ii) Command LIne Extension (CLIX)

To run an executable, you must first type the executable's name (e.g., `fileflux`) and immediately after provide positional arguments that align with the action you wish to perform. For exampe, from the fileflux help page, you see:  
`$ fileflux seq length type: fasta file: example.fasta`

Let's break down this command.  
`fileflux` is the executable and is always required first.  
`seq length` is a series of 2 positional arguments that conform to an executable found in the help message. These positional arguments are what tell the executable what to do, and may be anywhere from 1 to 5 space-separated arguments.  
`type: TYPE` (in this case, `type: fasta`) is **always required**. This tells the executable what type of file we are dealing with. In later releases of this app, we will try to smart-parse files so this is not necessarily needed.  
`file: FILE` (in this case, `file: example.fasta`) is also **always required** for any action to occur. This is the file you want to perform some action on.

Great, but what about if I want to provide extra parameters to the command? You can specify as many parameters as you want using the following syntax:  
`key: value`  
which will specify the parameter you want and the value it will have. For example:  
`length: 100 width: 200`  
will tell our system that we have the parameter length=100 and width=200.

### iii) Configuration Settings

One of our least favorite things to do is specify the same parameters over and over again, or forget which parameters we used because we did not document concisely enough. By default, we scan the home (~/.config/fileflux/) and /etc/fileflux/ folders for \*.yaml files. Attributes put into these files will automatically be added to the configuration, which is available for all your programs to use.  
For example, say you have a file `~/.config/fileflux/config.yaml` with the following parameters

```yml
name: "dane"
length: 10
```

If you were to invoke the following command:  
`fileflux filter sequences type: fasta file: example.fasta`  
and the action _filter sequences_ took in a _length_ parameter, the action can grab that length parameter from the configuration file by default. Now let's say you have that configuration file but it does not have the _length_ parameter specified. No worries, because each action will have default parameters baked into it. If you wanted to change the parameter on the fly _without_ having to edit your config.yaml file, you can easily do that specifying the parameter on the command line:

`fileflux filter sequences type: fasta file: example.fasta length: 20`

Note that the position of the parameters, the type, and the file do not matter. The above command is the same as the below command:

`fileflux filter sequences length: 20 type: fasta file: example.fasta`

The only positional arguments that matter are the `fileflux` as the first and the next sequence of arguments specifying the action to invoke (`filter sequences`)

For specifying parameters, there's a hierarchy that our program uses in order to resolve duplicate parameters. We first check the home folder (~/.config/fileflux/config.yaml), then the /etc/fileflux, and then the command line. Any parameters specified in the home configuration file that overlap with the /etc/fileflux will be over written by the /etc/fileflux, and any parameters specified on the command line will take ultimate priority in redundant paramers.

## First, let's dive into each section of our tools.

### **alignmentTools**

Tools that relate to alignment, which is the processing of sticking one sequence onto another in places that look like it should fit - or something like that.

### **annotationTools**

Tools that relate to annotation, which is the process of using a database, or some other external reference, to add extra metadata, or layers, to your data. For example, a gene can be annotated with a known function from a previously-established database

### **bashTools**

Small tools to use in your bash shell to help you noodle around and move things. These primarily relate to filesystem manipulations and viewing.

### **fastaTools**

Fasta/FastQ files are some of the most common in bioinformatics, so they have their own cabinet of tools! Feel like a magician and perform many complex permutations on your files.

### **miscTools**

Tools that do not yet have a cabinet, but if enough tools come about in a particular domain, let's go ahead and give them their own. Some of these tools are 1-off and only used in niche applications, but thats cool.

### **pipelineTools**

Tools that involve 3 or more steps, which require a little more logging and control in order to ensure we don't bust computer screen with error messages.

## Some philosophical rants

### Let's talk about file validation

Often times we get a file in our hands of a known type, but...how confident are we that the file exactly adheres to the type specification? For example, we might encounter a fasta file that has a _V_ in the sequence, which may not be a big deal, but shoving the file into a pipeline may error out because a particular program determines the fasta file to be invalid. Or perhaps there's a pesky extra space in a file and another program was tricked into thinking the remaining file was empty and the program terminates early; we probably never would know that our program did not finish correctly! (This has happened to me before). So here's our solution - which is meant to be an open-source, collaborative effort - let's create validation classes that scrub our files squeeky clean (and add additional logging) before performing any work on them.  
There's a folder called FileTypes, which contains Python classes that validate as many bioinformatics file types as possible. Each described file has the following capabilities:

- Validate the particular file either with soft (check extension) or hard (check contents) mode
- Define the **Preferred Filename**, which removes ambiguity in file naming and extension.
  - For example, .fna, .fasta, .fa, .fasta.gz, etc., will be coerced to _'.fasta.gz'_. This allows us to control not only the validation but also the naming of the file, which is helpful when we release automated analyses connected via **SnakeMake** (shhhh, it's not released yet...\*\*)
- Rewriting functionality, which allows you write a new validated file or transform to another file type
- A ton of properties that describe the file. For example, in a BAM file, how many reads are aligned? Or in a gff3 file, where are the XX1 genes located?
  - This is the meat and potatoes (as we say in the midwest US) of the general toolset, allowing us immediate access to any sort of defining property of our file with a couple keystrokes
- Subsetting functionality, or rewriting a new file based on a filtering condition. For example, you may want to write the 10 largest sequences, or sequences > 2000 basepairs to a new file in a fasta.

## Contributor Guide

Dane Deemer: Senior Computational Biologist (Purdue University)
Nathan Denny: Lead Research Analyst (Purdue University)
Stephen Lindemann: Associate Professor (Purdue University)
Maverick Cook: Senior Database Engineer (Purdue University)
