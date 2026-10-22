WITH hop0 AS (SELECT CAST(%(start_node_id)s AS text) AS node_id),
hop1 AS (
  SELECT c.node_id, c.support, NULL::double precision AS score
  FROM (SELECT e.dst_node_id AS node_id, COUNT(*) AS support
        FROM served.edges_view e JOIN hop0 f ON e.src_node_id = f.node_id
        WHERE e.dst_node_id NOT IN (SELECT node_id FROM hop0)
        GROUP BY e.dst_node_id ) c
  
  ORDER BY c.support DESC, c.node_id COLLATE "C"
  LIMIT 25),
hop2 AS (
  SELECT c.node_id, c.support, NULL::double precision AS score
  FROM (SELECT e.dst_node_id AS node_id, COUNT(*) AS support
        FROM served.edges_view e JOIN hop1 f ON e.src_node_id = f.node_id
        WHERE e.dst_node_id NOT IN (SELECT node_id FROM hop0 UNION ALL SELECT node_id FROM hop1)
        GROUP BY e.dst_node_id ) c
  
  ORDER BY c.support DESC, c.node_id COLLATE "C"
  LIMIT 25),
hop3 AS (
  SELECT c.node_id, c.support, NULL::double precision AS score
  FROM (SELECT e.dst_node_id AS node_id, COUNT(*) AS support
        FROM served.edges_view e JOIN hop2 f ON e.src_node_id = f.node_id
        WHERE e.dst_node_id NOT IN (SELECT node_id FROM hop0 UNION ALL SELECT node_id FROM hop1 UNION ALL SELECT node_id FROM hop2)
        GROUP BY e.dst_node_id ) c
  
  ORDER BY c.support DESC, c.node_id COLLATE "C"
  LIMIT 25),
hop4 AS (
  SELECT c.node_id, c.support, NULL::double precision AS score
  FROM (SELECT e.dst_node_id AS node_id, COUNT(*) AS support
        FROM served.edges_view e JOIN hop3 f ON e.src_node_id = f.node_id
        WHERE e.dst_node_id NOT IN (SELECT node_id FROM hop0 UNION ALL SELECT node_id FROM hop1 UNION ALL SELECT node_id FROM hop2 UNION ALL SELECT node_id FROM hop3)
        GROUP BY e.dst_node_id ) c
  
  ORDER BY c.support DESC, c.node_id COLLATE "C"
  LIMIT 25)
SELECT * FROM (
SELECT 1 AS hop, node_id, support, score FROM hop1
UNION ALL
SELECT 2 AS hop, node_id, support, score FROM hop2
UNION ALL
SELECT 3 AS hop, node_id, support, score FROM hop3
UNION ALL
SELECT 4 AS hop, node_id, support, score FROM hop4
) w
ORDER BY hop, support DESC, node_id COLLATE "C"
