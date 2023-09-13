import os
import subprocess

# Step 1: Create a virtual environment
print("Step 1: Creating a virtual environment...")
# Step 2: Activate the virtual environment
print("Step 2: Activating the virtual environment...")
if os.name == "posix":  # For Unix-like systems (Linux, macOS)
    subprocess.run(["source", "new_venv/bin/activate"])
# Step 4: Initialize the database and create a superuser
print("Step 4: Initializing the database and creating a superuser...")
subprocess.run(["python3", "manage.py", "migrate"])

# Step 5: Run the Django development server
print("Step 5: Starting the Django development server...")
subprocess.run(["python3", "manage.py", "runserver"])


# Done!
print("Your Django project is now set up and running.")
print("You can access it by opening your web browser and navigating to http://localhost:8000")
