from collections import Counter


def get_data_quality(membership, savings):

    membership_ids = [
        r.get("location_details/wagid", "").strip()
        for r in membership
    ]

    savings_ids = [
        r.get("location_details/wag_id", "").strip()
        for r in savings
    ]

    membership_counter = Counter(membership_ids)
    savings_counter = Counter(savings_ids)

    duplicate_membership = sum(
        1 for x in membership_counter.values() if x > 1
    )

    duplicate_savings = sum(
        1 for x in savings_counter.values() if x > 1
    )

    membership_without_savings = len(
        set(membership_ids) - set(savings_ids)
    )

    savings_without_membership = len(
        set(savings_ids) - set(membership_ids)
    )

    missing_gps = sum(
        1 for r in membership
        if not r.get("location_details/gps_location")
    )

    missing_ward = sum(
        1 for r in membership
        if not r.get("location_details/ward")
    )

    missing_community = sum(
        1 for r in membership
        if not r.get("location_details/community")
    )

    zero_members = 0

    for r in membership:

        members = r.get("mem_det/member_details", [])

        if not isinstance(members, list) or len(members) == 0:
            zero_members += 1

    return {

        "Membership Records": len(membership),

        "Savings Records": len(savings),

        "Membership without Savings": membership_without_savings,

        "Savings without Membership": savings_without_membership,

        "Duplicate Membership IDs": duplicate_membership,

        "Duplicate Savings IDs": duplicate_savings,

        "Missing GPS": missing_gps,

        "Missing Ward": missing_ward,

        "Missing Community": missing_community,

        "Zero Members": zero_members,

    }