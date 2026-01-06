SELECT
    date_id, 
    asset_id, 
    close_price,
    -- = adding closing price from previous day
    LAG(close_price) OVER (PARTITION BY asset_id ORDER BY date_id) AS prev_close,
    -- = calculating for daily return
    (close_price - LAG(close_price) OVER (PARTITION BY asset_id ORDER BY date_id)) 
        / LAG(close_price) OVER (PARTITION BY asset_id ORDER BY date_id) as daily_return
FROM
    fact_prices
ORDER BY
    asset_id, date_id
