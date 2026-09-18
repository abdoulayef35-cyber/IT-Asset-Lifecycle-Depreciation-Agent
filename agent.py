import json
from anthropic import Anthropic

from dotenv import load_dotenv
load_dotenv()

from depreciation import load_assets, calculate_schedule
from lifecycle_flags import get_lifecycle_flags
from reconciliation import reconcile

client = Anthropic()

tools = [
    {
        "name": "get_depreciation_schedule",
        "description": "Get the full year-by-year depreciation schedule for one asset, given its asset ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The asset ID to look up, e.g. '000-6'.",
                }
            },
            "required": ["asset_id"],
        },
    },
    {
        "name": "get_lifecycle_alerts",
        "description": "Get all assets that are past or nearing end-of-useful-life or warranty expiration.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_reconciliation_findings",
        "description": "Compare the asset register against the physical count. Returns ghost assets (on the books but not found) and unrecorded assets (found but not on the books).",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "save_report",
        "description": "Save the final written findings report as a markdown file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The full markdown content of the report.",
                }
            },
            "required": ["content"],
        },
    },
]

import os
import json
from datetime import datetime


def dispatch_tool(name, tool_input):
    if name == "get_depreciation_schedule":
        assets = load_assets("data/asset_register.csv")
        assets_by_id = {a["asset_id"]: a for a in assets}
        asset = assets_by_id.get(tool_input["asset_id"])
        if asset is None:
            return {"error": f"No asset found with ID {tool_input['asset_id']}"}
        return calculate_schedule(asset)

    elif name == "get_lifecycle_alerts":
        assets = load_assets("data/asset_register.csv")
        alerts = []
        for asset in assets:
            flags = get_lifecycle_flags(asset)
            if flags["eol_status"] != "active" or flags["warranty_status"] != "active":
                alerts.append(flags)
        return alerts

    elif name == "get_reconciliation_findings":
        register_assets = load_assets("data/asset_register.csv")
        count_assets = load_assets("data/physical_count.csv")
        return reconcile(register_assets, count_assets)

    elif name == "save_report":
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/findings_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tool_input["content"])
        return {"status": "saved", "filename": filename}

    else:
        return {"error": f"Unknown tool: {name}"}


SYSTEM_PROMPT = """You are an IT asset lifecycle and depreciation audit agent.
You have tools to look up depreciation schedules, end-of-life/warranty alerts,
and physical inventory reconciliation findings for a company's hardware assets.

When asked for a findings report, first gather the relevant data using your
tools, then write a clear markdown report summarizing what you found -
call out assets nearing or past end-of-life, expired or soon-to-expire
warranties, and any reconciliation discrepancies with their dollar impact.
Once written, save the report using the save_report tool."""


def run(user_message):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(block.text for block in response.content if block.type == "text")

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = dispatch_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, default=str),
                })

        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    result = run("Give me a full findings report on our IT asset lifecycle, depreciation, and reconciliation status.")
    print(result)