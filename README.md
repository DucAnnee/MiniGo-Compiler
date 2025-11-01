# MiniGo Compiler

A compiler for the **MiniGo programming language**, a simplified version of Go defined by the course *Principles of Programming Languages*.  
Implemented in **Python** with **ANTLR** for lexical and syntactic analysis.

## Overview
MiniGo is a lightweight teaching language inspired by Golang defined by professors in Ho Chi Minh University of Technology.  
This compiler performs **lexical analysis**, **parsing**, **semantic checking**, and **code generation**, following a traditional compiler pipeline.

## Project Structure
```
MiniGo-Compiler/
├── src/
│   ├── main.py                 # Entry point for the compiler
│   ├── minigo/
│   │   ├── parser/             # ANTLR grammar and generated lexer/parser
│   │   ├── astgen/             # Abstract Syntax Tree (AST) generation
│   │   ├── checker/            # Semantic analysis and type checking
│   │   ├── codegen/            # Intermediate/target code generation
│   │   └── utils/              # Visitor patterns and common helpers
│   └── test/                   # Unit tests for lexer, parser, checker, and codegen
└── specification/
    └── MiniGo Spec 1.0.2.pdf   # Language specification provided by the professor
```

## Features
- **ANTLR-based Parsing**: Grammar-driven lexer and parser generation.
- **AST Generation**: Construct hierarchical syntax representation for MiniGo programs.
- **Semantic Checking**: Type and scope analysis, static error detection.
- **Code Generation**: Produce intermediate representations or target code.
- **Modular Design**: Organized into reusable compiler phases and test suites.

## Technologies
- **Python 3**
- **ANTLR4**
- **Visitor Pattern**
- **Unit Testing**
