import pandas as pd
import numpy as np 
import random 

#load and structure the data: 

#load cleaned file 
data = pd.read_csv("ms_data.csv")
#convert visit date to date time
data['visit_date'] = pd.to_datetime(data['visit_date'])
#sort by patient_id and visit_date
data = data.sort_values(by=['patient_id', 'visit_date'])

#add insurance information 
#read insurance type from insurance.list 
with open('insurance.lst', 'r') as f:
    insurance_types = [line.strip () for line in f if line.strip()]

#randomly assign insurance type per patient_id
unique_patients = data['patient_id'].unique()
patient_insurance_mapping = {
    patient_id: random.choice(insurance_types) for patient_id in unique_patients
}
data['insurance_type'] = data['patient_id'].map(patient_insurance_mapping)

#generate visit costs based on insurance type
#fed in base costs for each insurance type 
insurance_costs = {
    'Basic': 100, 
    'Premium': 200,
    'Platinum': 300
}
#add random variation to costs 
data['visit_cost'] = data['insurance_type'].map(insurance_costs) + np.random.uniform(-20, 20, size=len(data))

#4. calculate summary statistics 
#mean walking speed by education level 
mean_speed_by_edu = data.groupby('education_level')['walking_speed'].mean()

#mean costs by insurance type 
mean_cost_by_type = data.groupby('insurance_type')['visit_cost'].mean()

#age effects on walking speed 
age_speed = data[['age', 'walking_speed']].corr().iloc[0, 1]

#handle missing data 
data = data.dropna()

#seasonal variations 
# Extract seasonal information
data['month'] = data['visit_date'].dt.month
data['season'] = data['month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})

#adjust walking speed by season
seasonal_walking_adj = {
    'Winter': -0.5,
    'Spring': 0.1,
    'Summer': 0.2,
    'Fall': 0.0
}
data['walking_speed'] += data['season'].map(seasonal_walking_adj)

#seasonal effects on costs 
seasonal_cost_adjustment = {
    'Winter': 10,
    'Spring': -5,
    'Summer': 0,
    'Fall': 5
}
data['visit_cost'] += data['season'].map(seasonal_cost_adjustment)

#mean walking speed and visit costs by season 
mean_walking_speed_by_season = data.groupby('season')['walking_speed'].mean()
mean_cost_by_season = data.groupby('season')['visit_cost'].mean()

#5. display summary statistics 
print("Summary Statistics:")
print("Mean Walking Speed by Education Level:")
print(mean_speed_by_edu)

print("Mean Costs by Insurance Type:")
print(mean_cost_by_type)

print("Correlation between Age and Walking Speed:")
print(age_speed)

print("Mean Walking Speed by Season:")
print(mean_walking_speed_by_season)

print("Mean Costs by Season:")
print(mean_cost_by_season)

#save processed data for further use 
data.to_csv('processed_ms_data.csv', index=False)
