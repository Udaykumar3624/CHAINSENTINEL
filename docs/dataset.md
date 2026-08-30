# 📊 ChainSentinel CSV Dataset Schema Documentation (SIH26146)

This document defines the schema, field types, validation constraints, and behavioral scenario annotations for Bitcoin transaction datasets processed by ChainSentinel.

---

## 📋 CSV Field Definitions & Constraints

| Field Name | Type | Constraint | Example | Description |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | `String` | Required, Unique | `e3b0c44298fc...` | 64-character SHA-256 transaction hash or unique row identifier (`tx_001`). |
| `timestamp` | `String (ISO 8601)` | Required | `2026-08-30T12:00:00Z` | UTC timestamp of block inclusion or transaction broadcast. |
| `input_address` | `String` | Required | `bc1q9x087v2n5k4...` | Primary sending Bitcoin address (Base58check or Bech32 format). |
| `output_address` | `String` | Required | `bc1qrapid83k92m...` | Primary receiving Bitcoin address. |
| `amount_btc` | `Float` | Required, $\ge 0.0$ | `12.5000` | Transferred transaction value in Bitcoin (BTC). |
| `input_count` | `Integer` | Required, $\ge 1$ | `1` | Total count of input UTXOs consumed in the transaction. |
| `output_count` | `Integer` | Required, $\ge 1$ | `2` | Total count of output UTXOs created (e.g. recipient output + change output). |
| `transaction_size` | `Integer` | Optional, $\ge 100$ | `225` | Estimated transaction size in bytes (vBytes). |
| `fee_btc` | `Float` | Optional, $\ge 0.0$ | `0.0005` | Transaction fee paid to miners in BTC. |
| `block_height` | `Integer` | Optional, $\ge 0$ | `895200` | Bitcoin block height index. |
| `time_to_next_transaction` | `Float` | Optional, $\ge 0.0$ | `83.0` | Elapsed delay in seconds before funds are forwarded from `output_address`. |
| `unique_counterparties` | `Integer` | Optional, $\ge 1$ | `14` | Distinct counterparties interacting with the address. |
| `scenario` | `String` | Required | `rapid_forwarding` | Ground-truth behavioral classification tag for benchmark evaluation. |
| `label` | `String` | Required | `suspicious` | Ground-truth risk classification (`normal` or `suspicious`). |

---

## 🎭 Supported Ground-Truth Behavioral Scenarios

1. **`normal`**: Standard retail / merchant transfers.
2. **`rapid_forwarding`**: Immediate relay of incoming funds within $<600$ seconds.
3. **`fan_out`**: 1 input splitting into $\ge 20$ small output payments (ransomware payout).
4. **`fan_in`**: $\ge 20$ input addresses consolidating into 1 destination wallet (mixer deposit).
5. **`peeling_chain`**: Sequential hop transfers peeling off micro amounts while forwarding remaining change.
6. **`circular_flow`**: Directed cycles ($A \to B \to C \to A$) creating artificial wash-trading volume.
7. **`dormancy_burst`**: Address inactive for $>180$ days suddenly initiating high-volume transfers.
8. **`structuring`**: Rapid sequence of transfers just below typical reporting thresholds ($<0.1$ BTC).
9. **`risky_neighbor`**: 1-hop or 2-hop topological proximity to a known flagged cluster.

---

## 📋 Sample CSV Template

```csv
transaction_id,timestamp,input_address,output_address,amount_btc,input_count,output_count,transaction_size,fee_btc,block_height,time_to_next_transaction,unique_counterparties,scenario,label
tx_001,2026-08-30T10:00:00Z,bc1qnormal001,bc1qnormal002,0.5000,1,2,225,0.0005,895200,3600.0,2,normal,normal
tx_002,2026-08-30T10:05:00Z,bc1qrapid83k,bc1qrapid84m,15.2000,1,2,225,0.0005,895201,83.0,14,rapid_forwarding,suspicious
tx_003,2026-08-30T10:10:00Z,bc1qpeel001,bc1qpeel002,8.4000,1,2,225,0.0005,895202,120.0,8,peeling_chain,suspicious
tx_004,2026-08-30T10:15:00Z,bc1qcycle001,bc1qcycle002,5.0000,1,1,200,0.0005,895203,90.0,4,circular_flow,suspicious
```
