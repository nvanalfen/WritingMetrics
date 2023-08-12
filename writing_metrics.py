import pandas as pd
import numpy as np
import seaborn as sns
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict

# Set working directory to file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

word_count_file = "test.csv"

# These columns are essential to running
# This dict will allow flexibility in the exact labels used
# The key is what the code will know them as, the value is what they may be called in the csv file
essential_columns = {"Date":"Date",
                     "Goal":"Goal"}

# The columns in the csv file that are projects
# i.e. the titles of the books you're writing
# This should more or less be automatically generated from the csv file
project_columns = ["Test Book 1", "Test Book 2", "Test Book 3"]

# For other subgoals (e.g. even if there's a 1500 words/day goal, you may have a 500 words/day goal for a specific project, taking part of that larger goal)
# For this dict, the key is the name of the project column in the csv, the value is the name of the subgoal column
# e.g. {"Book 1":"Book 1 Goal"}
subgoal_columns = {"Test Book 1":"Test Book 1 Goal"}

# The date format used in the csv file
date_format = "%m/%d/%y"

#####################################################################################################################################################
##### SUPPORT FUNCTIONS #############################################################################################################################
#####################################################################################################################################################

def project_goal_pairs(project_columns, essential_columns, subgoal_columns, total_only=False):
    if total_only:
        return ["Total"], [essential_columns["Goal"]]
    
    projects = [ proj for proj in project_columns if proj in subgoal_columns.keys() ]
    goals = [ subgoal_columns[key] for key in projects ]
    projects.append("Total")
    goals.append(essential_columns["Goal"])

    return projects, goals

def read_word_count_file(word_count_file):
    df = None
    if word_count_file[-4:] == ".csv":
        df = pd.read_csv(word_count_file, index_col=0)
    elif word_count_file[-5:] == ".xlsx":
        df = pd.read_excel(word_count_file, sheet_name="Sheet1", index_col=0)
    
    return df

def get_weekday(date, date_format):
    days = [datetime.strptime(day, date_format) for day in date]
    weekdays = np.array( [ day.weekday() for day in days ] )
    return weekdays

def weekday_to_string(days, lowercase=False):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if lowercase:
        weekdays = [ day.lower() for day in weekdays ]
    return np.array([ weekdays[day] for day in days ])

def weekday_to_int(days):
    weekdays = {"monday":0, "tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
    return np.array([ weekdays[ day.lower() ] for day in days ])

#####################################################################################################################################################
##### WORDS WRITTEN FUNCTIONS #######################################################################################################################
#####################################################################################################################################################

# Get words written by subtracting previous day's word count from current day's word count
# Do this for each project (column) and Total
def words_written(df, project_columns, essential_columns, subgoal_columns):
    diff = df[ project_columns ].diff()
    _, goals = project_goal_pairs(project_columns, essential_columns, subgoal_columns)
    diff[ goals ] = df[ goals ]
    diff.loc[ diff.index[0] ] = 0
    diff["Total"] = diff[project_columns].sum(axis=1)

    return diff.astype(int)

# Get the words written beyond the set goal
def net_words_written(df, project_columns, essential_columns, subgoal_columns, total_only=False):
    diff = words_written(df, project_columns, essential_columns, subgoal_columns)
    projects, goals = project_goal_pairs(project_columns, essential_columns, subgoal_columns, total_only)
    net = diff[projects] - diff[goals].values

    return net

# Get cumulative words written by summing words written for each day
# Do this for each project and Total
def cumulative_words_written(df, project_columns, essential_columns, subgoal_columns):
    written = words_written(df, project_columns, essential_columns, subgoal_columns)
    cumulative = written.cumsum()

    return cumulative

# Get net cumulative words written by subtracting goal from cumulative words written
def net_cumulative_words_written(df, project_columns, essential_columns, subgoal_columns, total_only=False):
    cumulative = cumulative_words_written(df, project_columns, essential_columns, subgoal_columns)
    projects, goals = project_goal_pairs(project_columns, essential_columns, subgoal_columns, total_only)
    net = cumulative[projects] - cumulative[goals].values

    return net

# Get the number of words written on each weekday
def weekday_words_written(df, project_columns):
    projects = [ proj for proj in project_columns if proj in df.columns ]
    value = pd.DataFrame(df[ projects ])
    if "Total" in df.columns:
        value["Total"] = df["Total"]
    weekdays = get_weekday(value.index)
    weekdays = weekday_to_string(weekdays)
    value["Weekday"] = weekdays

    value = value.groupby("Weekday").sum()

    return value

#####################################################################################################################################################
##### METRICS #######################################################################################################################################
#####################################################################################################################################################

def select_weekday(df, weekday, date_format):
    weekdays = get_weekday(df.index, date_format)
    if isinstance(weekday, str):
        weekday = weekday_to_int([weekday])[0]
    return df[ weekdays == weekday ]

def all_non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, date_format, columns=None):
    standard_metrics = OrderedDict()
    net_metrics = OrderedDict()
    standard_weekday_metrics = {}
    net_weekday_metrics = {}
    
    # Standard words written
    standard_metrics = non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, net=False, columns=columns)

    # Net words written
    net_metrics = non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, net=True, columns=columns)

    for i in range(7):
        standard_weekday_metrics[weekday_to_string([i])[0]] = non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, net=False, columns=columns, weekday=i)
        net_weekday_metrics[weekday_to_string([i])[0]] = non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, net=True, columns=columns, weekday=i)

    return standard_metrics, net_metrics, standard_weekday_metrics, net_weekday_metrics

def non_cumulative_metrics(df, project_columns, essential_columns, subgoal_columns, net=False, columns=None, total_only=False, weekday=None):
    if columns is None and net:
        projects, goals = project_goal_pairs(project_columns, essential_columns, subgoal_columns)
        columns = [ proj for proj in projects if proj in df.columns ] + ["Total"]
    elif columns is None:
        columns = project_columns + ["Total"]
    
    if not net:
        values = words_written(df, project_columns, essential_columns, subgoal_columns)
    else:
        values = net_words_written(df, project_columns, essential_columns, subgoal_columns, total_only=total_only)
    
    # If we just want to look at the values for a particular weekday, do it now (after the words/day have been calculated)
    if not weekday is None:
        values = select_weekday(values, weekday, date_format)
        df = select_weekday(df, weekday, date_format)
        if len(values) == 0:
            return None

    values = values[columns]
        
    metrics = OrderedDict()

    metrics["Mean Words/Day"] = values.mean(axis=0)
    metrics["Median Words/Day"] = values.median(axis=0)
    metrics["Standard Deviation Words/Day"] = values.std(axis=0)
    metrics["Highest Word Count"] = values.max(axis=0)
    metrics["Lowest Word Count"] = values.min(axis=0)
    metrics["Lowest Word Count (With Some Writing)"] = values[values != 0].min(axis=0)
    metrics["Skipped Days"] = (values == 0).sum(axis=0)
    if net:
        # For net metrics, the next two must be measured slightly differently
        goal_df = pd.DataFrame(df[goals])
        some_progress = values.mask(values == -goal_df.values, -np.inf)
        metrics["Lowest Word Count (With Some Writing)"] = some_progress[some_progress != -np.inf].min(axis=0)
        metrics["Skipped Days"] = (values > goal_df.values).sum(axis=0)
        
        # The following are only useful in net
        metrics["Negative Days"] = (values < 0).sum(axis=0)
        metrics["Positive Days"] = (values > 0).sum(axis=0)

    return metrics

#####################################################################################################################################################
##### PLOTTING FUNCTIONS ############################################################################################################################
#####################################################################################################################################################

# TODO: Plot goals and actuals differently
#   - Goals corresponding to specific projects should be the same color but a different style
#   - Give the option to ommit the goals from plotting

# Plots Wanted:
#   - Bar graph of words written on each weekday
#   - Line graph of words written (regular and net)
#   - Line graph of cumulative words written (regular cumulative and net cumulative)
# Tweaks Wanted:
#   - Limit range
#   - Select which series (projects) to plot

# Plot a bar graph of the words written on each weekday
# Do this for each project and Total
def plot_weekday_words_written(values):
    values.plot(kind="bar")
    plt.xlabel("Weekday")
    plt.ylabel("Words Written")
    plt.show()

# Plot a line graph of the words written
# This works for absolute, net, cumulative, and net cumulative
def plot_progress(values, columns=None, omit_goals=False, project_columns=None, subgoal_columns=None, essential_columns=None):
    if ( omit_goals ) and ( columns is None ) and ( not subgoal_columns is None ) and ( not essential_columns is None ):
        goal_labels = [ v for k, v in subgoal_columns.items() ]
        columns = [ col for col in values.columns if not col in goal_labels and not col == essential_columns["Goal"] ]
    values.plot(kind="line", y=columns)
    plt.hlines(0, -1, len(values.index)+1, linestyles=":", color="black")
    plt.xlim([0, len(values.index)])
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Words Written")
    plt.show()

def histogram_words_written(df, project_columns, bins=10, columns=None):
    if columns is None:
        columns = project_columns + ["Total"]
        columns = [ col for col in columns if col in df.columns ]
    #df.plot(kind="hist", bins=bins, y=columns, alpha=0.5)
    print(df[columns].melt())
    sns.histplot(data=df[columns].melt(), multiple="dodge", x="value", shrink=0.75, bins=bins, hue="variable")
    plt.xlabel("Words Written")
    plt.ylabel("Frequency")
    plt.show()

#####################################################################################################################################################
##### MAIN ##########################################################################################################################################
#####################################################################################################################################################

# TODO: Add metrics and plots
#   - Histogram of words written (allow variable bins sizes/numbers)
#   - Cumulative metrics
#   - For cumulative metrics, fit an equation?

df = read_word_count_file(word_count_file)
standard = words_written(df, project_columns, essential_columns, subgoal_columns)
net_words = net_words_written(df, project_columns, essential_columns, subgoal_columns)

#print(weekday_words_written( net_words_written(df) ))
#plot_weekday_words_written( weekday_words_written( words_written(df) ) )

print(">>>>> Standard")
print(words_written(df, project_columns, essential_columns, subgoal_columns)[:5] )
print(">>>>> Net")
print(net_words_written(df, project_columns, essential_columns, subgoal_columns)[:5] )
#print(">>>>> Cumulative")
#print(cumulative_words_written(df, project_columns, essential_columns, subgoal_columns)[:5] )
#print(">>>>> Net Cumulative")
#print(net_cumulative_words_written(df, project_columns, essential_columns, subgoal_columns)[:5] )

#histogram_words_written(net_words, project_columns, bins=10)

print(">>>>> Metrics")
standard_metrics, net_metrics, standard_week_metrics, net_week_metrics = all_non_cumulative_metrics(df[1:25], project_columns, essential_columns, subgoal_columns, date_format, columns=None)
print(">>>>> Standard")
for key in standard_metrics:
    print(f">>> {key}:\n{standard_metrics[key]}")
print(">>>>> Net")
for key in net_metrics:
    print(f">>> {key}:\n{net_metrics[key]}")
print(">>>>> Standard Week")
print(standard_week_metrics.keys())
for day in standard_week_metrics:
    print(f">>>{day}")
    for key in standard_week_metrics[day]:
        print(f">>>>> {key}:\n{standard_week_metrics[day][key]}")
print(">>>>> Net Week")
for day in net_week_metrics:
    print(f">>>{day}")
    for key in net_week_metrics[day]:
        print(f">>>>> {key}:\n{net_week_metrics[day][key]}")

#plot_progress( cumulative_words_written(df, project_columns, essential_columns, subgoal_columns), subgoal_columns=subgoal_columns, essential_columns=essential_columns, omit_goals=True )