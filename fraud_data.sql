CREATE TABLE fraud_data (
    transdatetranstime TIMESTAMP,
    merchant VARCHAR(255),
    category VARCHAR(255),
    amt NUMERIC,
    city VARCHAR(255),
    state VARCHAR(255),
    lat NUMERIC,
    long NUMERIC,
    citypop INTEGER,
    job VARCHAR(255),
    dob DATE,
    transnum VARCHAR(255),
    merchlat NUMERIC,
    merchlong NUMERIC,
    isfraud INTEGER
);

#sample questions:
#how many category are there in the fraud_data?
SELECT COUNT(category) FROM fraud_data;

#What is the total amt  grouped by state in the fraud_data ?
SELECT state, SUM(amt) AS total_amt FROM fraud_data GROUP BY state;

#How many fraudulent transactions (isfraud = 1) are there in each city in the fraud_data dataset?
SELECT city, COUNT(*) AS num_fraudulent_transactions FROM fraud_data WHERE isfraud = 1 GROUP BY city;

#How many transactions occurred in the fraud_data where the category is 'health_fitness' and the amt is greater than 100?
SELECT COUNT(*) FROM fraud_data WHERE category = 'grocery_pos' AND amt > 100;