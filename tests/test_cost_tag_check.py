"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export). The fixture also has a "no-op"
     entry and a "delete" entry with no `after` block at all — neither should appear in the
     output or crash the check.
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

check_plan() takes a file path, not a dict — for a case that needs its own plan contents
instead of the shared fixture, write one with pytest's `tmp_path` rather than editing
fixtures/plan.json. You don't need to shell out to the real script for every case.
"""
from scripts.cost_tag_check import check_plan


def test_fixture_flags_resources_missing_billing_unit_tag(capsys):
    result = check_plan("fixtures/plan.json")

    assert result == 1
    assert capsys.readouterr().out.splitlines() == [
        "Missing landlord_account_id tag: aws_s3_bucket.listing_media",
        "Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync",
    ]


def test_check_is_idempotent(capsys):
    first_result = check_plan("fixtures/plan.json")
    first_output = capsys.readouterr().out
    second_result = check_plan("fixtures/plan.json")
    second_output = capsys.readouterr().out

    assert (first_result, first_output) == (second_result, second_output)


def test_create_and_update_require_nonempty_landlord_account_tag(tmp_path, capsys):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
        """{
          "resource_changes": [
            {
              "address": "aws_s3_bucket.empty_tag",
              "change": {
                "actions": ["create"],
                "after": {"tags": {"landlord_account_id": " "}}
              }
            },
            {
              "address": "aws_lambda_function.updated",
              "change": {
                "actions": ["update"],
                "after": {"tags": {"landlord_account_id": "la-001"}}
              }
            },
            {
              "address": "aws_s3_bucket.replaced",
              "change": {
                "actions": ["delete", "create"],
                "after": {"tags": {"tenant_id": "ten-001"}}
              }
            },
            {
              "address": "aws_s3_bucket.deleted",
              "change": {
                "actions": ["delete"],
                "after": null
              }
            }
          ]
        }""",
        encoding="utf-8",
    )

    assert check_plan(str(plan_path)) == 1
    assert capsys.readouterr().out.splitlines() == [
        "Missing landlord_account_id tag: aws_s3_bucket.empty_tag",
        "Missing landlord_account_id tag: aws_s3_bucket.replaced",
    ]


def test_passes_when_created_and_updated_resources_have_billing_tag(tmp_path, capsys):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
        """{
          "resource_changes": [
            {
              "address": "aws_s3_bucket.media",
              "change": {
                "actions": ["create"],
                "after": {"tags": {"landlord_account_id": "la-001", "tenant_id": "ten-001"}}
              }
            },
            {
              "address": "aws_lambda_function.export",
              "change": {
                "actions": ["update"],
                "after": {"tags": {"landlord_account_id": "la-002"}}
              }
            }
          ]
        }""",
        encoding="utf-8",
    )

    assert check_plan(str(plan_path)) == 0
    assert capsys.readouterr().out == ""
