# Mempool.space API Integration & Fallback Architecture

## Overview
ChainSentinel provides an optional live data integration adapter with [Mempool.space](https://mempool.space/docs/api/rest) alongside its built-in offline deterministic Demo Engine (SIH26146).

---

## 1. Feature Flag Configuration
In `.env` or system environment variables:
```env
LIVE_DATA_ENABLED=false # Set to true to attempt live blockchain lookups
MEMPOOL_API_URL=https://mempool.space/api
REQUEST_TIMEOUT_SECONDS=5
```

---

## 2. Input Validation Rules
Before initiating any outbound HTTP requests, ChainSentinel validates inputs to prevent SSRF and waste:
- **Bitcoin Addresses**: Checked against regex `^(1...|3...|bc1q...|bc1p...)`.
- **Transaction IDs (TxID)**: Checked against 64-character hexadecimal regex `^[a-fA-F0-9]{64}$`.

---

## 3. Resilience & Fallback Guarantees
- **Timeout Policy**: 5.0 seconds per request with up to 2 retries and exponential backoff.
- **HTTP 429 Handling**: Automatically detects Mempool rate limits and suggests switching to Demo Mode.
- **No Silent Data Swapping**: ChainSentinel **NEVER** silently replaces a user's failed live query with unrelated demo data. If live lookup fails, a clear error prompt is shown with an explicit switch-to-demo option.

---

## 4. Responsible AI & Data Provenance
All responses contain a explicit `source` metadata field:
- `Live Mempool.space API`
- `Demo Mode (SIH26146)`
- `Uploaded CSV`
