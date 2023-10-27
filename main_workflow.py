"""
Main workflow for this website. Also captured in github workflows. 

"""
import os

# Get new data model from repo
os.system(
    "python ~/Documents/Projects/ELITE/ELITE_data_dictionary/dev/get_data_model.py"
)

# update new csvs and and terms
os.system(
    "python /Users/nlee/Documents/Projects/ELITE/ELITE_data_dictionary/term_file_manager.py"
)

os.system(
    "python /Users/nlee/Documents/Projects/ELITE/ELITE_data_dictionary/term_page_manager.py"
)

# Test jekyll site
# os.system("bundle exec jekyll serve")

# push changes
