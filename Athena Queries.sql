-- Count total patient records

SELECT COUNT(*) AS total_patients
FROM patient_recovery_curated;

-- Average recovery days by city

SELECT city, AVG(recovery_days) AS avg_recovery
FROM patient_recovery_curated
GROUP BY city
ORDER BY avg_recovery DESC;

-- Average recovery days by age group

SELECT 
    CASE 
        WHEN age BETWEEN 18 AND 30 THEN '18-30'
        WHEN age BETWEEN 31 AND 45 THEN '31-45'
        WHEN age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS age_group,
    AVG(recovery_days) AS avg_recovery
FROM patient_recovery_curated
GROUP BY age_group
ORDER BY avg_recovery;

-- Recovery by diabetes status

SELECT 
    CASE WHEN diabetes = 1 THEN 'Diabetic' ELSE 'Non-Diabetic' END AS diabetes_status,
    AVG(recovery_days) AS avg_recovery,
    COUNT(*) AS patient_count
FROM patient_recovery_curated
GROUP BY diabetes_status;

--Top 5 hospitals with longest average recovery

SELECT hospital, AVG(recovery_days) AS avg_recovery
FROM patient_recovery_curated
GROUP BY hospital
ORDER BY avg_recovery DESC
LIMIT 5;

-- Surgery type vs outcomes

SELECT surgery_type, outcome, COUNT(*) AS patient_count
FROM patient_recovery_curated
GROUP BY surgery_type, outcome
ORDER BY surgery_type, patient_count DESC;

-- City-wise diabetes impact

SELECT city,
       CASE WHEN diabetes = 1 THEN 'Diabetic' ELSE 'Non-Diabetic' END AS diabetes_status,
       AVG(recovery_days) AS avg_recovery
FROM patient_recovery_curated
GROUP BY city, diabetes_status
ORDER BY city, diabetes_status;