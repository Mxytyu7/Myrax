import subprocess

def start_core():
    try:
        subprocess.run(["python", "core.py"])
    except FileNotFoundError:
        print("Error: core.py not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    start_core()

if __name__ == "__main__":
    main()
