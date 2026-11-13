SELECT intent, COUNT(*) AS requests
FROM interaction
GROUP BY intent
ORDER BY requests DESC;


SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC;


SELECT i.topic, COUNT(*) AS thumbs_down
FROM interaction i
JOIN feedback f ON f.request_id = i.request_id
WHERE f.rating = -1
GROUP BY i.topic
ORDER BY thumbs_down DESC;