"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or updated (skip anything whose change.actions
    isn't "create" or "update" — a "no-op"/"read" change, or a "delete" with no `after`
    block at all).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail. This is about a single run being
    stable and repeatable — it does not require remembering anything between runs.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Returns an exit code: 0 if every resource being created or updated has
    `landlord_account_id`, non-zero otherwise.
    """
    with open(plan_path, encoding="utf-8") as plan_file:
        plan = json.load(plan_file)

    missing_addresses = []
    seen_addresses = set()
    for resource in plan["resource_changes"]:
        change = resource["change"]
        actions = change["actions"]
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after")
        tags = after.get("tags") if isinstance(after, dict) else None
        landlord_account_id = (
            tags.get("landlord_account_id") if isinstance(tags, dict) else None
        )
        if not isinstance(landlord_account_id, str) or not landlord_account_id.strip():
            address = resource["address"]
            if address not in seen_addresses:
                missing_addresses.append(address)
                seen_addresses.add(address)

    for address in missing_addresses:
        print(f"Missing landlord_account_id tag: {address}")

    return 1 if missing_addresses else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
