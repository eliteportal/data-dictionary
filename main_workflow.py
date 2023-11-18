"""
Main workflow for this website. Also captured in github workflows.

"""
import os

# Get new data model from repo
os.system("python dev/get_data_model.py")

# update new csvs and and terms
os.system("python term_file_manager.py")

os.system("python term_page_manager.py")

# Test jekyll site
# os.system("bundle exec jekyll serve")

# push changes
