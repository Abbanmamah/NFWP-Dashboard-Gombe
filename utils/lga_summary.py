from collections import defaultdict
from utils.calculations import to_number


def get_lga_summary(membership, savings):

    summary = defaultdict(lambda: {
        "WAGs": 0,
        "Members": 0,
        "Savings": 0,
        "Loan Fund": 0,
        "Loan Disbursed": 0,
        "Loan Repaid": 0,
        "Average Loan Utilisation": 0,
    })

    counts = defaultdict(int)

    # =========================
    # MEMBERSHIP
    # =========================

    for record in membership:

        lga = record.get("location_details/lga", "Unknown")

        summary[lga]["WAGs"] += 1

        members = record.get("mem_det/member_details", [])

        if isinstance(members, list):
            summary[lga]["Members"] += len(members)

    # =========================
    # SAVINGS
    # =========================

    for record in savings:

        lga = record.get("location_details/lga", "Unknown")

        savings_amt = to_number(
            record.get("lf_section/total_savings")
        )

        loan_fund = to_number(
            record.get("lf_section/tlfc")
        )

        loan_disbursed = to_number(
            record.get("ld_dis_act/total_loans_given")
        )

        loan_repaid = to_number(
            record.get("repayments/total_repayments_made")
        )

        summary[lga]["Savings"] += savings_amt
        summary[lga]["Loan Fund"] += loan_fund
        summary[lga]["Loan Disbursed"] += loan_disbursed
        summary[lga]["Loan Repaid"] += loan_repaid

        # Calculate utilisation ourselves
        if loan_fund > 0:
            utilisation = (loan_disbursed / loan_fund) * 100

            summary[lga]["Average Loan Utilisation"] += utilisation
            counts[lga] += 1

    # =========================
    # AVERAGE UTILISATION
    # =========================

    for lga in summary:

        if counts[lga] > 0:
            summary[lga]["Average Loan Utilisation"] = round(
                summary[lga]["Average Loan Utilisation"] / counts[lga],
                1
            )

    return dict(summary)