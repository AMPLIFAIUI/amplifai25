import subprocess
import os
import sys

def main():
    # Get the absolute path of the directory where this script is located
    # This will be d:\OpenAgent_Amplifai when the script is run from there
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to uvicorn.exe within the python_embedded directory
    # This should resolve to d:\OpenAgent_Amplifai\python_embedded\Scripts\uvicorn.exe
    uvicorn_executable = os.path.join(root_dir, "python_embedded", "Scripts", "uvicorn.exe")
    
    # Check if uvicorn.exe exists
    if not os.path.isfile(uvicorn_executable):
        print(f"Error: uvicorn.exe not found at {uvicorn_executable}")
        print("Please ensure the embedded Python environment is set up correctly, for example, by running setup_embedded_python.ps1.")
        sys.exit(1)
        
    # Define the command to run.
    # Uvicorn needs to be run with root_dir as the current working directory
    # so that it can find the 'Amplifai.webui_sandbox:app' module.
    command = [
        uvicorn_executable,
        "Amplifai.webui_sandbox:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    print(f"Attempting to launch Amplifai Web UI from: {root_dir}")
    print(f"Using uvicorn: {uvicorn_executable}")
    print(f"Executing command: {' '.join(command)}")
    
    process = None  # Initialize process to None
    try:
        # Run the command.
        # Set the current working directory (cwd) to root_dir.
        # This is crucial for Python's import system to find the 'Amplifai' package.
        process = subprocess.Popen(command, cwd=root_dir)
        
        # Wait for the uvicorn process to complete.
        # This means this script will keep running as long as uvicorn is running.
        process.wait()
        
    except FileNotFoundError:
        print(f"Error: Failed to start uvicorn. The executable was not found at '{uvicorn_executable}'.")
        print("Please verify the path and ensure the embedded Python environment is correctly set up.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to execute '{uvicorn_executable}'.")
        print("Please check the file permissions.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nUvicorn server process interrupted by user (Ctrl+C).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        if process and process.poll() is None: # If process is still running (e.g. KeyboardInterrupt didn't stop it)
            print("Terminating uvicorn process...")
            process.terminate()
            try:
                process.wait(timeout=5) # Wait a bit for graceful termination
            except subprocess.TimeoutExpired:
                print("Uvicorn process did not terminate gracefully, killing.")
                process.kill()
            print("Uvicorn process stopped.")

if __name__ == "__main__":
    main()
