import pandas as pd 

# reads data and skips first row, last couple rows
couple_rows = [0, 1, 2] 
df = pd.read_excel(r'A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx', skiprows=couple_rows)
df = df.iloc[:-28] # removes last 28 rows

# Step 1: remove all rows in col 6 with rural, urban, and subdistrict
print("\nStep 1: Ignore rural, urban, ignore subdistrict.")
print("**Note: Pandas dataframes show index as the first column but it is removed in the output")
df = df[~df[4].str.contains("SUB-DISTRICT")]
df = df[~df[4].str.contains("DISTRICT")]
df = df[~df[4].str.contains("INDIA")]
df = df[~df[6].str.contains("Rural")]
df = df[~df[6].str.contains("Urban")]
df = df.reset_index(drop = True)
print('\n')
print(df)
print("\nResult: india (1) + 35 (states +UTs) + 640 Districts = 676 records + headers")
print("Putting result in new file named: reduced-state.csv")
df.to_csv('reduced-state.csv', index=False, encoding='utf-8') 