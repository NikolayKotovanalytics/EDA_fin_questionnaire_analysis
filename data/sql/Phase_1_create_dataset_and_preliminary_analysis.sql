-- STEP 1: Create dataset and upload data

CREATE DATABASE finance_dataset;

USE finance_dataset;
-- NOTE: Data was uploaded from CSV using Python (pandas)


-- STEP 2: Overview data

DESCRIBE finance_data; -- check dataset structure and column data types

SELECT * 
FROM finance_data
LIMIT 5; -- quick preview to ensure data was loaded correctly

SELECT
    SUM(gender IS NULL) AS gender_nulls,            
    SUM(age IS NULL) AS age_nulls,               
    SUM(Mutual_Funds IS NULL) AS mutual_nulls,                  
    SUM(Equity_Market IS NULL) AS equity_nulls,                
    SUM(Debentures IS NULL) AS debentures_nulls,                   
    SUM(Government_Bonds IS NULL) AS government_bonds_nulls,   
    SUM(Fixed_Deposits IS NULL) AS fixed_deposits_nulls, 
    SUM(ppf IS NULL) AS ppf_nulls,     
    SUM(gold IS NULL) AS gold_nulls,   
    SUM(Factor IS NULL) AS factor_nulls,         
    SUM(Objective IS NULL) AS objective_nulls,         
    SUM(Purpose IS NULL) AS purpose_nulls,   
    SUM(Duration IS NULL) AS duration_nulls,          
    SUM(Invest_monitor IS NULL) AS invest_monitor_nulls,     
    SUM(Expect IS NULL) AS expect_nulls,          
    SUM(Avenue IS NULL) AS avenue_nulls,              
    SUM(`What are your savings objectives?` IS NULL) AS savings_nulls,    
    SUM(Reason_Equity IS NULL) AS reason_equity_nulls,
    SUM(Reason_Mutual IS NULL) AS reason_mutual_nulls,       
    SUM(Reason_Bonds IS NULL) AS reason_bonds_nulls,      
    SUM(Reason_FD IS NULL) AS reason_fd_nulls, 
    SUM(Source IS NULL) AS source_nulls     
FROM finance_data;
-- Note: no missing responses were found in the dataset

-- STEP 3: Gender distribution (used later for pie chart)

SELECT 
    COUNT(*) AS total_questioned,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS total_males,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS total_females
FROM finance_data;

-- STEP 4: Analyse age distribution

SELECT  -- basic age statistics
    MIN(age) AS youngest_person_questioned,
    MAX(age) AS oldest_person_questioned,
    ROUND(AVG(age), 1) AS average_age,

    -- Count respondents older than the average age
    COUNT(
        CASE
            WHEN age > (SELECT AVG(age) FROM finance_data WHERE age IS NOT NULL)
            THEN 1
        END
    ) AS above_avg_age,

    -- Age segmentation (used later for pie chart)
    COUNT(CASE WHEN age BETWEEN 21 AND 25 THEN 1 END) AS total_young_people,
    COUNT(CASE WHEN age BETWEEN 26 AND 30 THEN 1 END) AS total_middleaged_people,
    COUNT(CASE WHEN age > 30 THEN 1 END) AS total_over30_people

FROM finance_data

WHERE age IS NOT NULL; -- ensures average is calculated correctly

