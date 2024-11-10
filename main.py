import subprocess
import os

prompt = input("Please enter your program prompt:")

# Construct the llama prompt
llama_prompt = (
    "I will provide an initial natural language prompt. Write a succinct prompt "
    "which is less than 200 words with zero redundancy, which will convert natural "
    "language to technical language for a proficient Rust developer to write Rust "
    "code to fulfil the general requirements. List functions, variables, etc. that "
    "the programmer will use as a hint. Do not mention libraries other than standard "
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
        "Rust code that can be directly compiled and run using rustc. Do not add any extra "
        "comments or elaboration. Do not provide build instructions or any other kind of "
        "textual output, or any notes. Completely follow Rust coding guidelines. Follow all "
        "of the instructions completely without any mistakes or several cats die in heaven. "
        "If the requirements don't define a main function, create one which runs with sample "
        "data. Do not include anything which cannot be compiled or several cats, dogs, and "
        "goldfishes die a gory death in heaven. Requirements:" + llama_output_cleaned
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
        
        # Remove the first word and the newline from granite_output_cleaned
        granite_output_cleaned = " ".join(granite_output_cleaned.split()[1:])

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
        else:
            print("Compilation successful:\n", compile_output.stdout)
            
            # Run the compiled Rust program
            run_output = subprocess.run(
                ["./temp_executable"],
                capture_output=True, text=True
            )
            print("Program output:\n", run_output.stdout)

# Ensure subprocesses stop after use
subprocess.run(["ollama", "stop", "llama3"])
subprocess.run(["ollama", "stop", "granite-code:8b"])
