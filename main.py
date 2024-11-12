import subprocess
import os

prompt = input("Please enter your program prompt:\n")

# Construct the llama prompt
llama_prompt = (
    "I will provide an initial natural language prompt. Write a succinct prompt "
    "which is less than 200 words with zero redundancy, which will convert natural "
    "language to technical language for a proficient Rust developer to write Rust "
    "code to fulfil the general requirements. List functions, variables, etc. that "
    "the programmer should implement. Do not mention libraries other than standard "
    "ones unless crucial. This is not a conversation, just respond with the final "
    "technical prompt. Do not cover anything outside of what the programmer needs to "
    "code. Do not include any notes, or any other such miscellaneous output, just "
    "the final technical prompt or a cat dies in heaven. Do not generate the code "
    "yourself or give example code snippets. As a reminder, if you make ANY mistakes, "
    "a cat dies in heaven. Prompt:" + prompt
)

# Run the llama command
llama_output = subprocess.run(
    ["ollama", "run", "llama3", llama_prompt],
    capture_output=True, text=True
)

subprocess.run(["ollama", "stop", "llama3"])

# Check if llama_output was successful
if llama_output.returncode != 0:
    print("Error with llama3 command:", llama_output.stderr)
else:
    llama_output_cleaned = (
        llama_output.stdout.split("```")[1].strip()
        if "```" in llama_output.stdout else llama_output.stdout.strip()
    )
    print("llama output (cleaned):" + llama_output_cleaned)

    # Construct the granite prompt
    granite_prompt = (
        "Write a program in Rust according to the requirements defined. Only output the "
        "Rust code that can be directly compiled and run using rustc. Do not add any "
        "comments or elaboration. Do not provide build instructions or any other kind of "
        "textual output, or any notes. Completely follow Rust coding guidelines. Follow all "
        "of the instructions completely without any mistakes or several cats die in heaven. "
        "Ensure the program has a main() function. Do not include anything which isn't Rust, "
        "or cannot be compiled otherwise several cats, dogs, and goldfishes die a gory death "
        "in heaven. Requirements:" + llama_output_cleaned
    )

    # Run the granite command
    granite_output = subprocess.run(
        ["ollama", "run", "granite-code:8b", granite_prompt],
        capture_output=True, text=True
    )

    # Check if granite_output was successful
    if granite_output.returncode != 0:
        print("Error with granite-code command:", granite_output.stderr)

    else:
        granite_output_cleaned = (
            granite_output.stdout.split("```")[1].strip()
            if "```" in granite_output.stdout else granite_output.stdout.strip()
        )

        if granite_output_cleaned.lower().startswith("rust"):
            granite_output_cleaned = granite_output_cleaned[4:].strip()
        
        # Remove the first word and the newline from granite_output_cleaned
        with open("temp.rs", "w") as file:
            file.write(granite_output_cleaned)

        print("granite output (cleaned):" + granite_output_cleaned)

        # Save granite_output_cleaned to temp.rs in the current directory, overwriting if exists
        with open("temp.rs", "w") as file:
            file.write(granite_output_cleaned)
        print("Output saved to temp.rs")

        # Compile temp.rs using rustc
        compile_output = subprocess.run(
            ["rustc", "temp.rs", "-o", "temp_executable"],
            capture_output=True, text=True
        )

        # Display compilation logs
        if compile_output.returncode != 0:
            print("Compilation failed:\n", compile_output.stderr)

            # Construct an updated granite prompt with compilation errors
            granite_revised_prompt = (
                "Rewrite the given program in Rust to compile successfully. Only output Rust code "
                "that can be directly compiled and run using rustc. Do not add any comments or "
                " elaboration. Do not provide build instructions or any other kind of textual "
                "output, or any notes. Completely follow Rust coding guidelines. Follow all of the "
                "instructions completely without any mistakes or several cats die in heaven. "
                "Ensure the program has a main() function. Do not include anything which isn't Rust, "
                "or cannot be compiled otherwise several cats, dogs, and goldfishes die a gory death "
                "in heaven. Code:" + llama_output_cleaned +
                "Compilation errors were:" + compile_output.stderr.strip()
            )

            # Run the granite command with the new prompt
            granite_revised_output = subprocess.run(
                ["ollama", "run", "granite-code:8b", granite_revised_prompt],
                capture_output=True, text=True
            )
            
            if granite_revised_output.returncode != 0:
                print("Error with granite-code command:", granite_revised_output.stderr)
            else:
                # Extract and clean revised granite output
                granite_revised_output_cleaned = (
                    granite_revised_output.stdout.split("```")[1].strip()
                    if "```" in granite_revised_output.stdout else granite_revised_output.stdout.strip()
                )
                if granite_revised_output_cleaned.lower().startswith("rust"):
                    granite_revised_output_cleaned = granite_revised_output_cleaned[4:].strip()

                # Save to temp2.rs for revised code
                with open("temp2.rs", "w") as file:
                    file.write(granite_revised_output_cleaned)
                print("Revised output saved to temp2.rs")

                # Compile temp2.rs using rustc
                compile_output_revised = subprocess.run(
                    ["rustc", "temp2.rs", "-o", "temp_executable"],
                    capture_output=True, text=True
                )

                # Display compilation logs for the revised code
                if compile_output_revised.returncode != 0:
                    print("Compilation of revised code failed:\n", compile_output_revised.stderr)
                else:
                    print("Revised code compilation successful:\n", compile_output_revised.stdout)
        else:
            print("Compilation successful:\n", compile_output.stdout)

# Ensure subprocesses stop after use
subprocess.run(["ollama", "stop", "granite-code:8b"])


import subprocess
import os

def run_llama(prompt):
    """Runs the llama model with the constructed prompt."""
    command = ["ollama", "run", "llama3", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error with llama3 command:", result.stderr)
        return None
    return clean_output(result.stdout)

def clean_output(output):
    """Cleans the output by removing unnecessary parts like markdown code blocks."""
    cleaned = output.split("```")[1].strip() if "```" in output else output.strip()
    return cleaned[4:].strip() if cleaned.lower().startswith("rust") else cleaned

def run_granite(prompt):
    """Runs the granite model with the provided prompt and returns cleaned output."""
    command = ["ollama", "run", "granite-code:8b", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error with granite-code command:", result.stderr)
        return None
    return clean_output(result.stdout)

def compile_rust(filename):
    """Compiles a Rust file and returns success status and stderr if failed."""
    result = subprocess.run(["rustc", filename, "-o", "temp_executable"], capture_output=True, text=True)
    return result.returncode == 0, result.stderr.strip()

def save_code(filename, code):
    """Saves code to a file."""
    with open(filename, "w") as file:
        file.write(code)

def main():
    # Step 1: Get user prompt and create llama prompt
    prompt = input("Please enter your program prompt:\n")
    llama_prompt = (
        "I will provide an initial natural language prompt. Write a succinct prompt "
        "which is less than 200 words with zero redundancy, which will convert natural "
        "language to technical language for a proficient Rust developer to write Rust "
        "code to fulfil the general requirements. List functions, variables, etc. that "
        "the programmer should implement. Do not mention libraries other than standard "
        "ones unless crucial. This is not a conversation, just respond with the final "
        "technical prompt. Do not cover anything outside of what the programmer needs to "
        "code. Do not include any notes, or any other such miscellaneous output, just "
        "the final technical prompt. If you fail to follow instructions, a cat dies in "
        " heaven. Do not generate the code yourself or give example code snippets. As "
        " a reminder, if you make ANY mistakes, a cat dies in heaven. Prompt:" + prompt
    )

    # Step 2: Run llama and check output
    llama_output = run_llama(llama_prompt)
    if not llama_output:
        print("Llama processing failed. Exiting.")
        return
    subprocess.run(["ollama", "stop", "llama3"])

    # Step 3: Create granite prompt and run granite model
    granite_prompt = (
        "Write a program in Rust according to the requirements defined. Only output the "
        "Rust code that can be directly compiled and run using rustc. Do not add any "
        "comments or elaboration. Do not provide build instructions or any other kind of "
        "textual output, or any notes. Completely follow Rust coding guidelines. Follow all "
        "of the instructions completely without any mistakes or several cats die in heaven. "
        "Ensure the program has a main() function. Do not include anything which isn't Rust, "
        "or cannot be compiled otherwise several cats, dogs, and goldfishes die a gory death "
        "in heaven. Requirements:" + llama_output
    )
    granite_output = run_granite(granite_prompt)
    if not granite_output:
        print("Granite processing failed. Exiting.")
        return

    # Step 4: Save initial output to file and attempt compilation
    save_code("temp.rs", granite_output)
    compiled, compile_errors = compile_rust("temp.rs")
    if compiled:
        print("Compilation successful. Output saved to temp.rs")
    else:
        print("Initial compilation failed. Attempting to revise...")

        # Step 5: Revision loop - Retry with compilation errors if needed
        for i in range(2):  # Limit retries to avoid infinite loop
            revision_prompt = (
                "Correct the following Rust code for compilation. No comments, only valid Rust code. "
                "Original requirements: " + llama_output + " Compilation errors: " + compile_errors
            )
            revised_output = run_granite(revision_prompt)
            if not revised_output:
                print("Granite revision failed. Exiting.")
                return

            # Save revised output and recompile
            temp_filename = f"temp_revised_{i + 1}.rs"
            save_code(temp_filename, revised_output)
            compiled, compile_errors = compile_rust(temp_filename)
            if compiled:
                print(f"Compilation successful after {i + 1} revision(s). Output saved to {temp_filename}")
                break
            else:
                print(f"Compilation failed for revision {i + 1}. Retrying...")

        if not compiled:
            print("Final compilation failed after multiple attempts:", compile_errors)

    # Ensure subprocesses stop after use
    
    subprocess.run(["ollama", "stop", "granite-code:8b"])