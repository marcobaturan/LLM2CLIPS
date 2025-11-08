# ⚡ Quick Start - LLM2CLIPS

Get started in 2 minutes!

---

## 🚀 Installation (1 minute)

### Step 1: Install Dependencies

```bash
pip install clipspy ollama
```

### Step 2: Install Ollama

**Already have Ollama?** Skip to Step 3.

- **Mac**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`
- **Windows**: [Download installer](https://ollama.ai/download/windows)

### Step 3: Start Ollama

```bash
ollama serve
```

Keep this terminal open!

---

## ▶️ Run (30 seconds)

Open a new terminal:

```bash
python llm2clips.py
```

First run will ask to download `codellama` (~3.8GB). Accept with `y`.

---

## 💬 Your First Expert System (30 seconds)

When prompted, type:

```
Check if a person can vote. John is 25 years old. 
Voting age is 18 or above.
```

Press Enter and watch the magic! ✨

The system will:
1. Generate CLIPS code
2. Execute it
3. Explain results in plain English

---

## 📚 Try More Examples

### Example 1: Temperature Check

```
Classify temperature as hot, warm, or cold.
Temperature is 35 degrees.
Hot is above 30, warm is 15-30, cold is below 15.
```

### Example 2: Grade Assignment

```
Assign letter grade to student.
Student scored 87 points.
A is 90-100, B is 80-89, C is 70-79, D is 60-69, F is below 60.
```

### Example 3: Loan Decision

```
Decide if loan should be approved.
Applicant has income $4000, credit score 720, debt ratio 25%.
Approve if income > $3000 AND credit > 700 AND debt < 30%.
```

---

## 🎯 Commands

- **Type your problem**: Natural language description
- **`help`**: Show examples
- **`quit`** or **`exit`**: Close program

---

## 🐛 Problems?

### "Ollama is not running"
```bash
ollama serve
```

### "clipspy not installed"
```bash
pip install clipspy
```

### Need more examples?
```bash
# In the program
help
```

Or check `EXAMPLES.md` for 20+ ready-to-use problems!

---

## 📖 Learn More

- **Full documentation**: Read `README.md`
- **20+ examples**: Check `EXAMPLES.md`
- **CLIPS info**: Visit [clipsrules.net](https://clipsrules.net/)

---

**That's it! You're ready to build expert systems!** 🧠

```bash
python llm2clips.py
```

