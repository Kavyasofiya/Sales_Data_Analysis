import pandas as pd

df = pd.read_csv("dataset/superstore.csv")

print("SALES DATA SUMMARY")
print("------------------")
print("Total Revenue:", df["Sales"].sum())
print("Total Profit:", df["Profit"].sum())
print("Total Orders:", df["Order_ID"].nunique())
print("\nRevenue by Category:")
print(df.groupby("Category")["Sales"].sum())
print("\nRevenue by Region:")
print(df.groupby("Region")["Sales"].sum())
