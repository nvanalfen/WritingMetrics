import numpy as np
import pandas as pd

# These columns are essential to running
# This dict will allow flexibility in the exact labels used
# The key is what the code will know them as, the value is what they may be called in the csv file
essential_columns = {"Date":"Date",
                     "Goal":"Goal"}

# The columns in the csv file that are projects
# i.e. the titles of the books you're writing
# This should more or less be automatically generated from the csv file
project_columns = []

# For other subgoals (e.g. even if there's a 1500 words/day goal, you may have a 500 words/day goal for a specific project, taking part of that larger goal)
# For this dict, the key is the name of the project column in the csv, the value is the name of the subgoal column
# e.g. {"Book 1":"Book 1 Goal"}
subgoal_columns = {}

# The date format used in the csv file
date_format = "%m/%d/%y"

def add_project(project_name, project_columns):
    project_columns.append(project_name)