import pandas as pd 

# reads data and skips first row, last couple rows
couple_rows = [0, 1, 2] 
df = pd.read_excel(r'..\A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx', skiprows=couple_rows)
df = df.iloc[:-28] # removes last 28 rows

# because col 1 extracted as float, convert to string to get back the actual values
df[1] = df[1].astype(str)
df[1] = df[1].replace(regex=['\.'], value='')

# Step 1: remove all rows in col 6 with rural, urban, and subdistrict
print("\nStep 1: Ignore rural, urban, ignore subdistrict.")
print("**Note: Pandas dataframes show index as the first column but it is removed in the output")
df = df[~df[4].str.contains("SUB-DISTRICT")]
df = df[~df[6].str.contains("Rural")]
df = df[~df[6].str.contains("Urban")]
df = df.reset_index(drop = True)
print('\n')
print(df)
print("\nResult: india (1) + 35 (states +UTs) + 640 Districts = 676 records + headers")
print("Putting result in new file named: reduced.csv")
df.to_csv('reduced.csv', index=False, encoding='utf-8') 

# running scripts
passes = 0 # index of number of passes
# these dataframes are useful here:
df1 = df[df[4].str.contains("STATE")] # creates new dataframe with only STATE's
df2 = df[df[4].str.contains("DISTRICT")] # creates new dataframe with only DISTRICT's

# Step 2:  Run data integrity check on population data
print("\nRunning Data Integrity Checks on Population Data...") 
# Check 1
# int(df.iloc[0, 10]) --> india population
# int(df1[11].sum()) --> state population
if (int(df1[11].sum()) == int(df.iloc[0, 10])):
    print('Check 1: States + UT pop = India Pop PASS')
    passes += 1
else:
    print('Check 1: States + UT pop = India Pop FAIL')
#Check 2
district_sum = df2.groupby([1], sort=False).sum() # finds the sum by grouping the State Code 
# Reset index just to make tables similar 
district_sum = district_sum[11].reset_index(drop = True) 
pop_state = df1[11].reset_index(drop = True)
if (district_sum.equals(pop_state)):
    print("Check 2: For each state and UT, sum of pop of districts = pop of state or UT PASS")
    passes += 1
else:
    print("Check 2: For each state and UT, sum of pop of districts = pop of state or UT FAIL")

#Step 3: Run data integrity check on Area:
print("\nRunning Data Integrity Checks on Area...")
#Check 1: 
# Since df1 is a dataframe with States, you can find the sums of all of the area in column 13
# df1[13].sum() -->  sum of state area
# df.iloc[0, 12] --> India area
if (int(df1[13].sum()) == int(df.iloc[0, 12])):
    print("Check 1: States + UT Area = India PASS")
    passes += 1
else:
    print("Check 1: States + UT Area = India FAIL")
#Check 2: For each state and UT, sum of area of districts = area of state or UT
district_sum = df2.groupby([1], sort=False).sum() # finds the sum by grouping the State Code 
# Reset index just to make tables similar 
district_sum = district_sum[13].reset_index(drop = True) 
pop_state = df1[13].reset_index(drop = True)
if (district_sum.equals(pop_state)):
    print("Check 2: For each state and UT, sum of area of districts = area of state or UT PASS")
    passes += 1
else:
    print("Check 2: For each state and UT, sum of area of districts = area of state or UT FAIL")

print("\nResults:")
print("Passed " + str(passes) + "/4")
