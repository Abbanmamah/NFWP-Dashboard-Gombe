import math


def to_number(value):
    """Convert Kobo values to numbers safely."""
    if value is None or value == "":
        return 0

    try:
        num = float(value)

        if math.isnan(num):
            return 0

        return num

    except (ValueError, TypeError):
        return 0


def calculate_total_wags(records):
    """Calculate Total WAGs."""
    return len(records)


def calculate_total_members(records):
    """Calculate Total Members."""
    total_members = 0

    for record in records:
        members = record.get("mem_det/member_details", [])

        if isinstance(members, list):
            total_members += len(members)

    return total_members


def calculate_total_savings(records):
    """Calculate Total Savings Fund."""
    total = 0

    for record in records:
        total += to_number(record.get("lf_section/total_savings"))

    return total


def calculate_total_loan_fund(records):
    """Calculate Total Loan Fund."""
    total = 0

    for record in records:
        total += to_number(record.get("lf_section/tlfc"))

    return total


def calculate_total_loan_disbursed(records):
    """Calculate Total Loan Disbursed."""
    total = 0

    for record in records:
        total += to_number(record.get("ld_dis_act/total_loans_given"))

    return total


def calculate_total_loan_repaid(records):
    """Calculate Total Loan Repaid."""
    total = 0

    for record in records:
        total += to_number(record.get("repayments/total_repayments_made"))

    return total


def calculate_outstanding_loan(records):
    """Outstanding Loan = Loan Disbursed - Loan Repaid"""
    return (
        calculate_total_loan_disbursed(records)
        - calculate_total_loan_repaid(records)
    )


def calculate_average_loan_utilisation(records):
    """Average Loan Utilisation (%)"""
    total = 0
    count = 0

    for record in records:
        value = to_number(
            record.get("begin_group_L6KqAQmFs/lur")
        )

        if value > 0:
            total += value
            count += 1

    if count == 0:
        return 0

    return total / count