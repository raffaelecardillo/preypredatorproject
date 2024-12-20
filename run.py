import subprocess
import os

# Function to compile a C file
def compile_c_file(c_file):
    # Constructing the compile command
    output_file = os.path.splitext(c_file)[0] 
    command = ["gcc", c_file, "-o", output_file, "-lm"] 

    try:
        # Execute the compile command
        subprocess.run(command, check=True)
        print(f"Compilation succeeded: {c_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation of {c_file}: {e}")
        return None

# Function to run a compiled C program with arguments
def run_c_program_with_args(executable, t0, amplitude):
    try:
        # Run the compiled C program with arguments
        subprocess.run([f"./{executable}", str(t0), str(amplitude)], check=True)
        print(f"Execution succeeded for program: {executable} with t0={t0}, amplitude={amplitude}")
    except subprocess.CalledProcessError as e:
        print(f"Error during execution of {executable}: {e}")

# Function to run a Python script
def run_python_script(script):
    try:
        # Run the Python script
        subprocess.run(["python", script], check=True)
        print(f"Execution succeeded for script: {script}")
    except subprocess.CalledProcessError as e:
        print(f"Error during execution of {script}: {e}")

# List of Python files to execute first
python_files_first = ["codes/interpolation.py", "codes/define_parameters.py"]

# List of C files to compile and execute
c_files = ["codes/equations_solver.c"]

# List of Python files to execute at the end
python_files_last = ["codes/plot.py"]

# Values for t0 and amplitude to run the C program multiple times
t0_values = [1845, 1883, 1877]
amplitude_values = [0,-15000,-10000] 

# Run the first two Python files
for python_file in python_files_first:
    run_python_script(python_file)

# Compile and run the C program
for c_file in c_files:
    executable = compile_c_file(c_file)
    if executable:
        # Run the C program for each combination of t0 and amplitude
        for t0, amplitude in zip(t0_values, amplitude_values):
            run_c_program_with_args(executable, t0, amplitude)

# Run the last Python file
for python_file in python_files_last:
    run_python_script(python_file)
