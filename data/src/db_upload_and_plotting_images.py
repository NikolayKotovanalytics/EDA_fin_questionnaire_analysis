import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from db import get_db_engine

engine = get_db_engine()

# Load CSV file into pandas DataFrame
df = pd.read_csv("E:/Kaggle/Finance Data/Finance_data.csv")

# Upload DataFrame to MySQL table

df.to_sql("finance_data", engine, if_exists="replace", index=False)

# Quick sanity check to ensure data loaded correctly

print(df.shape)   # number of rows and columns
print(df.head())  # preview first 5 rows

query = "SELECT * FROM finance_data LIMIT 5;"  # Check 5 rows from the MySQL table
df_query = pd.read_sql(query, engine)

print(df_query)

#============================================================================

# Plot 1: Gender distribution of survey participants using SQL and Matplotlib

# SQL query calculating gender counts and percentages
query1 = """
SELECT 
    COUNT(*) as total_questioned,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS total_males,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS total_females
FROM finance_data;
"""

df_query1 = pd.read_sql(query1, engine) 

# Extracting values for the pie chart from the SQL query results
values = [
    df_query1.loc[0, "total_males"],
    df_query1.loc[0, "total_females"]
]

labels = ["Male", "Female"]

plt.figure(figsize=(6,6))

colors = ["#4C72B0", "#C7652B"]

# Create pie chart
plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%", # shows percentage on pie charts with one decimal place
    startangle=90,
    colors=colors
)

plt.title("Gender Distribution of Survey Participants")

plt.tight_layout()
#plt.savefig("C:\\...\\images\\fd_gender_distribution.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================


# Plot 2: Age distribution of survey participants using SQL and Matplotlib

# SQL query calculating gender counts and percentages

query2 = """
SELECT 
    COUNT(CASE WHEN age BETWEEN 21 AND 25 THEN 1 END) AS total_young_people,
    COUNT(CASE WHEN age BETWEEN 26 AND 30 THEN 1 END) AS total_middleaged_people,
    COUNT(CASE WHEN age > 30 THEN 1 END) AS total_over30_people
FROM finance_data
WHERE age IS NOT NULL;
"""

df_query2 = pd.read_sql(query2, engine) 

# Extracting values for the pie chart from the SQL query results
values = [
    df_query2.loc[0, "total_young_people"], # retieves the value of row 0 and the targeted column 
    df_query2.loc[0, "total_middleaged_people"],
    df_query2.loc[0, "total_over30_people"]
]

labels = ["21-25", "26-30", "31+"]

plt.figure(figsize=(6,6))

colors = ["#72D167", "#F4B248", "#AA449F"]

# Plotting the pie chart with specified colors, labels, and percentage display
plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%", # Display percentage on pie charts with one decimal place
    startangle=-150,
    colors=colors,
    counterclock=False
)

plt.title("Age Distribution of Survey Participants")

plt.tight_layout()
#plt.savefig("C:\\...\\images\\fd_age_distribution.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================

# Plot 3: Investment preferences avergaed among survey participants and divided by gender using SQL and Matplotlib

# SQL query calculating gender counts, percentages, and average preference ranks for each investment type

query3 = """
SELECT 
    COUNT(*) AS respondents,
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,
    AVG(Mutual_Funds) AS average_mutual_funds_preference_rank,
    AVG(Equity_Market) AS average_equity_market_preference_rank,
    AVG(Debentures) AS average_debentures_preference_rank,
    AVG(Government_Bonds) AS average_goverment_bonds_preference_rank,
    AVG(Fixed_Deposits) AS average_fixed_deposits_preference_rank,
    AVG(ppf) AS average_ppf_preference_rank,
    AVG(gold) AS average_gold_preference_rank
FROM finance_data
WHERE gender = 'Male'
UNION -- Used to combine Gender-based datasets in one table for easier comparison
SELECT 
    COUNT(*) AS respondents,
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,
    AVG(Mutual_Funds) AS average_mutual_funds_preference_rank,
    AVG(Equity_Market) AS average_equity_market_preference_rank,
    AVG(Debentures) AS average_debentures_preference_rank,
    AVG(Government_Bonds) AS average_goverment_bonds_preference_rank,
    AVG(Fixed_Deposits) AS average_fixed_deposits_preference_rank,
    AVG(ppf) AS average_ppf_preference_rank,
    AVG(gold) AS average_gold_preference_rank
FROM finance_data
WHERE gender = 'Female';
"""

# Extracting values for the block chart from the SQL query results

df3 = pd.read_sql(query3, engine)

# Ensure all values are numeric
df3 = df3.apply(pd.to_numeric)

categories = [
    "Mutual Funds",
    "Equity Market",
    "Debentures",
    "Gov Bonds",
    "Fixed Deposits",
    "PPF",
    "Gold"
]

x = range(len(categories))
width = 0.3

plt.figure(figsize=(10,6))

plt.bar([i - width/2 for i in x], df3.iloc[0, 2:], width, label="Male")     # skips first 2 coloumns (respondents and investment_interest_pct) and plot only preference ranks
plt.bar([i + width/2 for i in x], df3.iloc[1, 2:], width, label="Female")   # skips first 2 coloumns (respondents and investment_interest_pct) and plot only preference ranks

plt.xticks(x, categories, rotation=15)

plt.title("Average Investment Preference Rank by Gender")
plt.ylabel("Average Rank")
plt.xlabel("Investment Type")

plt.legend()
plt.tight_layout()
#plt.savefig("C:\\...\\images\\fd_investment_preferences.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================

# Plot 4: Investment preferences averaged among survey participants which are <= 25 y.o. divided by gender using SQL and Matplotlib

# SQL query calculating average preference ranks for each investment type
query4 = """
SELECT 
    AVG(Mutual_Funds) AS average_mutual_funds_preference_rank,
    AVG(Equity_Market) AS average_equity_market_preference_rank,
    AVG(Debentures) AS average_debentures_preference_rank,
    AVG(Government_Bonds) AS average_goverment_bonds_preference_rank,
    AVG(Fixed_Deposits) AS average_fixed_deposits_preference_rank,
    AVG(ppf) AS average_ppf_preference_rank,
    AVG(gold) AS average_gold_preference_rank
FROM finance_data
WHERE gender = 'Male' AND age <= 25
UNION -- Used to combine Gender-based datasets in one table for easier comparison
SELECT 
    AVG(Mutual_Funds) AS average_mutual_funds_preference_rank,
    AVG(Equity_Market) AS average_equity_market_preference_rank,
    AVG(Debentures) AS average_debentures_preference_rank,
    AVG(Government_Bonds) AS average_goverment_bonds_preference_rank,
    AVG(Fixed_Deposits) AS average_fixed_deposits_preference_rank,
    AVG(ppf) AS average_ppf_preference_rank,
    AVG(gold) AS average_gold_preference_rank
FROM finance_data
WHERE gender = 'Female' AND age <= 25;
"""

# Extracting values for the histogram chart from the SQL query results
df4 = pd.read_sql(query4, engine)

# Ensure all values are numeric
df4 = df4.apply(pd.to_numeric)

categories = [
    "Mutual Funds",
    "Equity Market",
    "Debentures",
    "Gov Bonds",
    "Fixed Deposits",
    "PPF",
    "Gold"
]

x = range(len(categories))
width = 0.3

plt.figure(figsize=(10,6))

plt.bar([i - width/2 for i in x], df4.iloc[0], width, label="Young Males")
plt.bar([i + width/2 for i in x], df4.iloc[1], width, label="Young Females")

plt.xticks(x, categories, rotation=15)

plt.title("Average Investment Preference Rank by Gender (Age ≤ 25)")
plt.ylabel("Average Rank")
plt.xlabel("Investment Type")

plt.legend()
plt.tight_layout()

#plt.savefig("C:\\...\\images\\fd_Youngs_investment_preferences.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================


# Plot 5: Interest in Stock Market Investments according to survey participants divided by gender using SQL and Matplotlib

# SQL Query to calculate percent of respondents who prefer stock market investments divided by gender

query5 = """
SELECT -- Calculates percent of respondents who prefer stock market investments for each gender
    gender,
    ROUND(100 * COUNT(CASE WHEN Stock_Marktet = 'Yes' THEN 1 END) / COUNT(*), 2) AS Stock_Market_Investment_Preference_Pct
FROM finance_data
GROUP BY gender;
"""

# Extracting values for the histogram chart from the SQL query results

df5= pd.read_sql(query5, engine)

# Ensure all values are numeric

bars = plt.bar(
    df5["gender"],
    df5["Stock_Market_Investment_Preference_Pct"],
    color=["#C7652B", "#4C72B0"])

# Add value labels on top of bars

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,  # center of bar
        height,                           # height of bar
        f"{height:.2f}%",                 # value displayed
        ha='center',
        va='bottom'
    )

plt.title("Interest in Stock Market Investments by Gender")
plt.ylabel("Interested Participants Percentage")
plt.xlabel("Gender")

#plt.savefig("C:\\...\\images\\interest_stock_market_investments_gender.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================


# Plot 6: Analysis of factors which have the most influence on investment preferences per gender
# Note: I decided to use pandas instead of SQL here for more concise and clear code

# SQL Query to convert all data in the table into a DataFrame for further analysis
df6 = pd.read_sql("SELECT * FROM finance_data", engine)

# Clean column names
df6.columns = df6.columns.str.strip().str.replace(" ", "_")

# Precompute gender totals
male_total = (df6["gender"] == "Male").sum()
female_total = (df6["gender"] == "Female").sum()

# Function to calculate top responses for each question and their percentages by gender
def calculate_top_response(df6, column, label):

    grouped = df6.groupby(column)["gender"].value_counts().unstack(fill_value=0) # value_counts() counts the frequency of each unique value in the selected column ("gender") within each group created by the groupby operation.
                                                                                 # unstack(fill_value=0) transforms the resulting Series into a DataFrame by moving the innermost index level (the unique values from "gender") to columns. This creates a pivot table where rows are the group keys (from the groupby column), columns are the unique "gender" values, and cells contain the counts. fill_value=0 replaces any missing combinations (e.g., if a group has no "female") with 0 instead of NaN.
    # Calculate percentages per vote for each gender
    grouped["males_selection_pct"] = 100 * grouped.get("Male", 0) / male_total        # get(X,0) retrieves the value for the specified key, returning 0 if the key is not found
    grouped["females_selection_pct"] = 100 * grouped.get("Female", 0) / female_total  # get(X,0) retrieves the value for the specified key, returning 0 if the key is not found

    grouped = grouped[["males_selection_pct", "females_selection_pct"]]

    max_male = grouped["males_selection_pct"].max()
    max_female = grouped["females_selection_pct"].max()

# Select the response(s) with the highest percentage for each
    top = grouped[
        (grouped["males_selection_pct"] == max_male) |
        (grouped["females_selection_pct"] == max_female)
    ]

    top = top.round(1).reset_index() #round(1) rounds all numeric values in the DataFrame to 1 decimal place
                                     # reset_index() converts the current index (which contains the groupby column values) into a regular column and replaces it with a default integer index starting from 0. This makes the DataFrame easier to work with for plotting or further operations.

    top["Respondent_responses"] = label + top[column]

    return top[["Respondent_responses", "males_selection_pct", "females_selection_pct"]] # Return only the columns needed for plotting. Multiple colomns which is why dataframe used instead of series


columns = {
    "Factor": "Main factor: ",
    "Objective": "Goal: ",
    "Purpose": "Purpose: ",
    "Duration": "Duration: ",
    "Invest_Monitor": "Regular monitoring: ",
    "Expect": "Expected returns: ",
    "Avenue": "Investments via: ",
    "What_are_your_savings_objectives?": "Main financial contribution: ",
    "Reason_Equity": "Reason Equity: ",
    "Reason_Mutual": "Reason Mutual: ",
    "Reason_Bonds": "Reason Bonds: ",
    "Reason_FD": "Reason FD: ",
    "Source": "Information Source: "
}

results = pd.concat(
    [calculate_top_response(df6, col, label) for col, label in columns.items()]     # combines the returned DataFrames of the above function for each column into a single DataFrame for easier plotting
)

# Plot bar chart comparing top responses for each question by gender with % of respective respondents
plt.figure(figsize=(13,6))

results.set_index("Respondent_responses").plot(         # used results for plotting
    kind="bar",
    color=["#F4B248", "steelblue"],
    ax=plt.gca()
)

plt.title("Top Investment Responses by Gender")
plt.ylabel("Respondent Selection Percentage")
plt.xlabel("Survey Question")
plt.xticks(rotation=15, ha="right")

plt.legend(["Male", "Female"])

# Plot labels above the highest bar for each question

ax = plt.gca()  # Get current axes to add value labels on top of bars
                # plt.gca() (get current axes) returns the current Axes object from the active figure in matplotlib. 
                # This allows to modify the plot (e.g., add labels, annotations, or adjust properties) without explicitly creating or storing an axes reference earlier.

male_bars = ax.containers[0]
female_bars = ax.containers[1]

for i, (male_bar, female_bar) in enumerate(zip(male_bars, female_bars)): # iterate through bars to find the largest one and label it

    male_val = male_bar.get_height()        # get value of the bar
    female_val = female_bar.get_height()

    # Label only the highest bar
    if male_val >= female_val:
        bar = male_bar
        value = male_val
    else:
        bar = female_bar
        value = female_val

    ax.text(
        bar.get_x() + bar.get_width()/2, # x position (center of the bar) and width of the bar
        value + 0.5,                     # y position slightly above the bar (value + 0.5) to avoid overlap
        f"{value:.1f}%",                 # value label with one decimal place and percentage sign
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

#plt.savefig("C:\\...\\images\\top_investments_responses_gender.png", dpi=300) Example of picture saving path, adjust if needed
plt.show()

#============================================================================

engine.dispose() # Dispose of the engine to close all connections and free up resources

