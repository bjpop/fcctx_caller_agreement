[![travis](https://travis-ci.org/bjpop/fcctx_caller_agreement.svg?branch=master)](https://travis-ci.org/bjpop/fcctx_caller_agreement)

# Overview 

Convert DNA structural variants in VCF files into BED format.

# Licence

This program is released as open source software under the terms of [BSD-2-Clause License](https://raw.githubusercontent.com/bjpop/fcctx_caller_agreement/master/LICENSE).

# Installing

Svdistil can be installed using `pip` in a variety of ways (`%` indicates the command line prompt):

1. Inside a virtual environment:
```
% python3 -m venv fcctx_caller_agreement_dev
% source fcctx_caller_agreement_dev/bin/activate
% pip install -U /path/to/fcctx_caller_agreement
```
2. Into the global package database for all users:
```
% pip install -U /path/to/fcctx_caller_agreement
```
3. Into the user package database (for the current user only):
```
% pip install -U --user /path/to/fcctx_caller_agreement
```


# General behaviour


# Usage 


```
% fcctx_caller_agreement -h
```


## Logging

If the ``--log FILE`` command line argument is specified, fcctx_caller_agreement will output a log file containing information about program progress. The log file includes the command line used to execute the program, and a note indicating which files have been processes so far. Events in the log file are annotated with their date and time of occurrence. 

```
% fcctx_caller_agreement --log 
# normal fcctx_caller_agreement output appears here
# contents of log file displayed below
```
```
% cat bt.log
```

# Exit status values

Svdistil returns the following exit status values:

* 0: The program completed successfully.
* 1: File I/O error. This can occur if at least one of the input FASTA files cannot be opened for reading. This can occur because the file does not exist at the specified path, or fcctx_caller_agreement does not have permission to read from the file. 
* 2: A command line error occurred. This can happen if the user specifies an incorrect command line argument. In this circumstance fcctx_caller_agreement will also print a usage message to the standard error device (stderr).
* 3: Input FASTA file is invalid. This can occur if fcctx_caller_agreement can read an input file but the file format is invalid. 


# Error handling

# Testing

## Unit tests

```
% cd fcctx_caller_agreement/python/fcctx_caller_agreement
% python -m unittest -v fcctx_caller_agreement_test
```

# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[fcctx_caller_agreement issue tracker](https://github.com/bjpop/fcctx_caller_agreement/issues)
