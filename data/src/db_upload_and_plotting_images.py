import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from pathlib import Path

from db import get_db_engine

# Output folder
IMAGE_DIR = Path("data/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

engine = get_db_engine()


from db import get_db_engine

engine = get_db_engine()

# Load CSV file into pandas DataFrame
df = pd.read_csv("Original_data.csv")

# Rename columns
df = df.rename(columns={'AGE':'Age','GENDER':'Gender',
       'Do you invest in Investment Avenues?':'Investment_Avenues',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Mutual Funds]': 'Mutual_Funds',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Equity Market]': 'Equity_Market',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Debentures]': 'Debentures',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Government Bonds]': 'Government_Bonds',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Fixed Deposits]': 'Fixed_Deposits',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Public Provident Fund]': 'Public_Provident_Fund',
       'What do you think are the best options for investing your money? (Rank in order of preference) [Gold]': 'Gold',
       'Do you invest in Stock Market?': 'Stock_Market',
       'What are the factors considered by you while investing in any instrument?': 'Investment_Factors',
       'What is your investment objective?': 'Investment_Objective',
       'What is your purpose behind investment?': 'Investment_Purpose',
       'How long do you prefer to keep your money in any investment instrument?': 'Investment_Horizon',
       'How often do you monitor your investment?': 'Monitoring_Frequency',
       'How much return do you expect from any investment instrument?': 'Expected_Return',
       'Which investment avenue do you mostly invest in?': 'Preferred_Investment_Avenue',
       'What are your savings objectives?': 'Savings_Objectives',
       'Reasons for investing in Equity Market': 'Reasons_for_Equity_Market',
       'Reasons for investing in Mutual Funds': 'Reasons_for_Mutual_Funds',
       'Reasons for investing in Government Bonds': 'Reasons_for_Government_Bonds',
       'Reasons for investing in Fixed Deposits ': 'Reasons_for_Fixed_Deposits ',
       'Your sources of information for investments is ': 'Sources_of_Information'})


# Gender distribution - pie chart
ax = df['Gender'].value_counts() \
.plot(kind='pie',
    title='Gender Distribution of Survey Participants',
    autopct='%1.1f%%',
    startangle=90,
    counterclock=False) 
plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "gender_distribution.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()



# Age distribution - pie chart
ax = df['Age'].value_counts() \
.sort_index() \
.plot(
    kind='pie',
    title='Age Distribution of Survey Participants',
    autopct='%1.1f%%',
    pctdistance=0.87,
    startangle=90,
    counterclock=False) 

# Adjust percentage texts inside sectors of the pie chart
for text in ax.texts:
    if '%' in text.get_text():
        text.set_fontsize(7)
        text.set_fontstyle('italic')
        text.set_color('white')

plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "age_distribution.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()




# Respondents' interest in Investment Avenues - pie chart
df_ia = df.groupby('Investment_Avenues')[['Gender']].value_counts()
ax = df_ia.plot(kind='pie',
    title='Respondents responses to opportunities in Investment Avenues',
    autopct='%1.1f%%',
    pctdistance=0.7,

        # Custom colors
    colors=["#ff9ca2", "#609d4d", "#8fe079"],

    startangle=65) 

plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "investment_avenues.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()


# Respondents' interest in Stock Market - pie chart
df_sm = df.groupby('Stock_Market')[['Gender']].value_counts()

ax = df_sm.plot(kind='pie',
    title='Respondents responses to opportunities in Stock Market',
    autopct='%1.1f%%',
    pctdistance=0.7,

    # Custom colors
    colors=["#ff9ca2", "#f14b7d", "#609d4d", "#8fe079"],

    startangle=45) 



plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "stock_market.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()



# Average ranking of Investment avenues - bar plot

cols = ['Mutual_Funds', 'Equity_Market',
        'Debentures', 'Government_Bonds', 'Fixed_Deposits',
        'Public_Provident_Fund', 'Gold']

grouped = df.groupby('Gender')[cols].mean()

ax = grouped.T.plot(
    kind='barh',
    title='Investment Avenues Average Ranking'
)

ax.set_xlabel('Average Score (Lower is More Preferred)')
ax.set_ylabel('Investment Type')

plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "investment_avenues_ranking.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()


# Average ranking of Investment avenues by respondents under 25 y.o. - bar plot

cols = ['Mutual_Funds', 'Equity_Market',
        'Debentures', 'Government_Bonds', 'Fixed_Deposits',
        'Public_Provident_Fund', 'Gold']

# Filter the DataFrame to include only respondents under 25 years old
df_under_25 = df[df['Age'] <= 25]

grouped = df_under_25.groupby('Gender')[cols].mean()
ax = grouped.T.plot(
    kind='barh',
    title='Investment Avenues Average Ranking by Respondents <= 25 y.o.'
)

ax.set_xlabel('Average Score (Lower is More Preferred)')
ax.set_ylabel('Investment Type')

plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "investment_avenues_ranking_under_25.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()


# Most common answers given by Respondents separated by Gender and their respective occurence percentage ratio - bar plot

results = []

for column in df.columns[11:]:
    row = {'Column': column}

    for gender in ['Male', 'Female']:
        df_gender = df[df['Gender'] == gender]

        vc = df_gender[column].value_counts()

        most_common = vc.idxmax()
        pct = math.ceil(100 * vc.max() / len(df_gender))

        row[f'{gender}_Answer'] = most_common
        row[f'{gender}_Ratio'] = pct

    results.append(row)

df_responses = pd.DataFrame(results).set_index('Column')

# labels

def make_label(row):
    if row['Male_Answer'] == row['Female_Answer']:
        return row['Male_Answer']
    else:
        return f"M: {row['Male_Answer']} | F: {row['Female_Answer']}"

df_responses['Answer_Label'] = df_responses.apply(make_label, axis=1)

# Plot

# import MultipleLocator for better control over y-axis ticks  
from matplotlib.ticker import MultipleLocator


plot_df = df_responses[['Male_Ratio', 'Female_Ratio']].rename(
    columns={
        'Male_Ratio': 'Men',
        'Female_Ratio': 'Women'
    }
)

ax = plot_df.plot(
    kind='barh',
    title='Most Common Answers by Gender',
    figsize=(14, 6)
)

ax.set_xlabel('Ratio (%)')
ax.set_ylabel('Questions')

# Grid only on x-axis
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_minor_locator(MultipleLocator(10))

ax.grid(which='major', linestyle='--', linewidth=0.6)
ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.5)

# Add x-axis labels for better readability
for i, label in enumerate(df_responses['Answer_Label']):
    ax.text(
        plot_df.iloc[i].max() + 1,  # x-position (right of bar)
        i,                           # y-position
        label,
        va='center',
        fontsize=7
    )
plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "most_common_answers.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()



# Most common answers given by Young Respondents under 25 y.o. separated by Gender and their respective occurence percentage ratio - bar plot

results = []

# Filter the DataFrame to include only respondents under 25 years old
df_under_25 = df[df['Age'] <= 25]

for column in df_under_25.columns[11:]:
    row = {'Column': column}

    for gender in ['Male', 'Female']:
        df_gender = df_under_25[df_under_25['Gender'] == gender]

        vc = df_gender[column].value_counts()

        most_common = vc.idxmax()
        pct = math.ceil(100 * vc.max() / len(df_gender))

        row[f'{gender}_Answer'] = most_common
        row[f'{gender}_Ratio'] = pct

    results.append(row)

df_responses = pd.DataFrame(results).set_index('Column')

# labels

def make_label(row):
    if row['Male_Answer'] == row['Female_Answer']:
        return row['Male_Answer']
    else:
        return f"M: {row['Male_Answer']} | F: {row['Female_Answer']}"

df_responses['Answer_Label'] = df_responses.apply(make_label, axis=1)

# Plot

# import MultipleLocator for better control over y-axis ticks  
from matplotlib.ticker import MultipleLocator


plot_df = df_responses[['Male_Ratio', 'Female_Ratio']].rename(
    columns={
        'Male_Ratio': 'Men',
        'Female_Ratio': 'Women'
    }
)

ax = plot_df.plot(
    kind='barh',
    title='Most Common Answers of respondents <= 25 y.o. by Gender',
    figsize=(14, 6)
)

ax.set_xlabel('Ratio (%)')
ax.set_ylabel('Questions')

# Grid only on x-axis
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_minor_locator(MultipleLocator(10))

ax.grid(which='major', linestyle='--', linewidth=0.6)
ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.5)

# Add x-axis labels for better readability
for i, label in enumerate(df_responses['Answer_Label']):
    ax.text(
        plot_df.iloc[i].max() + 1,  # x-position (right of bar)
        i,                           # y-position
        label,
        va='center',
        fontsize=7
    )
plt.tight_layout()

# Saving the plot as .png image
output_path = IMAGE_DIR / "most_common_answers_under_25.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_path}")

plt.show()