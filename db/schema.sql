-- =========================
-- DIMENSION TABLES
-- =========================

-- ex entyr 
-- symbol,asset_name,asset_type,currency
-- AAPL,Apple Inc,Stock,usd
CREATE TABLE dim_asset (
  asset_id SERIAL PRIMARY KEY,
  symbol VARCHAR(10) NOT NULL UNIQUE,
  asset_name TEXT,
  asset_type VARCHAR(20) NOT NULL
    CHECK (asset_type IN ('stock', 'etf', 'crypto')),
  currency VARCHAR(3) NOT NULL
);

CREATE TABLE dim_date (
  date_id INTEGER PRIMARY KEY,      -- YYYYMMDD
  date DATE NOT NULL UNIQUE,
  year INTEGER NOT NULL,
  quarter INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  day_of_week INTEGER NOT NULL,
  is_trading_day BOOLEAN NOT NULL
);

CREATE TABLE dim_portfolio (
  portfolio_id SERIAL PRIMARY KEY,
  portfolio_name TEXT NOT NULL,
  owner TEXT,
  base_currency VARCHAR(3) NOT NULL
);

-- =========================
-- FACT TABLES
-- =========================

CREATE TABLE fact_prices (
  date_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  open_price NUMERIC(12,4),
  high_price NUMERIC(12,4),
  low_price NUMERIC(12,4),
  close_price NUMERIC(12,4),
  volume BIGINT,

  PRIMARY KEY (date_id, asset_id),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id)
);

CREATE TABLE fact_trades (
  trade_id SERIAL PRIMARY KEY,
  portfolio_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  trade_time TIMESTAMP NOT NULL,
  quantity NUMERIC(12,4) NOT NULL,
  price NUMERIC(12,4) NOT NULL,
  side VARCHAR(4) NOT NULL
    CHECK (side IN ('BUY', 'SELL')),

  FOREIGN KEY (portfolio_id) REFERENCES dim_portfolio(portfolio_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id)
);

CREATE TABLE fact_positions (
  date_id INTEGER NOT NULL,
  portfolio_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  quantity NUMERIC(14,4),
  market_value NUMERIC(14,4),

  PRIMARY KEY (date_id, portfolio_id, asset_id),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (portfolio_id) REFERENCES dim_portfolio(portfolio_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id)
);
