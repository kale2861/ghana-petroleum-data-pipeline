-- =====================================================
-- Ghana Petroleum Analytics SQL Queries
-- =====================================================

-- =====================================================
-- 1. FULL DATASET
-- =====================================================

SELECT *
FROM petroleum_analytics
ORDER BY year;

-- =====================================================
-- 2. HIGHEST REVENUE YEARS
-- =====================================================

SELECT
    year,
    ROUND(petroleum_revenue_usd / 1000000, 2)
        AS revenue_millions
FROM petroleum_analytics
ORDER BY petroleum_revenue_usd DESC;

-- =====================================================
-- 3. HIGHEST PRODUCTION YEARS
-- =====================================================

SELECT
    year,
    ROUND(total_production_barrels / 1000000, 2)
        AS production_million_barrels
FROM petroleum_analytics
ORDER BY total_production_barrels DESC;

-- =====================================================
-- 4. YEAR-OVER-YEAR REVENUE CHANGE
-- =====================================================

SELECT
    year,

    ROUND(
        petroleum_revenue_usd / 1000000,
        2
    ) AS revenue_millions,

    ROUND(
        petroleum_revenue_usd
        - LAG(petroleum_revenue_usd)
            OVER (ORDER BY year),
        2
    ) AS revenue_change
FROM petroleum_analytics
ORDER BY year;