import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_graph():
    location = "datasets/Customer_Purchasing_Behaviors.csv"
    df = pd.read_csv(location)

    destination = "static/graphs"
    os.makedirs(destination, exist_ok=True)

    sns.set_theme(style="whitegrid")

    # -------------------------------------------
    # 1. Scatter Plot: Income vs Purchase Amount
    # -------------------------------------------

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df,
        x='annual_income',
        y='purchase_amount',
        hue='loyalty_score',
        palette='viridis'
    )
    plt.title("Income vs Purchase Amount (colored by Loyalty Score)")
    plt.xlabel("Annual Income")
    plt.ylabel("Purchase Amount")
    plt.legend(title="Loyalty Score")
    plt.tight_layout()
    plt.savefig(os.path.join(destination, "income_vs_purchase.png"))
    plt.show()

    # -----------------------------------------------------
    # 2. Scatter Plot: Loyalty Score vs Purchase Frequency
    # -----------------------------------------------------

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df,
        x='loyalty_score',
        y='purchase_frequency',
        hue='region',
        palette='Dark2'
    )
    plt.title("Loyalty Score vs Purchase Frequency")
    plt.xlabel("Loyalty Score")
    plt.ylabel("Purchase Frequency")
    plt.legend(title="Region")
    plt.tight_layout()
    plt.savefig(os.path.join(destination, "loyalty_score_vs_purchase_frequency.png"))
    plt.show()

    # ------------------------------------------------------
    # 3. Bar Plot: Region-wise Average Spending by Age Group
    # -------------------------------------------------------

    if 'age_group' not in df.columns:
        df['age_group'] = pd.cut(
            df['age'],
            bins=[18, 25, 35, 45, 55, 65],
            right=False,
            labels=["18-24", "25-34", "35-44", "45-54", "55-64"]
        )

    region_avg = df.groupby(['region', 'age_group'], observed=True)['purchase_amount'].mean().reset_index()

    plt.figure(figsize=(16, 12))
    sns.barplot(
    data=region_avg,
    x='region',
    y='purchase_amount',
    hue='age_group',
    palette='Set2'
    )
    plt.title("Average Purchase Amount by Region and Age Group")
    plt.xlabel("Region")
    plt.ylabel("Average Purchase Amount")
    plt.legend(title="Age Group", loc='upper left', bbox_to_anchor=(0, 1))
    plt.tight_layout()
    plt.savefig(os.path.join(destination, "region_avg_spending.png"))
    plt.show()