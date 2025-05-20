# C-Minus Compiler (educational)

<p align="center">
  <img src="https://img.shields.io/badge/status-alpha-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/language-Python%203.11-yellow?style=flat-square"/>
</p>

> A didactic, from-scratch compiler for the **C-–** language (subset of C).  
> Phases implemented so far: **Lexer → Parser → Semantic Analyzer**.  
> Codebase driven by university coursework & personal exploration.

---

## ✨ Key features

| Phase | Highlights |
|-------|------------|
| **Lexer** | DFA-based scanner, support for comments `/* … */`, multi-char ops (`<=`, `!=`, `&&`, `||`). |
| **Parser** | Hand-written recursive-descent for the full C-– grammar (functions, arrays, `if/while`, calls). |
| **Semantic Analyzer** | <ul><li>Scope stack & symbol tables (one table per block).</li><li>Two-pass traversal (build ST → type check).</li><li>Detailed error messages with line + column & <code>^</code> caret.</li></ul> |
| **Project structure** | Clean separation by phase & plenty of unit samples under `tasks/`. |

---

## 🗂️ Repository layout
\n├── Analizador Semántico/ # PDF slides & rubric
\n├── c_minus/ # Current C-– compiler implementation
\n│ ├── globalTypes.py
│ ├── lexer.py
│ ├── Parser.py
│ ├── semantica.py
│ └── symtab.py
├── tiny/ # Legacy Tiny compiler (reference baseline)
├── tasks/ # Short programs, test cases & scripts
├── parser_transcript.md # Design notes
└── projects.md # Road-map / To-dos

---
