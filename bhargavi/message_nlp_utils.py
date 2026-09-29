"""
NLP Utilities for Abusive Message Detection System
Provides utilities for message analysis, content classification, and insights generation
"""

import numpy as np
import pandas as pd
from collections import Counter

class MessageAnalyzer:
    """Analyzes messages for linguistic patterns and content characteristics"""
    
    def __init__(self, df):
        """Initialize with message data"""
        self.df = df
        
    def calculate_message_metrics(self):
        """Calculate comprehensive message metrics"""
        metrics = {
            'Total_Messages': len(self.df),
            'Safe_Messages': (self.df['Label'] == 0).sum(),
            'Abusive_Messages': (self.df['Label'] == 1).sum(),
            'Safe_Percentage': (self.df['Label'] == 0).sum() / len(self.df) * 100,
            'Abusive_Percentage': (self.df['Label'] == 1).sum() / len(self.df) * 100,
            'Avg_Message_Length': self.df['Message_Length'].mean(),
            'Avg_Word_Count': self.df['Word_Count'].mean(),
            'Avg_Exclamation_Count': self.df['Exclamation_Count'].mean(),
            'Avg_Question_Count': self.df['Question_Count'].mean(),
            'Avg_Capital_Ratio': self.df['Capital_Ratio'].mean()
        }
        
        return metrics
    
    def analyze_by_message_length(self):
        """Analyze message classification by length"""
        length_bins = [0, 20, 40, 60, 80, 100, 500]
        length_labels = ['Very Short', 'Short', 'Medium', 'Long', 'Very Long', 'Extremely Long']
        
        self.df['Length_Category'] = pd.cut(self.df['Message_Length'], 
                                            bins=length_bins, labels=length_labels)
        
        analysis = []
        for category in length_labels:
            category_data = self.df[self.df['Length_Category'] == category]
            if len(category_data) > 0:
                abusive_rate = (category_data['Label'] == 1).sum() / len(category_data) * 100
                
                analysis.append({
                    'Length_Category': category,
                    'Count': len(category_data),
                    'Abusive_Rate': abusive_rate,
                    'Avg_Exclamation': category_data['Exclamation_Count'].mean(),
                    'Avg_Capital_Ratio': category_data['Capital_Ratio'].mean()
                })
        
        return pd.DataFrame(analysis)
    
    def analyze_by_linguistic_features(self):
        """Analyze message type by linguistic features"""
        analysis = []
        
        # Analyze by exclamation mark usage
        high_excl = self.df[self.df['Exclamation_Count'] >= 2]
        low_excl = self.df[self.df['Exclamation_Count'] < 2]
        
        analysis.append({
            'Feature': 'High Exclamation (>=2)',
            'Count': len(high_excl),
            'Abusive_Rate': (high_excl['Label'] == 1).sum() / len(high_excl) * 100 if len(high_excl) > 0 else 0,
            'Avg_Length': high_excl['Message_Length'].mean() if len(high_excl) > 0 else 0
        })
        
        analysis.append({
            'Feature': 'Low Exclamation (<2)',
            'Count': len(low_excl),
            'Abusive_Rate': (low_excl['Label'] == 1).sum() / len(low_excl) * 100 if len(low_excl) > 0 else 0,
            'Avg_Length': low_excl['Message_Length'].mean() if len(low_excl) > 0 else 0
        })
        
        # Analyze by capital letter usage
        high_cap = self.df[self.df['Capital_Ratio'] >= 0.1]
        low_cap = self.df[self.df['Capital_Ratio'] < 0.1]
        
        analysis.append({
            'Feature': 'High Capitals (>=10%)',
            'Count': len(high_cap),
            'Abusive_Rate': (high_cap['Label'] == 1).sum() / len(high_cap) * 100 if len(high_cap) > 0 else 0,
            'Avg_Length': high_cap['Message_Length'].mean() if len(high_cap) > 0 else 0
        })
        
        analysis.append({
            'Feature': 'Low Capitals (<10%)',
            'Count': len(low_cap),
            'Abusive_Rate': (low_cap['Label'] == 1).sum() / len(low_cap) * 100 if len(low_cap) > 0 else 0,
            'Avg_Length': low_cap['Message_Length'].mean() if len(low_cap) > 0 else 0
        })
        
        return pd.DataFrame(analysis)
    
    def identify_high_risk_messages(self, threshold=0.5):
        """Identify messages with high risk characteristics"""
        # Calculate risk score based on linguistic features
        self.df['Risk_Score'] = (
            (self.df['Exclamation_Count'] / (self.df['Exclamation_Count'].max() + 1)) * 0.3 +
            (self.df['Capital_Ratio']) * 0.3 +
            (self.df['Question_Count'] / (self.df['Question_Count'].max() + 1)) * 0.2 +
            (1 - self.df['Message_Length'] / self.df['Message_Length'].max()) * 0.2
        )
        
        high_risk = self.df[self.df['Risk_Score'] > threshold]
        
        return {
            'High_Risk_Count': len(high_risk),
            'High_Risk_Percentage': len(high_risk) / len(self.df) * 100,
            'High_Risk_Abusive_Rate': (high_risk['Label'] == 1).sum() / len(high_risk) * 100 if len(high_risk) > 0 else 0,
            'Avg_Risk_Score': high_risk['Risk_Score'].mean() if len(high_risk) > 0 else 0
        }
    
    def calculate_content_drivers(self):
        """Identify key factors driving abusive classification"""
        safe = self.df[self.df['Label'] == 0]
        abusive = self.df[self.df['Label'] == 1]
        
        drivers = {
            'Avg_Length_Safe': safe['Message_Length'].mean(),
            'Avg_Length_Abusive': abusive['Message_Length'].mean(),
            'Avg_Exclamation_Safe': safe['Exclamation_Count'].mean(),
            'Avg_Exclamation_Abusive': abusive['Exclamation_Count'].mean(),
            'Avg_Capital_Safe': safe['Capital_Ratio'].mean(),
            'Avg_Capital_Abusive': abusive['Capital_Ratio'].mean(),
            'Avg_Words_Safe': safe['Word_Count'].mean(),
            'Avg_Words_Abusive': abusive['Word_Count'].mean()
        }
        
        return drivers


class ContentInsights:
    """Generates actionable insights from message analysis"""
    
    def __init__(self, df):
        """Initialize with message data"""
        self.df = df
        self.analyzer = MessageAnalyzer(df)
    
    def get_key_findings(self):
        """Extract key findings from the data"""
        metrics = self.analyzer.calculate_message_metrics()
        
        findings = []
        
        # Finding 1: Overall abusive rate
        abusive_rate = metrics['Abusive_Percentage']
        if abusive_rate >= 40:
            findings.append(f"High abusive message rate of {abusive_rate:.1f}% detected. Urgent moderation needed.")
        elif abusive_rate >= 25:
            findings.append(f"Moderate abusive message rate of {abusive_rate:.1f}% indicates ongoing moderation challenges.")
        else:
            findings.append(f"Low abusive message rate of {abusive_rate:.1f}% suggests effective community management.")
        
        # Finding 2: Linguistic patterns
        drivers = self.analyzer.calculate_content_drivers()
        excl_diff = drivers['Avg_Exclamation_Abusive'] - drivers['Avg_Exclamation_Safe']
        findings.append(f"Exclamation mark usage is a strong indicator: abusive messages have {excl_diff:.2f} more exclamation marks on average.")
        
        # Finding 3: Message length impact
        length_diff = drivers['Avg_Length_Safe'] - drivers['Avg_Length_Abusive']
        findings.append(f"Message length correlates with content type: safe messages are {length_diff:.1f} characters longer on average.")
        
        return findings
    
    def get_moderation_recommendations(self):
        """Generate content moderation recommendations"""
        high_risk = self.analyzer.identify_high_risk_messages()
        
        recommendations = []
        
        if high_risk['High_Risk_Percentage'] > 30:
            recommendations.append("High proportion of high-risk messages detected. Implement real-time flagging system.")
        
        if high_risk['High_Risk_Abusive_Rate'] > 60:
            recommendations.append("High-risk messages have significant abusive content. Prioritize these for human review.")
        
        recommendations.append("Implement automated alerts for messages with multiple exclamation marks and high capital letter usage.")
        recommendations.append("Develop user education program to promote respectful communication patterns.")
        
        return recommendations
    
    def get_platform_insights(self):
        """Generate platform-level insights"""
        metrics = self.analyzer.calculate_message_metrics()
        
        insights = []
        
        safe_count = metrics['Safe_Messages']
        abusive_count = metrics['Abusive_Messages']
        
        insights.append(f"Total messages processed: {metrics['Total_Messages']:,} with {metrics['Safe_Percentage']:.1f}% safe and {metrics['Abusive_Percentage']:.1f}% abusive")
        insights.append(f"Average message length: {metrics['Avg_Message_Length']:.1f} characters, indicating {('brief' if metrics['Avg_Message_Length'] < 50 else 'detailed')} communication")
        insights.append(f"Linguistic intensity: {metrics['Avg_Exclamation_Count']:.2f} exclamation marks and {metrics['Avg_Capital_Ratio']:.2%} capital letter ratio on average")
        
        return insights


def generate_and_save_message_datasets(output_dir='/home/ubuntu'):
    """Generate and save all sample message datasets"""
    print("Generating message datasets...")
    
    # Generate message dataset
    from abusive_message_detection import generate_message_dataset
    
    df = generate_message_dataset(n_messages=1000)
    
    # Save raw dataset
    print("  Saving raw message dataset...")
    df.to_csv(f'{output_dir}/messages.csv', index=False)
    print(f"  ✓ Raw dataset saved")
    
    # Perform message analysis
    print("  Performing message analysis...")
    analyzer = MessageAnalyzer(df)
    
    # Calculate message metrics
    print("  Calculating message metrics...")
    metrics = analyzer.calculate_message_metrics()
    
    metrics_df = pd.DataFrame({
        'Metric': list(metrics.keys()),
        'Value': list(metrics.values())
    })
    
    metrics_df.to_csv(f'{output_dir}/message_metrics.csv', index=False)
    print(f"  ✓ Message metrics saved")
    
    # Analyze by message length
    print("  Analyzing by message length...")
    length_analysis = analyzer.analyze_by_message_length()
    length_analysis.to_csv(f'{output_dir}/message_length_analysis.csv', index=False)
    print(f"  ✓ Length analysis saved")
    
    # Analyze by linguistic features
    print("  Analyzing by linguistic features...")
    linguistic_analysis = analyzer.analyze_by_linguistic_features()
    linguistic_analysis.to_csv(f'{output_dir}/message_linguistic_analysis.csv', index=False)
    print(f"  ✓ Linguistic analysis saved")
    
    # Generate insights
    print("  Generating insights...")
    insights = ContentInsights(df)
    
    findings = insights.get_key_findings()
    recommendations = insights.get_moderation_recommendations()
    platform = insights.get_platform_insights()
    
    insights_df = pd.DataFrame({
        'Type': ['Finding'] * len(findings) + ['Recommendation'] * len(recommendations) + ['Platform'] * len(platform),
        'Insight': findings + recommendations + platform
    })
    
    insights_df.to_csv(f'{output_dir}/message_insights.csv', index=False)
    print(f"  ✓ Insights saved")
    
    return df, analyzer, metrics


if __name__ == '__main__':
    df, analyzer, metrics = generate_and_save_message_datasets()
    
    print("\nDataset Summary:")
    print(f"Total Messages: {len(df)}")
    print(f"Safe: {(df['Label'] == 0).sum()}")
    print(f"Abusive: {(df['Label'] == 1).sum()}")
    
    print("\nMessage Metrics:")
    for metric, value in list(metrics.items())[:5]:
        print(f"  {metric}: {value:.2f}")
    
    print("\nRisk Analysis:")
    high_risk = analyzer.identify_high_risk_messages()
    print(f"  High-Risk Messages: {high_risk['High_Risk_Count']}")
    print(f"  High-Risk Percentage: {high_risk['High_Risk_Percentage']:.2f}%")
