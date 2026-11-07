# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

The cost-tag check uses each Terraform resource's `address` as its idempotency key. If the
same address appears more than once in a plan, it is reported only once. For an unchanged
plan, the resource order, addresses, actions, and tags are unchanged, so the check produces
the same output and exit code on every run; it keeps no state between runs.

## Any other decision with a non-obvious alternative

For screening-report access, the authorization boundary is the landlord account: resolve the
report's tenant and property, then compare the property's `landlord_account_id` with the
Property Manager's. Missing tenant or property data fails closed.
