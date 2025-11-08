# 🧠 LLM2CLIPS - Expert System Generator

**A minimalist conversational interface for generating and executing CLIPS expert systems using LLM**

---

## 📖 Overview

LLM2CLIPS is a single-module Python program that bridges Large Language Models (LLMs) with the CLIPS expert system shell. Users describe problems in natural language, and the system automatically generates, executes, and interprets CLIPS rule-based programs.

### Flow Architecture

```
┌──────┐    ┌─────────┐    ┌──────────┐    ┌───────────┐    ┌─────────┐    ┌──────┐
│ User │───▶│ Problem │───▶│ CodeLlama│───▶│ CLIPS Code│───▶│ Execute │───▶│ User │
└──────┘    │ Describe│    │ Generate │    │  Program  │    │ & Result│    └──────┘
            └─────────┘    └──────────┘    └───────────┘    └─────┬───┘
                                                                    │
                                            ┌───────────────────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │CodeLlama │
                                      │Interpret │
                                      └──────────┘
```

**Cycle**: User → LLM (codellama) → CLIPS Program → Execution → LLM → User

---

## 🎯 Design Philosophy

This program follows strict minimalist principles:

- **Single Module**: All code in one file (`llm2clips.py`)
- **No Over-Engineering**: Direct, simple implementations
- **Clear Documentation**: Every function, class, and important line documented
- **Lightweight**: Minimal dependencies, maximum clarity
- **CLI-First**: Simple command-line chat interface

---

## 🏗️ Architecture & Design

### Component Breakdown

#### 1. **Setup & Validation Layer**
- `check_ollama_running()`: Verify Ollama server accessibility
- `check_model_installed()`: Check if codellama is available
- `download_model()`: Auto-download codellama if missing
- `setup_ollama()`: Orchestrate complete setup process

#### 2. **Code Generation Layer**
- `generate_clips_code()`: Send problem to LLM, receive CLIPS code
- `clean_generated_code()`: Remove markdown artifacts from LLM output
- Uses structured prompts to ensure valid CLIPS syntax

#### 3. **Execution Layer**
- `execute_clips_code()`: Create CLIPS environment, run code, capture output
- Uses `clipspy` bindings to interact with CLIPS engine
- Returns success status and execution results

#### 4. **Interpretation Layer**
- `interpret_results()`: Send execution output to LLM for human-friendly explanation
- Bridges technical CLIPS output with user understanding

#### 5. **Interface Layer**
- `display_welcome()`: Show startup message and instructions
- `display_help()`: Provide examples and usage guidance
- `chat_loop()`: Main interaction loop implementing full cycle

### Data Flow

```python
# 1. User Input
problem = "Check if person is adult (age >= 18)"

# 2. LLM Generates CLIPS Code
clips_code = """
(deftemplate person
  (slot name)
  (slot age))

(defrule check-adult
  (person (name ?n) (age ?a&:(>= ?a 18)))
  =>
  (printout t ?n " is an adult" crlf))

(deffacts initial
  (person (name "John") (age 25)))
"""

# 3. Execute in CLIPS
output = "Rules fired: 1\nFacts:\n  f-1 (person (name John) (age 25))"

# 4. LLM Interprets
interpretation = "John is 25 years old, which meets the adult threshold of 18. 
                 The system correctly identified him as an adult."

# 5. Display to User
```

---

## 📦 Installation

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Ollama** ([Download](https://ollama.ai))
   ```bash
   # Mac
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download/windows
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   ```

### Install Dependencies

```bash
pip install clipspy ollama
```

### Verify Installation

```bash
python llm2clips.py
```

The program will automatically:
- Check if Ollama is running
- Detect if codellama is installed
- Offer to download codellama if missing (~3.8GB)

---

## 🚀 Usage

### Quick Start

```bash
python llm2clips.py
```

### Example Session

```
🧠 LLM2CLIPS - Expert System Generator
======================================================================

Describe your problem and I'll generate a CLIPS expert system!

----------------------------------------------------------------------
You: Check if temperature is hot (>30), warm (15-30), or cold (<15). 
     Current temperature is 35 degrees.

🤖 Processing your request...

  [1/4] Generating CLIPS code...
  ✓ Code generated
  [2/4] Executing CLIPS system...
  ✓ Execution complete
  [3/4] Interpreting results...
  ✓ Results interpreted

======================================================================
🎯 RESULT
======================================================================

The temperature of 35 degrees is classified as HOT since it exceeds 
the 30-degree threshold. The CLIPS system correctly evaluated the 
condition and applied the appropriate rule.

Show technical details? (y/n): n

----------------------------------------------------------------------
You: quit

👋 Goodbye!
```

### Commands

- **Describe problem**: Type naturally, include data and rules
- **`help`**: Show examples and usage tips
- **`quit`** / **`exit`**: Close the program
- **Ctrl+C**: Emergency exit

---

## 💡 Example Problems

### Example 1: Simple Classification

```
Problem: Classify students by grade
Data: Student Alice has grade 85
Rules: A=90-100, B=80-89, C=70-79, D=60-69, F=<60
```

### Example 2: Decision System

```
Problem: Approve credit card application
Data: Applicant has income=4000, credit_score=720, debt_ratio=25%
Rules: Approve if income>3000 AND credit_score>700 AND debt_ratio<30%
```

### Example 3: Medical Triage

```
Problem: Classify patient urgency
Data: Patient has fever=true, chest_pain=true, breathing_difficulty=true
Rules: Urgent if (fever AND chest_pain) OR breathing_difficulty
```

### Example 4: Recommendation System

```
Problem: Recommend programming language
Data: Project type=web, experience=beginner, team_size=small
Rules: web+beginner=JavaScript, data+any=Python, systems+expert=Rust
```

---

## 🔧 Technical Details

### CLIPS Code Structure

Generated CLIPS programs typically include:

1. **Templates** (deftemplate): Define data structures
   ```clips
   (deftemplate person
     (slot name (type STRING))
     (slot age (type INTEGER)))
   ```

2. **Facts** (deffacts): Initial data
   ```clips
   (deffacts people
     (person (name "John") (age 25))
     (person (name "Jane") (age 17)))
   ```

3. **Rules** (defrule): Inference logic
   ```clips
   (defrule check-adult
     (person (name ?n) (age ?a&:(>= ?a 18)))
     =>
     (printout t ?n " is adult" crlf))
   ```

4. **Actions**: Output results
   ```clips
   (printout t "message" crlf)
   ```

### LLM Prompting Strategy

#### Generation Prompt
- Instructs LLM to produce **only** valid CLIPS code
- No markdown, no explanations
- Includes structure requirements (templates, facts, rules)
- Specifies output format

#### Interpretation Prompt
- Provides context (original problem + execution output)
- Asks for concise, user-friendly explanation
- 2-3 sentences maximum

### Error Handling

The program handles:
- **Ollama not running**: Clear instructions to start service
- **Model missing**: Automatic download offer
- **Code generation failure**: Retry prompt
- **Execution errors**: Display error + generated code for debugging
- **Keyboard interrupts**: Graceful shutdown

---

## 📚 CLIPS Background

### What is CLIPS?

**CLIPS** (C Language Integrated Production System) is a forward-chaining rule-based programming language designed for building expert systems.

### Key Concepts

1. **Expert Systems**: Programs that mimic human expert decision-making
2. **Forward Chaining**: Start with facts, apply rules, derive conclusions
3. **Pattern Matching**: Automatically match facts against rule conditions
4. **Inference Engine**: Determines which rules to fire and when

### CLIPS Syntax Basics

```clips
; Define data structure
(deftemplate car
  (slot make)
  (slot year)
  (slot price))

; Define initial facts
(deffacts cars
  (car (make "Toyota") (year 2020) (price 25000))
  (car (make "Tesla") (year 2023) (price 45000)))

; Define rule
(defrule expensive-car
  (car (make ?m) (price ?p&:(> ?p 40000)))
  =>
  (printout t ?m " is expensive" crlf))

; Execution:
; (reset)  ; Load facts
; (run)    ; Fire rules
```

### Use Cases

- Decision support systems
- Diagnostic systems
- Configuration systems
- Monitoring and control
- Planning and scheduling
- Classification systems

---

## 🔍 Code Structure

### Function Overview

| Function | Purpose | Lines |
|----------|---------|-------|
| `check_ollama_running()` | Verify Ollama server | ~10 |
| `check_model_installed()` | Check if model exists | ~15 |
| `download_model()` | Download codellama | ~15 |
| `setup_ollama()` | Complete setup workflow | ~30 |
| `generate_clips_code()` | LLM → CLIPS code | ~25 |
| `clean_generated_code()` | Remove artifacts | ~20 |
| `execute_clips_code()` | Run CLIPS program | ~30 |
| `interpret_results()` | LLM → explanation | ~20 |
| `display_welcome()` | Show startup UI | ~15 |
| `display_help()` | Show examples | ~20 |
| `chat_loop()` | Main interaction loop | ~60 |
| `main()` | Entry point | ~20 |

**Total**: ~280 lines (including documentation)

### Dependencies

```python
import sys           # System operations (exit)
import subprocess    # Process management (reserved for future use)
import clips         # CLIPS engine bindings (clipspy)
import ollama        # Ollama LLM client
```

---

## 🐛 Troubleshooting

### "Ollama is not running"

**Solution**:
```bash
# Start Ollama server
ollama serve
```

### "clipspy not installed"

**Solution**:
```bash
pip install clipspy
```

### "ollama not installed"

**Solution**:
```bash
pip install ollama
```

### Generated code fails to execute

**Possible causes**:
- LLM generated invalid syntax
- Problem description too vague

**Solution**:
- Use "Show technical details" to see generated code
- Rephrase problem more clearly
- Include specific data and rules

### Model download fails

**Possible causes**:
- Network issues
- Insufficient disk space (~3.8GB needed)

**Solution**:
- Check internet connection
- Free up disk space
- Manual download: `ollama pull codellama`

---

## 🎓 Learning Resources

### CLIPS Documentation
- [CLIPS Official Website](https://clipsrules.net/)
- [CLIPS Tutorial 1](https://web.archive.org/web/20100510113711/http://wwwdi.ujaen.es/~dofer/ico/material/CLIPS-Tutorial-1.html)
- [CLIPS Tutorial 2](https://web.archive.org/web/20100510120647/http://wwwdi.ujaen.es/~dofer/ico/material/CLIPS-Tutorial-2.html)
- [CLIPS Wikipedia](https://es.wikipedia.org/wiki/CLIPS)

### Ollama & CodeLlama
- [Ollama Library](https://ollama.com/library)
- [CodeLlama Model](https://ollama.com/library/codellama)
- [clipspy Documentation](https://clipspy.readthedocs.io/en/latest/)

### Expert Systems
- Rule-based reasoning
- Forward vs backward chaining
- Knowledge representation
- Inference engines

---

## 📝 Code Quality

This codebase follows:

- ✅ **Single Responsibility**: Each function does one thing
- ✅ **Clear Naming**: Descriptive function and variable names
- ✅ **Complete Documentation**: Docstrings for all functions
- ✅ **Inline Comments**: Explain non-obvious logic
- ✅ **Error Handling**: Try-except blocks with meaningful messages
- ✅ **Type Hints**: Function signatures include types
- ✅ **Modular Design**: Separated concerns (setup, generation, execution, interpretation)
- ✅ **No Magic Numbers**: Constants defined at top
- ✅ **Consistent Style**: PEP 8 compliance

---

## 🚦 Limitations

1. **LLM Dependency**: Code quality depends on codellama's output
2. **Single Problem**: Each interaction is independent (no context memory)
3. **CLIPS Scope**: Limited to forward-chaining rule systems
4. **Local Only**: Requires local Ollama installation
5. **No Persistence**: Generated code not saved automatically

---

## 🔮 Future Enhancements

Possible improvements (not implemented to maintain minimalism):

- Save generated CLIPS files
- Multi-turn conversations with context
- Support for other models
- Web interface
- CLIPS code validation before execution
- Syntax highlighting
- History of past problems
- Export results to file

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

## 👤 Author

**Marco**  
Created with Cursor IDE

---

## 🧪 Experiments & Known Issues

### Known Issue: Syntax Errors in Generated Code

**Problem**: Sometimes the LLM generates CLIPS code with syntax errors, particularly with unclosed parentheses.

**Example Error**:
```
[STRNGFUN2] Function 'build' encountered extraneous input.
```

**Example Case**:
```
Input: "Check if person can vote. Person is 25 years old and is a citizen. 
        Can vote if age 18 or above AND is citizen."

Generated Code (with error):
(deffacts init-data
  (person (age 25) (citizen TRUE))    ; Missing closing parenthesis
(defrule can-vote
  (printout t "Person is eligible to vote." crlf)
```

**Root Cause**: The `deffacts` block is missing its closing parenthesis. Should be:
```clips
(deffacts init-data
  (person (age 25) (citizen TRUE)))  ; Properly closed
```

**Solutions**:

1. **Immediate Fix**: When you see this error, select "y" to view technical details and manually inspect the generated code for syntax issues.

2. **Retry**: Simply describe the problem again, sometimes the LLM generates correct code on second attempt.

3. **Simplify**: Use simpler problem descriptions:
   - ✅ Good: "Check voting eligibility. Person age 25. Eligible if age >= 18."
   - ❌ Complex: "Check if person can vote. Person is 25 years old and is a citizen. Can vote if age 18 or above AND is citizen."

4. **Model Temperature**: The current temperature is 0.3 (low). You could try adjusting it in the code for more consistent syntax.

### Statistics from Testing

- **Success Rate**: ~70-80% on first attempt
- **Common Issues**: Unclosed parentheses, missing rule conditions
- **Best Results**: Simple classification problems with 2-3 rules
- **Most Errors**: Complex multi-condition rules with AND/OR logic

### Workaround Tips

1. Start with simple problems (age classification, temperature check)
2. Add complexity gradually once you see it working
3. If error occurs, simplify your description
4. Use "Show technical details" to learn CLIPS syntax patterns
5. After seeing patterns, you can mentally validate expected structure

---

## 🙏 Acknowledgments

- **CLIPS**: Gary Riley and the CLIPS development team
- **Ollama**: Ollama team for local LLM infrastructure
- **clipspy**: noxdafox for Python bindings
- **CodeLlama**: Meta AI for the code generation model

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [CLIPS Documentation](https://clipsrules.net/)
3. Verify Ollama is running: `ollama list`

---

**Ready to build expert systems? Run `python llm2clips.py` and start describing your problems!** 🚀

