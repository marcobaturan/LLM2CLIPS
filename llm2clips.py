#!/usr/bin/env python3
"""
LLM2CLIPS - Expert System Generator via Chat Interface

This program creates a conversational interface where users describe problems,
an LLM (codellama) generates CLIPS code, executes it, and returns results.

Flow: User → LLM → CLIPS Code → Execution → LLM → User

Dependencies:
    - clipspy: Python bindings for CLIPS expert system
    - ollama: Python client for Ollama LLM server

Author: Marco
License: GNU General Public License v3.0
"""

import sys

import subprocess
from typing import Optional, Tuple

try:
    import clips
except ImportError:
    print("Error: clipspy not installed. Install with: pip install clipspy")
    sys.exit(1)

try:
    import ollama
except ImportError:
    print("Error: ollama not installed. Install with: pip install ollama")
    sys.exit(1)


# ============================================================================
# Configuration Constants
# ============================================================================

MODEL_NAME = "codellama"  # Ollama model for code generation
CLIPS_GENERATION_PROMPT = """You are a CLIPS expert system programmer.
Generate ONLY valid CLIPS code (no explanations, no markdown, no comments outside CLIPS syntax).

User problem:
{problem}

Generate a complete CLIPS program with:
1. Templates (deftemplate) for data structures
2. Facts (deffacts) with initial data
3. Rules (defrule) for inference
4. Output using (printout t "message" crlf)

Return ONLY the CLIPS code, nothing else."""

RESULT_INTERPRETATION_PROMPT = """You are an expert system analyst.
A user described this problem:
{problem}

The generated CLIPS code executed with this output:
{output}

Explain the results to the user in a clear, friendly way.
Keep it concise (2-3 sentences)."""


# ============================================================================
# Core Functions
# ============================================================================

def check_ollama_running() -> bool:
    """
    Check if Ollama server is running.
    
    Returns:
        bool: True if Ollama is accessible, False otherwise
    """
    try:
        # Try to list models - if this works, Ollama is running
        ollama.list()
        return True
    except Exception:
        return False


def check_model_installed(model: str) -> bool:
    """
    Check if a specific model is installed in Ollama.
    
    Args:
        model (str): Name of the model to check
        
    Returns:
        bool: True if model is installed, False otherwise
    """
    try:
        # Get list of installed models
        models_response = ollama.list()
        models = models_response.get('models', [])
        
        # Check if our model is in the list
        for m in models:
            if model in m['name']:
                return True
        return False
    except Exception:
        return False


def download_model(model: str) -> bool:
    """
    Download a model using Ollama.
    
    Args:
        model (str): Name of the model to download
        
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        print(f"\n📥 Downloading {model} model...")
        print("This may take several minutes depending on your connection.")
        
        # Use ollama.pull() to download the model
        ollama.pull(model)
        
        print(f"✅ {model} downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


def setup_ollama() -> bool:
    """
    Ensure Ollama is running and codellama model is available.
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    # Check if Ollama is running
    if not check_ollama_running():
        print("❌ Ollama is not running.")
        print("Please start Ollama:")
        print("  - Windows: Should start automatically")
        print("  - Mac/Linux: Run 'ollama serve' in a terminal")
        return False
    
    print("✅ Ollama is running")
    
    # Check if codellama is installed
    if not check_model_installed(MODEL_NAME):
        print(f"⚠️  {MODEL_NAME} model not found")
        
        # Ask user if they want to download it
        response = input(f"Download {MODEL_NAME}? (y/n): ").strip().lower()
        if response == 'y':
            return download_model(MODEL_NAME)
        else:
            print("Cannot proceed without the model.")
            return False
    
    print(f"✅ {MODEL_NAME} model is available")
    return True


def generate_clips_code(problem: str) -> Optional[str]:
    """
    Use LLM to generate CLIPS code from a problem description.
    
    Args:
        problem (str): User's problem description
        
    Returns:
        Optional[str]: Generated CLIPS code, or None if generation failed
    """
    try:
        # Format the prompt with the user's problem
        prompt = CLIPS_GENERATION_PROMPT.format(problem=problem)
        
        # Call the LLM
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract the generated code
        clips_code = response['message']['content']
        
        # Clean the code (remove markdown artifacts if present)
        clips_code = clean_generated_code(clips_code)
        
        return clips_code
    
    except Exception as e:
        print(f"❌ Error generating CLIPS code: {e}")
        return None


def clean_generated_code(code: str) -> str:
    """
    Clean generated code by removing markdown and non-CLIPS content.
    
    Args:
        code (str): Raw generated code
        
    Returns:
        str: Cleaned CLIPS code
    """
    lines = code.split('\n')
    cleaned = []
    in_code_block = False
    
    for line in lines:
        # Skip markdown code block markers
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        # Keep lines that start with '(' (CLIPS code) or ';' (CLIPS comments)
        stripped = line.strip()
        if stripped.startswith('(') or stripped.startswith(';') or stripped == '':
            cleaned.append(line)
    
    return '\n'.join(cleaned).strip()


def execute_clips_code(clips_code: str) -> Tuple[bool, str]:
    """
    Execute CLIPS code and capture output.
    
    Args:
        clips_code (str): CLIPS code to execute
        
    Returns:
        Tuple[bool, str]: (success, output) where success is True if execution
                          succeeded, and output is the captured result
    """
    try:
        # Create a new CLIPS environment
        env = clips.Environment()
        
        # Build (load) the CLIPS code
        env.build(clips_code)
        
        # Reset the environment (initialize facts)
        env.reset()
        
        # Run the inference engine
        rules_fired = env.run()
        
        # Collect output: get all facts
        facts = [str(fact) for fact in env.facts()]
        
        # Format output
        if facts:
            output = f"Rules fired: {rules_fired}\n\nFacts:\n"
            output += '\n'.join(f"  {fact}" for fact in facts)
        else:
            output = f"Rules fired: {rules_fired}\nNo facts generated."
        
        return True, output
    
    except Exception as e:
        return False, f"Execution error: {str(e)}"


def interpret_results(problem: str, output: str) -> str:
    """
    Use LLM to interpret CLIPS execution results for the user.
    
    Args:
        problem (str): Original problem description
        output (str): CLIPS execution output
        
    Returns:
        str: Human-friendly interpretation of results
    """
    try:
        # Format the interpretation prompt
        prompt = RESULT_INTERPRETATION_PROMPT.format(
            problem=problem,
            output=output
        )
        
        # Call the LLM
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response['message']['content']
    
    except Exception as e:
        return f"Could not interpret results: {e}"


def display_welcome():
    """Display welcome message and instructions."""
    print("\n" + "="*70)
    print("           🧠 LLM2CLIPS - Expert System Generator")
    print("="*70)
    print("\nDescribe your problem and I'll generate a CLIPS expert system!")
    print("\nExamples:")
    print("  - 'Classify if a person is adult based on age >= 18'")
    print("  - 'Recommend coffee type: morning=espresso, afternoon=latte'")
    print("  - 'Diagnose if student needs help: grade<6 or attendance<70%'")
    print("\nCommands:")
    print("  'quit' or 'exit' - Exit the program")
    print("  'help' - Show examples")
    print("="*70)


def display_help():
    """Display help and examples."""
    print("\n" + "="*70)
    print("📚 HOW TO USE")
    print("="*70)
    print("\n1. Describe your problem clearly")
    print("2. Include the data/facts to evaluate")
    print("3. Specify the rules or logic")
    print("\n💡 EXAMPLE 1:")
    print("Problem: Check if a temperature is hot, warm, or cold")
    print("Data: Temperature is 35 degrees")
    print("Rules: >30=hot, 15-30=warm, <15=cold")
    print("\n💡 EXAMPLE 2:")
    print("Problem: Decide if someone can get a loan")
    print("Data: Person has income=3000, credit=good, debt=20%")
    print("Rules: Approve if income>2500 AND credit=good AND debt<30%")
    print("="*70)


def chat_loop():
    """
    Main chat loop for user interaction.
    
    Implements the full cycle:
    User → LLM → CLIPS → Execution → LLM → User
    """
    while True:
        # Get user input
        print("\n" + "-"*70)
        user_input = input("You: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Check for help command
        if user_input.lower() == 'help':
            display_help()
            continue
        
        # Ignore empty input
        if not user_input:
            continue
        
        print("\n🤖 Processing your request...\n")
        
        # Step 1: Generate CLIPS code using LLM
        print("  [1/4] Generating CLIPS code...")
        clips_code = generate_clips_code(user_input)
        
        if not clips_code:
            print("❌ Failed to generate CLIPS code. Please try again.")
            continue
        
        print("  ✓ Code generated")
        
        # Step 2: Execute CLIPS code
        print("  [2/4] Executing CLIPS system...")
        success, execution_output = execute_clips_code(clips_code)
        
        if not success:
            print(f"❌ Execution failed: {execution_output}")
            print("\n📄 Generated code (for debugging):")
            print(clips_code)
            continue
        
        print("  ✓ Execution complete")
        
        # Step 3: Interpret results using LLM
        print("  [3/4] Interpreting results...")
        interpretation = interpret_results(user_input, execution_output)
        print("  ✓ Results interpreted")
        
        # Step 4: Display results to user
        print("\n" + "="*70)
        print("🎯 RESULT")
        print("="*70)
        print(f"\n{interpretation}\n")
        
        # Optionally show technical details
        show_details = input("Show technical details? (y/n): ").strip().lower()
        if show_details == 'y':
            print("\n📄 Generated CLIPS Code:")
            print("-"*70)
            print(clips_code)
            print("\n📊 Execution Output:")
            print("-"*70)
            print(execution_output)


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """
    Main function - entry point of the program.
    
    Workflow:
    1. Display welcome message
    2. Setup and verify Ollama + codellama
    3. Enter chat loop for user interaction
    """
    # Display welcome
    display_welcome()
    
    # Setup Ollama and model
    print("\n🔧 Initializing system...")
    if not setup_ollama():
        print("\n❌ Setup failed. Please fix the issues and try again.")
        sys.exit(1)
    
    print("\n✅ System ready!")
    
    # Start chat loop
    try:
        chat_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()

