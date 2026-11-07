# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

The cost-tag check uses each Terraform resource's exact `address` as its idempotency key
when deduplicating missing-tag findings. A repeated address is reported only once, and
findings are printed in plan order. On an unchanged plan, the resource addresses, actions,
and tags are unchanged, so the output and exit code are identical on every run; the script
does not persist state between runs.

## Any other decision with a non-obvious alternative

For screening-report access, the authorization boundary is the landlord account, not the
tenant ID. The check resolves the report's tenant and property, then compares the property's
`landlord_account_id` with the Property Manager's. An alternative would be to authorize
against a tenant-supplied or report-supplied account ID, but those are not the ownership
relationship established by the domain model. Missing or ambiguous tenant/property records
fail closed (deny access) rather than raising or granting access, because this is a sensitive
report and ownership cannot be established safely.

The cost-tag check validates only resources with a `create` or `update` action; it ignores
deletes and no-ops because they do not create or change the resource's resulting tags. It
requires a non-empty `landlord_account_id` value, rather than merely the presence of the key,
so a blank tag cannot pass as a valid billing-unit identifier.
