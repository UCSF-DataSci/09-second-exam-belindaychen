import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, kruskal
from statsmodels.stats.anova import AnovaRM

#load cleaned data
data = pd.read_csv('processed_ms_data.csv')

#multiple regression: walking speed with education and age
#convert categorical education_level to dummy variables 
data['education_level'] = data['education_level'].astype('category')
data['education_code'] = data['education_level'].cat.codes

#mixed-effects model for repeated measures 
model = smf.mixedlm("walking_speed ~ age + education_code", data, groups=data['patient_id'])
results = model.fit()
print("Mixed Effects Model Results:")
print(results.summary())

#education-age interaction effects 
interaction_model = smf.ols("walking_speed ~ age * education_code", data=data).fit()
print("Interaction Model Results:")
print(interaction_model.summary())

#analyze costs: insurace type effect 
#using ANOVA for cost by insurance type 
anova_result = f_oneway(
    *[data.loc[data['insurance_type'] == t, 'visit_cost'] for t in data['insurance_type'].unique()]
)
print("ANOVA Results for Visit Costs by Insurance Type:")
print(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}")

#box plot of costs by insurance type
plt.figure()
data.boxplot(column='visit_cost', by='insurance_type')
plt.title('Visit Costs by Insurance Type')
plt.ylabel('Visit Cost')
plt.xlabel('Insurance Type')
plt.suptitle('')
plt.show()


# summary stats for cost
mean_costs = data.groupby('insurance_type')['visit_cost'].mean()
median_costs = data.groupby('insurance_type')['visit_cost'].median()
print("Mean and Median Costs by Insurance Type:")
print("Mean Costs:", mean_costs)
print("Median Costs:", median_costs)

# correlation between age and walking speed
age_walking_corr = data[['age', 'walking_speed']].corr().iloc[0, 1]
print("Correlation between Age and Walking Speed:")
print(age_walking_corr)

# advanced control for confounders
confounder_model = smf.ols("walking_speed ~ age + education_code + insurance_type + month", data=data).fit()
print("Model with Confounders Controlled:")
print(confounder_model.summary())
