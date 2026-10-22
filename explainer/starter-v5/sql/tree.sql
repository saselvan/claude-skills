WITH RECURSIVE walk(depth, frontier, seen) AS (
  SELECT 0, ARRAY[CAST(%(start_node_id)s AS text)], ARRAY[CAST(%(start_node_id)s AS text)]
  UNION ALL
  SELECT w.depth + 1, n.frontier, w.seen || n.frontier
  FROM walk w CROSS JOIN LATERAL (
    SELECT array_agg(k.node_id) AS frontier FROM (
      SELECT c.node_id FROM (
        SELECT DISTINCT e.dst_node_id AS node_id
        FROM served.edges_view e
        WHERE e.src_node_id = ANY(w.frontier)
          AND NOT (e.dst_node_id = ANY(w.seen))
      ) c
      
      ORDER BY c.node_id COLLATE "C"
      LIMIT 25
    ) k
  ) n
  WHERE w.depth < 3 AND n.frontier IS NOT NULL
),
reached AS (SELECT u.node_id, w.depth FROM walk w CROSS JOIN LATERAL unnest(w.frontier) AS u(node_id) WHERE w.depth > 0)
SELECT t.node_id, t.depth, NULL::double precision AS score
FROM reached t

ORDER BY t.depth, t.node_id COLLATE "C"
LIMIT 25
