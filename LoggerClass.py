import pandas as pd

class FraudRuleLogger:
    def __init__(self):
        self.trial_number = 1
        self.logs = []

    def log_rule(self, df, rule_name, rule_filter):
        filtered_df = df[rule_filter]

        total_transactions = filtered_df.shape[0]
        total_fraud_count = filtered_df['fraud_label'].sum()
        fraud_rate = (total_fraud_count / total_transactions) * 100 if total_transactions > 0 else 0
        fraud_amount_saved = filtered_df[filtered_df['fraud_label'] == 1]['amount'].sum()

        self.logs.append({
            'trial_number': self.trial_number,
            'rule_name': rule_name,
            'total_fraud_count': int(total_fraud_count),
            'total_transactions': int(total_transactions),
            'fraud_rate': round(fraud_rate, 2),
            'fraud_amount_saved': int(fraud_amount_saved)
        })

        self.trial_number += 1  # Increment after each log

    def get_logs(self):
        return pd.DataFrame(self.logs)

    def reset(self):
        self.trial_number = 1
        self.logs = []


