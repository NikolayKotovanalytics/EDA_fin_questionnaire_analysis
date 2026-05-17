-- Phase 3 - Gender-based questions about investment analysis

-- Step 1: Analysis of factors influencing investment preferences

-- CTEs which calculate percentage of male/female respondents per option for a given question

WITH prep_factor AS (
    SELECT 
        Factor,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Factor)
,
prep_objective AS (
    SELECT 
        Objective,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Objective)
,
prep_purpose AS (
    SELECT 
        Purpose,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Purpose)
,
prep_duration AS (
    SELECT 
        Duration,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Duration)
,
prep_invest_monitor AS (
    SELECT 
        Invest_monitor,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Invest_monitor)    
,
prep_expect AS (
    SELECT 
        Expect,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Expect)    
,
prep_avenue AS (
    SELECT 
        Avenue,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Avenue)    
,
prep_savings_objectives AS (
    SELECT 
        `What are your savings objectives?`, -- NOTE: Used `` symbols to read header in the coloumn, it is not '' text symbols
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY `What are your savings objectives?`)    
,
prep_reason_equity AS (
    SELECT 
        Reason_Equity,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Reason_Equity)    
,
prep_reason_mutual AS (
    SELECT 
        Reason_Mutual,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Reason_Mutual)
,
prep_reason_bonds AS (
    SELECT 
        Reason_Bonds,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Reason_Bonds)    
,
prep_reason_fd AS (
    SELECT 
        Reason_FD,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Reason_FD)    
,
prep_source AS (
    SELECT 
        Source,
        100 *COUNT(CASE WHEN gender = 'Male' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Male') AS males_selection_pct,
        100 * COUNT(CASE WHEN gender = 'Female' THEN 1 END) / (SELECT COUNT(*) FROM finance_data WHERE gender = 'Female') AS females_selection_pct
    FROM finance_data
    GROUP BY Source)    


 -- Main Query which filters uses CTEs results to show only 1 TOP option chosen by most respondents
 -- and provides percentage of respondents voted out of total per gender


SELECT 
    CONCAT('Main factor: ', factor) AS respondent_responses,
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_factor
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_factor)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_factor)

UNION -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT
    CONCAT('Goal: ', Objective),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_objective
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_objective)
 OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_objective)

UNION -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Purpose: ', Purpose),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_purpose
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_purpose)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_purpose)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Duration: ', Duration),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_duration
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_duration)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_duration)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Regular monitoring: ', Invest_Monitor),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_invest_monitor
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_invest_monitor)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_invest_monitor)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Expected returns: ', Expect),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_expect
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_expect)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_expect)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Investments via: ', Avenue),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_avenue
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_avenue)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_avenue)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Main financial contribution: ', `What are your savings objectives?`),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_savings_objectives
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_savings_objectives)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_savings_objectives)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

 SELECT 
    CONCAT('Reason Equity: ', Reason_Equity),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_reason_equity
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_reason_equity)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_reason_equity)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Reason Mutual: ', Reason_Mutual),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_reason_mutual
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_reason_mutual)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_reason_mutual)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Reason Bonds: ', Reason_Bonds),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_reason_bonds
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_reason_bonds)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_reason_bonds)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Reason FD: ', Reason_FD),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_reason_fd
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_reason_fd)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_reason_fd)

UNION  -- combines results of CTEs into one result set, showing only the top factor for each question

SELECT 
    CONCAT('Information Source: ', Source),
    ROUND(males_selection_pct, 1) AS males_selection_pct,
    ROUND(females_selection_pct, 1) AS females_selection_pct
FROM prep_source
WHERE males_selection_pct = (SELECT MAX(males_selection_pct) FROM prep_source)
   OR females_selection_pct = (SELECT MAX(females_selection_pct) FROM prep_source)
;
