-- fixture walk
WITH hop1 AS (
  SELECT e.dst_node_id, COUNT(*) AS support
  FROM edges e
  GROUP BY e.dst_node_id
)
SELECT * FROM hop1;
