
# IT Asset Lifecycle, Depreciation & Reconciliation Findings Report

## Executive Summary

A review of the IT asset register against lifecycle/warranty data and the most recent physical inventory count identified **7 assets with lifecycle or warranty concerns**, **2 "ghost" assets** still on the books but not physically located (representing **$2,568.16** in book value at risk), and **2 unrecorded (untagged) high-value assets** found on-site but missing from the asset register. Several assets are already past their end-of-useful-life (EOL) date while still carrying active warranties or non-trivial book value, indicating a need for lifecycle policy review and register cleanup.

---

## 1. Lifecycle & Warranty Alerts

| Asset ID | EOL Date | EOL Status | Warranty End | Warranty Status |
|----------|----------|------------|--------------|------------------|
| 000-6  | 2025-11-06 | ⚠️ Past (316 days ago) | 2027-05-08 | Active (232 days left) |
| 000-7  | 2026-04-30 | ⚠️ Past (141 days ago) | 2027-10-30 | Active (407 days left) |
| 000-8  | 2026-08-23 | ⚠️ Past (26 days ago) | 2028-02-22 | Active (522 days left) |
| 000-11 | 2026-06-19 | ⚠️ Past (91 days ago) | 2026-06-19 | ❌ Expired (91 days ago) |
| 000-12 | 2026-09-27 | 🟡 Near (9 days out) | 2026-09-27 | 🟡 Near expiration (9 days out) |
| 000-14 | 2027-11-04 | ✅ Active (412 days left) | 2025-11-04 | ❌ Expired (318 days ago) |
| 000-15 | 2025-03-12 | ⚠️ Past (555 days ago) | 2025-03-12 | ❌ Expired (555 days ago) |

**Key observations:**
- **000-6, 000-7, 000-8, 000-11, and 000-15** are already past their end-of-useful-life dates, with 000-15 being the most severely overdue (555 days past EOL and warranty).
- **000-11 and 000-15** have both EOL and warranty status expired — these assets are unsupported and off official service life simultaneously, posing operational and support risk.
- **000-12** is approaching both EOL and warranty expiration within the next 9 days and should be flagged for imminent refresh/replacement planning.
- **000-14** has an active EOL runway (412 days) but its warranty already lapsed 318 days ago — meaning any hardware failure going forward is an out-of-pocket repair/replacement cost.

---

## 2. Depreciation Summary

Depreciation schedules were pulled for all flagged assets. Current book values (most recent recorded year) are:

| Asset ID | Schedule Length | Final/Current Book Value | Notes |
|----------|-----------------|---------------------------|-------|
| 000-6  | 4 yrs | $5,000.00 | Still carries meaningful book value despite being past EOL |
| 000-7  | 4 yrs | $5,000.00 | Same depreciation profile as 000-6; past EOL with residual value |
| 000-8  | 4 yrs | $9,000.00 | Highest remaining book value among past-EOL assets |
| 000-11 | 5 yrs | $1,298.00 | Nearly fully depreciated; EOL and warranty both expired |
| 000-12 | 5 yrs | $1,299.00 | Nearly fully depreciated; nearing EOL/warranty simultaneously |
| 000-14 | 7 yrs | $300.00 (final scheduled) / ~$768.16 (current, per reconciliation) | Ghost asset — see Section 3 |
| 000-15 | 5 yrs | $1,800.00 | Ghost asset — see Section 3 |

**Observation:** Assets 000-6, 000-7, and 000-8 are past their end-of-life dates yet still hold $5,000–$9,000 of undepreciated book value. This is a common source of balance sheet risk if these assets are retired, lost, or disposed of without a formal write-off — finance should confirm whether accelerated depreciation or impairment is warranted for hardware kept in service beyond its planned life.

---

## 3. Reconciliation Findings

Comparing the asset register to the physical inventory count revealed discrepancies in both directions:

### 3.1 Ghost Assets (on the books, not found in physical count)

| Asset ID | Description | Book Value at Risk |
|----------|--------------|--------------------|
| 000-15 | Dell PowerEdge R750 | $1,800.00 |
| 000-14 | Server Technology PRO2 | $768.16 |
| **Total** | | **$2,568.16** |

Both ghost assets are also flagged in the lifecycle alerts above (000-15 is past EOL/warranty; 000-14's warranty has expired). This suggests these units may have already been quietly decommissioned, lost, or stolen without an associated retirement entry — the $2,568.16 combined book value should be investigated for write-off or located and re-tagged.

### 3.2 Unrecorded Assets (found in physical count, not on the books)

| Asset ID (temp) | Description | Location | Count Date |
|------------------|--------------|----------|-------------|
| UNTAGGED-1 | NVIDIA HGX H200 80GB SXM5 | Shelf A5 | 2026-09-17 |
| UNTAGGED-2 | NVIDIA HGX A100 8-GPU BB | Shelf A2 | 2026-09-15 |

These are high-value GPU compute assets (NVIDIA HGX-class accelerators) sitting on shelves without any register entry, depreciation schedule, warranty tracking, or insurance coverage. Given the high unit cost of HGX H200/A100 systems, this represents a significant unrecorded capital asset exposure and a compliance/audit gap.

---

## 4. Financial Impact Summary

| Category | Impact |
|----------|--------|
| Ghost asset book value at risk | $2,568.16 |
| Unrecorded high-value GPU assets | Value unknown — not yet appraised/entered (material, given HGX H200/A100 replacement costs typically run five to six figures per unit) |
| Past-EOL assets still carrying book value (000-6, 000-7, 000-8) | $19,000.00 combined residual book value on hardware past its planned service life |
| Assets with lapsed warranty still in active use (000-11, 000-14, 000-15) | Ongoing unbudgeted repair/replacement risk |

---

## 5. Recommendations

1. **Investigate ghost assets 000-14 and 000-15 immediately** — confirm physical disposition, and either locate/re-tag them or process a formal write-off of the $2,568.16 book value.
2. **Onboard the two unrecorded NVIDIA HGX assets** into the asset register with proper acquisition cost, depreciation schedule, and warranty terms; verify how long they've been in service and whether this is a control gap in the intake process.
3. **Review retirement/replacement plans for 000-6, 000-7, and 000-8**, which are past EOL but still hold significant book value ($5,000–$9,000 each) — determine whether continued use is acceptable risk or whether refresh should be accelerated.
4. **Prioritize 000-12** for replacement planning, as both its EOL and warranty windows close within 9 days.
5. **Establish extended warranty or self-insurance coverage** for 000-11, 000-14, and 000-15, whose manufacturer warranties have already lapsed while the assets remain in service.
6. **Schedule more frequent physical-to-book reconciliations**, ideally quarterly for high-value compute assets (GPUs/servers), to catch ghost and unrecorded assets sooner.
