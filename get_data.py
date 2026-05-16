import pandas as pd


def load_customer_data(csv_path: str = "customer_shopping_behavior.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
        lambda x: x.fillna(x.mean())
    )

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'}, inplace=True)

    labels = ['Young_adult', 'Adult', 'Middel-Aged', 'Senior']
    df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

    frequency_mapping = {
        'Fortnightly': 14,
        'Weekly': 7,
        'Monthly': 30,
        'Quarterly': 90,
        'Annually': 365,
        'Every Months': 90,
    }
    df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

    df = df.drop(columns=['promo_code_used'], errors='ignore')
    return df


if __name__ == '__main__':
    df = load_customer_data()
    print(df.head())
    print(df.info())
    print(df.describe())
    print(df.isnull().sum())
    print(df[['age', 'age_group']].head(10))
    print(df[['frequency_of_purchases', 'purchase_frequency_days']].head(10))
    print(df.columns)

