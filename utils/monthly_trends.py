from collections import defaultdict
from datetime import datetime

from utils.calculations import to_number


def get_monthly_trends(savings):

    monthly = defaultdict(lambda: {
        "Savings": 0,
        "Loan Disbursed": 0,
        "Loan Repaid": 0
    })

    for record in savings:

        date = record.get("reporting_date")

        if not date:
            continue

        try:
            month = datetime.strptime(
                date,
                "%Y-%m-%d"
            ).strftime("%b %Y")

        except:
            continue

        monthly[month]["Savings"] += to_number(
            record.get("lf_section/total_savings")
        )

        monthly[month]["Loan Disbursed"] += to_number(
            record.get("ld_dis_act/total_loans_given")
        )

        monthly[month]["Loan Repaid"] += to_number(
            record.get("repayments/total_repayments_made")
        )

    return dict(monthly)