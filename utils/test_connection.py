from utils.data_loader import load_membership_data, load_savings_data

membership = load_membership_data()
savings = load_savings_data()

print("=" * 60)
print("DATA LOADER TEST")
print("=" * 60)

print(f"Membership Records : {len(membership)}")
print(f"Savings Records    : {len(savings)}")