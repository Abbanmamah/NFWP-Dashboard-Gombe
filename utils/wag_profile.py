from utils.calculations import to_number


def get_wag_profile(search, membership, savings):
    """
    Search a WAG by either WAG ID or WAG Name.
    """

    search = search.strip().lower()

    member = None

    # -------------------------------------
    # Search Membership Data
    # -------------------------------------

    for record in membership:

        wag_id = str(
            record.get("location_details/wagid", "")
        ).strip().lower()

        if wag_id == search:
            member = record
            break

    saving = None

    # -------------------------------------
    # Search Savings Data
    # -------------------------------------

    for record in savings:

        wag_id = str(
            record.get("location_details/wag_id", "")
        ).strip().lower()

        wag_name = str(
            record.get("location_details/wagname", "")
        ).strip().lower()

        if wag_id == search or wag_name == search:

            saving = record

            if member is None:

                member = next(
                    (
                        m for m in membership
                        if m.get("location_details/wagid", "").strip().lower()
                        == wag_id
                    ),
                    None,
                )

            break

    if member is None:
        return None

    members = member.get("mem_det/member_details", [])

    if not isinstance(members, list):
        members = []

    profile = {
        "WAG ID": member.get("location_details/wagid", ""),
        "WAG Name": saving.get("location_details/wagname", "N/A") if saving else "N/A",
        "LGA": member.get("location_details/lga", ""),
        "Ward": member.get("location_details/ward", ""),
        "Community": member.get("location_details/community", ""),
        "Ward Facilitator": member.get("wfname", ""),
        "Members": len(members),
        "Savings": to_number(
            saving.get("lf_section/total_savings")
        ) if saving else 0,
        "Loan Fund": to_number(
            saving.get("lf_section/tlfc")
        ) if saving else 0,
        "Loan Disbursed": to_number(
            saving.get("ld_dis_act/total_loans_given")
        ) if saving else 0,
        "Loan Repaid": to_number(
            saving.get("repayments/total_repayments_made")
        ) if saving else 0,
        "Average Loan Utilisation": to_number(
            saving.get("begin_group_L6KqAQmFs/lur")
        ) if saving else 0,
    }

    return profile