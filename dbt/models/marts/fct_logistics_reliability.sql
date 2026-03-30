{{ config(materialized='table') }}

SELECT 
    callsign,
    destination,
    -- Metric 1: Average Duration for your bar chart
    AVG(DATETIME_DIFF(arrival_time, departure_time, MINUTE)) as avg_flight_duration,
    -- Metric 2: Count of flights for volume tracking
    COUNT(*) as total_flights,
    -- Metric 3: Reliability flag
    CASE 
        WHEN AVG(DATETIME_DIFF(arrival_time, departure_time, MINUTE)) > 240 THEN 'Delayed'
        ELSE 'On-Time'
    END as reliability_status
FROM {{ ref('stg_arrivals') }}
GROUP BY 1, 2