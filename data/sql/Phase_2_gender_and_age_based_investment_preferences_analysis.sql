-- Step 1: Gender-based investment trends

-- % of respondents preferring investments and, specifically, investments in stock market
SELECT 
    gender,
    ROUND(100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*), 2
    ) AS Investment_Preference_Pct,
    ROUND(100 * COUNT(CASE WHEN Stock_Marktet = 'Yes' THEN 1 END) / COUNT(*), 2
    ) AS Stock_Market_Investment_Preference_Pct -- Note: used for plotting a bar char later
FROM finance_data
GROUP BY gender;


-- Step 2: Average investment preference rank by gender
-- Note: used to plot a bar chart later

SELECT 
    CONCAT(COUNT(*), ' Male') AS total_asked,

    -- % of Male respondents interested in investments
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,

    -- Average preference ranking for investment instruments
    AVG(Mutual_Funds) AS average_mutual_funds_preference_rank,
    AVG(Equity_Market) AS average_equity_market_preference_rank,
    AVG(Debentures) AS average_debentures_preference_rank,
    AVG(Government_Bonds) AS average_goverment_bonds_preference_rank,
    AVG(Fixed_Deposits) AS average_fixed_deposits_preference_rank,
    AVG(ppf) AS average_ppf_preference_rank,
    AVG(gold) AS average_gold_preference_rank

FROM finance_data
WHERE gender = 'Male'

UNION -- combine both genders for comparison

SELECT 
    CONCAT(COUNT(*), ' Female') AS total_asked,
    -- % of Female respondents interested in investments
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,

    -- Average preference ranking for investment instruments
    AVG(Mutual_Funds),
    AVG(Equity_Market),
    AVG(Debentures),
    AVG(Government_Bonds),
    AVG(Fixed_Deposits),
    AVG(ppf),
    AVG(gold)

FROM finance_data
WHERE gender = 'Female';



-- Step 3: Average investment preference rank by gender among young people (<= 25 y.o.)
-- Note: used to plot a bar chart later

SELECT 
    CONCAT(COUNT(*), ' Male') AS total_asked,

    -- % of Male respondents interested in investments
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,

    -- Average preference ranking for investment instruments
    AVG(Mutual_Funds),
    AVG(Equity_Market),
    AVG(Debentures),
    AVG(Government_Bonds),
    AVG(Fixed_Deposits),
    AVG(ppf),
    AVG(gold)

FROM finance_data
WHERE gender = 'Male'
AND age <= 25

UNION

SELECT 
    CONCAT(COUNT(*), ' Female') AS total_asked,

    -- % of Female respondents interested in investments
    100 * COUNT(CASE WHEN Investment_Avenues = 'Yes' THEN 1 END) / COUNT(*) AS investment_interest_pct,

    -- Average preference ranking for investment instruments
    AVG(Mutual_Funds),
    AVG(Equity_Market),
    AVG(Debentures),
    AVG(Government_Bonds),
    AVG(Fixed_Deposits),
    AVG(ppf),
    AVG(gold)

FROM finance_data
WHERE gender = 'Female'
AND age <= 25;
