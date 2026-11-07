"""
B2, part 1 — implement can_access_screening_report().

Read README.md's domain model first. A ScreeningReport belongs to a Tenant, a Tenant belongs to
a Property, and a Property belongs to a LandlordAccount. A PropertyManager is scoped to exactly
one LandlordAccount.

Work out from that hierarchy which boundary actually gates access to a ScreeningReport.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    actor: the PropertyManager requesting access
    report: the ScreeningReport they're trying to view
    properties: all known Property records
    tenants: all known Tenant records

    Return True if actor may view report, False otherwise. Fail closed — if anything needed to
    make this determination is missing (tenant not found, property not found), return False.
    """
    matching_tenants = [tenant for tenant in tenants if tenant.id == report.tenant_id]
    if len(matching_tenants) != 1:
        return False

    matching_properties = [
        prop for prop in properties if prop.id == matching_tenants[0].property_id
    ]
    if len(matching_properties) != 1:
        return False

    return actor.landlord_account_id == matching_properties[0].landlord_account_id
