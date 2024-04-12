"""
Main workflow for this website. Also captured in github workflows.

"""

import subprocess

# Get new data model from repo
# os.system("python dev/get_data_model.py")

# update new csvs and and terms
file_management = subprocess.Popen("python data_manager.py")

page_management = subprocess.Popen("python page_manager.py")

# Test jekyll site
# subprocess.Popen("bundle exec jekyll serve")

# push changes
