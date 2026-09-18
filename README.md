# IT Asset Lifecycle & Depreciation Agent

A Python + Claude API agent that manages the full lifecycle of IT hardware assets: it calculates depreciation schedules, flags assets approaching or past end-of-life or warranty expiration, reconciles the asset register against a physical inventory count, and writes a full findings report — all driven by an LLM agent calling real Python functions as tools rather than guessing at the numbers itself.

Built as a second portfolio project alongside [grc-audit-agent](https://github.com/abdoulayef35-cyber/grc-audit-agent), applying the same agentic pattern to a hardware asset management / fixed-asset accounting domain instead of IT audit.

## What it does

- **Depreciation** (`depreciation.py`) — computes a straight-line depreciation schedule for any asset, correctly handling fractional useful-life years (e.g. 3.5 years), and can compute an asset's book value as of any specific date rather than only at year-end.
- **Lifecycle & warranty flagging** (`lifecycle_flags.py`) — flags assets that are past or approaching end-of-useful-life and/or warranty expiration, tracking the two independently (an asset can be past warranty but still within its useful life, or the reverse).
- **Reconciliation** (`reconciliation.py`) — compares the asset register against a physical inventory count to surface "ghost" assets (on the books, not found) and "unrecorded" assets (found, not on the books), with the current book value at risk for each ghost asset.
- **Agent** (`agent.py`) — a Claude API tool-use agent that calls the three modules above as tools, then writes and saves a full markdown findings report summarizing lifecycle risk, depreciation exposure, and reconciliation discrepancies with recommendations.

## Setup

1. Clone this repo.
2. Install dependencies:
   ```
   python -m pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
4. Run the agent:
   ```
   python agent.py
   ```

The report gets saved to `reports/` as a timestamped markdown file, and printed to the console. A sample run is included at `reports/sample_findings_report.md`.

## Sample data

`data/asset_register.csv` and `data/physical_count.csv` are synthetic data modeled on real AI/HPC data center hardware — NVIDIA GPU modules (H100, H200, A100), Arista switches, a PDU, and a server — with purchase dates and a physical count deliberately spread out to exercise every code path: assets already past end-of-life, one only days from end-of-life, assets with expired vs. active warranties independent of their EOL status, ghost assets, and unrecorded assets.

## A bug worth mentioning

The first version of `agent.py` had no direct way to get an asset's *current* book value — `calculate_schedule` only returns year-indexed rows, not a value tied to today's date. On the first real report run, the agent worked around that gap by guessing: it used an asset's salvage value as a stand-in for its remaining book value, which is only correct once an asset has actually reached the end of its schedule. For an asset that hadn't (000-14, still mid-schedule), this understated its book value by roughly $466 and led the agent to also misstate its lifecycle status.

Fix: added `get_book_value_as_of(asset, as_of_date=None)` to `depreciation.py`, which computes book value directly from elapsed time rather than stepping through a year-by-year list, and updated `reconciliation.py` to use it for ghost-asset valuations. Re-running confirmed the fix — a good example of why testing an agent's actual numeric output against hand-calculated values matters, rather than trusting a well-written report at face value.

## License

MIT — see [LICENSE](LICENSE).
