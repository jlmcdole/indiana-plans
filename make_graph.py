# H354 GitHub project: Indiana plans, premium vs deductible
# Usage: python make_graph.py "Extra Credit.xlsm"   (a .xlsx or .csv works too)
import sys
import pandas as pd
import matplotlib.pyplot as plt

path = sys.argv[1]
# the file can be xlsx or xlsm so check which one it is, excel files take a bit to load
if path.lower().endswith((".xlsx", ".xlsm")):
    # the real column names are in the second row of this file, the first row is group labels
    df = pd.read_excel(path, dtype=str, header=1)
else:
    df = pd.read_csv(path, dtype=str)
print("rows in whole file:", len(df))

# helper to find a column by words in its name
def find_col(words):
    for c in df.columns:
        if all(w.lower() in c.lower() for w in words):
            return c
    return None

# keep only Indiana
state_col = find_col(["state", "code"])
df = df[df[state_col].str.strip() == "IN"].copy()
print("rows after keeping Indiana:", len(df))
# small Indiana only copy, easy to upload or paste into another AI tool
df.to_csv("indiana_plans_only.csv", index=False)

# premium and deductible columns, I picked the age 40 premium and the individual medical deductible
prem_col = find_col(["premium", "adult", "individual", "age 40"])
ded_col = find_col(["medical", "deductible", "individual", "standard"])
print("premium column:", prem_col)
print("deductible column:", ded_col)

# turn text like "$1,500" into a number, anything else becomes NaN
def to_num(s):
    return pd.to_numeric(s.str.replace(r"[$,]", "", regex=True), errors="coerce")

df["premium"] = to_num(df[prem_col])
df["deductible"] = to_num(df[ded_col])
df = df.dropna(subset=["premium", "deductible"])

# the file repeats each plan for every county, so drop repeats to get one dot per plan
id_col = find_col(["plan id"])
area_col = find_col(["rating area"])
keys = [c for c in [id_col, area_col] if c]
df = df.drop_duplicates(subset=keys)
print("plans left after cleaning:", len(df))

# scatter plot, premium on x and deductible on y like the slide
plt.figure(figsize=(8, 6))
plt.scatter(df["premium"], df["deductible"], alpha=0.6)
plt.xlabel("Monthly premium ($, age 40)")
plt.ylabel("Individual medical deductible ($)")
plt.title("Indiana marketplace plans: premium vs deductible")
plt.savefig("premium_vs_deductible.png", dpi=150, bbox_inches="tight")
print("saved premium_vs_deductible.png")
