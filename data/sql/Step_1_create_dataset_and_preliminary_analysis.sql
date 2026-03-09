-- STEP 1: Create dataset and upload data

CREATE DATABASE finance_dataset;

USE finance_dataset;
-- NOTE: Data was uploaded from CSV using Python (pandas)


-- STEP 2: Overview data

DESCRIBE finance_data; -- check dataset structure and column data types

SELECT * 
FROM finance_data
LIMIT 5; -- quick preview to ensure data was loaded correctly


-- STEP 3: Gender distribution (used later for pie chart)

SELECT 
    COUNT(*) AS total_questioned,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS total_males,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS total_females,
    COUNT(CASE WHEN gender IS NULL THEN 1 END) AS total_missing_gender
FROM finance_data;
-- Note: no missing responses were found in the dataset


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
