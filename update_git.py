import os
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    print("=== GitHub Auto-Sync Tool by Mahmoud Ali ===")
    
    # Check git status
    code, stdout, stderr = run_cmd("git status -s")
    if code != 0:
        print("Error: Not a git repository or git is not installed.")
        return

    if not stdout:
        print("No changes detected in the repository. Everything is up to date!")
        return

    print("\nModified/New files detected:")
    print(stdout)

    commit_msg = input("\nEnter commit message (press Enter for default 'Update project'): ").strip()
    if not commit_msg:
        commit_msg = "Update project: " + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    confirm = input("\nDo you want to push these changes to GitHub? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled by user.")
        return

    print("\nAdding files...")
    run_cmd("git add .")

    print(f"Committing with message: '{commit_msg}'...")
    code, out, err = run_cmd(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"Commit failed: {err}")
        return

    print("Pushing to GitHub (origin main)...")
    code, out, err = run_cmd("git push origin main")
    if code != 0:
        print(f"Push failed: {err}")
        # Try push without origin main if branch differs
        code, out, err = run_cmd("git push")
        if code != 0:
            print(f"Push failed again: {err}")
            return

    print("\nSuccessfully pushed updates to GitHub! 🚀")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
