--  lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
    band_name,
    IFNULL(
        FLOOR((DATEDIFF(
                    IFNULL(SUBSTRING_INDEX(SUBSTRING_INDEX(lifespan, ' - ', 1), '-', -1), '2022-01-01'),
                    IFNULL(SUBSTRING_INDEX(SUBSTRING_INDEX(lifespan, ' - ', -1), '-', -1), '2022-01-01')
                ) / 365)),
        0
    ) AS lifespan
FROM
    bands
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC,
    band_name;
