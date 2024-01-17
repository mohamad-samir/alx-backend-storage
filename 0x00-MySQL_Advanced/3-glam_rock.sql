--  lists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name,
       IFNULL(2022 - formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
