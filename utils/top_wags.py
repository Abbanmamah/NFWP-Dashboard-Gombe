from utils.calculations import to_number


def get_top_wags(savings, top=True):

    rows = []

    for record in savings:

        rows.append({

            "WAG Name": record.get("location_details/wagname", ""),

            "WAG ID": record.get("location_details/wag_id", ""),

            "Ward": record.get("location_details/ward", ""),

            "Savings": to_number(
                record.get("lf_section/total_savings")
            ),

            "Loan Fund": to_number(
                record.get("lf_section/tlfc")
            ),

            "Loan Disbursed": to_number(
                record.get("ld_dis_act/total_loans_given")
            ),

            "Loan Repaid": to_number(
                record.get("repayments/total_repayments_made")
            ),

            "Loan Utilisation (%)": to_number(
                record.get("begin_group_L6KqAQmFs/lur")
            )

        })

    rows = sorted(
        rows,
        key=lambda x: x["Savings"],
        reverse=top
    )

    return rows[:10]