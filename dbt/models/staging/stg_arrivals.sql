SELECT
    icao24,
    TIMESTAMP_SECONDS(firstSeen) as departure_time,
    TIMESTAMP_SECONDS(lastSeen) as arrival_time,
    estArrivalAirport as destination,
    callsign
FROM {{ source('raw_data', 'arrivals') }}
WHERE callsign IS NOT NULL