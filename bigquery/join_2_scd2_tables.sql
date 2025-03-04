WITH d1 AS (
    SELECT 1 AS id, 'D1-A' AS value, CAST('2025-01-01 00:00:00' AS TIMESTAMP) AS eff_from, CAST('2025-02-01 23:59:59.999999'AS TIMESTAMP) AS eff_to
    UNION ALL
    SELECT 1, 'D1-B', CAST('2025-02-01 00:00:00' AS TIMESTAMP), CAST('9999-12-12 23:59:59.999999'AS TIMESTAMP)
)
, d2 AS (
    SELECT 1 AS id, 'D2-A' AS value, CAST('2025-01-15 00:00:00' AS TIMESTAMP) AS eff_from, CAST('2025-02-15 23:59:59.999999'AS TIMESTAMP) AS eff_to
    UNION ALL
    SELECT 1, 'D2-B', CAST('2025-02-16 00:00:00' AS TIMESTAMP), CAST('2025-03-15 23:59:59.999999'AS TIMESTAMP)
    UNION ALL
    SELECT 1, 'D2-C', CAST('2025-03-16 00:00:00' AS TIMESTAMP), CAST('9999-12-12 23:59:59.999999'AS TIMESTAMP)
)
, eff_from_union AS (
	SELECT DISTINCT 
		id, eff_from
	FROM d1
	UNION DISTINCT
	SELECT DISTINCT
		id, eff_from
	FROM d2
)
, date_range AS (
	SELECT 
		efu.id
		, efu.eff_from
		, COALESCE(
			DATE_ADD(LEAD(efu.eff_from) OVER (PARTITION BY efu.id ORDER BY efu.eff_from), INTERVAL -1 MICROSECOND)
			, CAST('9999-12-12 23:59:59.999999'AS TIMESTAMP)
		) AS eff_to
	FROM eff_from_union efu
)
--SELECT * FROM date_range;
SELECT
	dr.*
	, d1.value
	, d2.value
FROM date_range dr
LEFT JOIN d1 
	ON d1.id = dr.id
	AND d1.eff_from <= dr.eff_from AND d1.eff_to >= dr.eff_to
LEFT JOIN d2
	ON d2.id = dr.id
	AND d2.eff_from <= dr.eff_from AND d2.eff_to >= dr.eff_to
;