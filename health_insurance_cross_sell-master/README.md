# Health Insurance Cross-Selling
## Auto Insurance

![alt_text](reports/figures/head.jpg) 

# 1 - Business Challenge
An Insurance company that has provided Health Insurance to its customers need to predict whether the policyholders (customers) from past year will also be interested in Vehicle Insurance provided by the company (Kaggle).
With the information about customers, the company did a survey asking customers if they are interested in car insurance, with this information a model will be made to rank the customers most likely to buy.

## 1.1 - Business Questions

	1. Main Insights on the most relevant attributes of customers interested in purchasing auto insurance.

	2. What percentage of customers interested in purchasing auto insurance will the sales team be able to contact by making 20,000 calls?

	3. If the sales team capacity increases to 40,000 calls, what percentage of customers interested in purchasing auto insurance will the sales team be able to contact?

	4. How many calls does the sales team need to make to contact 80% of customers interested in purchasing auto insurance?

# 2 - Business Assumptions

	1. Customers who already have Health Insurance may also be interested in Auto Insurance.
	
	2. Cross-selling increases customer loyalty.
	
	3. Learning from cross-selling can become a horizontal strategy for the company in the market.
	
	4. A machine learning model to rank customers most likely to buy will increase sales force productivity and accelerate new market entry.
	
# 3 - Solution Strategy

Methodology: CRISP-DS

1. Data Description: data dimensions, types, NaN verification, descriptive statistics, numerical attributes and categorical attributes
2. Feature Engineering: Mind Map of Hypotheses and feature derivation
3. Exploratory Data Analysis: Univariate, bivariate and multivariate analysis
4. Data Preparation: Data division into training and testing, coding, standardization and rescaling.
5. Feature Selection: Feature importance
6. Machine Learning: KNN, Logistic Regression and Extra Tree
7. Model performance: recall and accuracy top k 
8. Business performance: Business questions
9. Deployment: API in Heroku and access to ranking via Google Sheets

# 4 - Top 3 Data Insights

### Hypothesis 1: Customers with new cars are more interested in insurance

Result: True

![alt_text](reports/figures/car_age.png)

This information can drive the sales team and impact the Machine Learning model.
 
### Hypothesis 4. Older people are more interested in auto insurance

Result: True

![alt_text](reports/figures/age.png) 

Clients between 33 and 52 years represent 58% of the interested group

### Hypothesis 2. Damaged cars are more insured

Result: False

Of the group of customers who already have insurance, only 6% had any damage to their car, indicating a low-risk market.

# 5 - Machine Learning Model

![alt_text](reports/figures/gain_curve.png) 

The Logistic Regression model was selected for presenting the best performance of the tested algorithms.

X-Axis: Number of customers

Y-Axis: Algorithm's ability to sort by customers likely to buy

# 6 - Machine Learning Performance

Ranking Position: 2000 

Recall: 0.08 

Precison: 0.32

# 7 - Business Result

### 1. Main Insights on the most relevant attributes of customers interested in purchasing auto insurance.

- Customers with new cars are more likely to take out insurance.
- 58% of the positive response are between 33 and 52 years old
- 76% of customers who had damaged cars responded positively.
- Men represent the most positive responses.

### 2. What percentage of customers interested in purchasing auto insurance will the sales team be able to contact by making 20,000 calls?

- With 20.000 calls sales team will be contact 61% of customers interested

### 3. If the sales team capacity increases to 40,000 calls, what percentage of customers interested in purchasing auto insurance will the sales team be able to contact?

- With 40.000 calls sales team will be contact 99% of customers interested

### 4. How many calls does the sales team need to make to contact 80% of customers interested in purchasing auto insurance?

- With 27.500 calls sales team will be contact 80% of customers interested

# 8 - Deploy


![alt_text](reports/figures/sheets.gif) 

The API with the ranking model is available to the company and can be accessed by Google Sheets, the sales team can provide the customer information to get the ranking score.

# 9 - Lessons Learned

The problem of learning to rank requires other metrics to assess the performance of the algorithm, these metrics are adapted from classification models.

# 10 - Next Steps to Improve

In this solution, classes were not balanced in model training. Another tool is the application of hyperparameters to improve algorithm performance and cross-validation to ensure that the algorithm evaluation is not biased.
