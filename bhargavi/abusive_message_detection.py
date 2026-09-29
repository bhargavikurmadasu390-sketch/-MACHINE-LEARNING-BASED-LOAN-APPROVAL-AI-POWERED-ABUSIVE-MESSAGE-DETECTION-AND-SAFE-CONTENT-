"""
AI-Powered Abusive Message Detection and Safe Content Classification Platform
Detects abusive, offensive, and harmful messages using NLP and Machine Learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. GENERATE SYNTHETIC MESSAGE DATASET
# ============================================================================

def generate_message_dataset(n_messages=1000, random_state=42):
    """Generate synthetic message dataset with abusive and safe messages"""
    np.random.seed(random_state)
    
    # Safe messages
    safe_messages = [
        "Hello, how are you doing today?",
        "Great to see you! Let's catch up soon.",
        "Thank you for your help and support.",
        "I really appreciate your kind words.",
        "Let's work together on this project.",
        "Have a wonderful day ahead!",
        "Your feedback is very valuable to us.",
        "I'm excited about this opportunity.",
        "Thanks for being such a great friend.",
        "Let's celebrate this achievement together.",
        "I hope you're having a fantastic day.",
        "Your contribution is truly appreciated.",
        "Looking forward to our meeting tomorrow.",
        "Thank you for your patience and understanding.",
        "I'm grateful for your support and guidance.",
        "Let's make this project a success together.",
        "I hope everything is going well for you.",
        "Your dedication is truly inspiring.",
        "Let's keep in touch and stay connected.",
        "I'm confident we can achieve great things.",
    ]
    
    # Abusive messages
    abusive_messages = [
        "You are so stupid and worthless!",
        "I hate you, you're disgusting!",
        "Go kill yourself, nobody likes you.",
        "You're a complete idiot and a waste of space.",
        "I hope something bad happens to you.",
        "You're the worst person I've ever met.",
        "Shut up, nobody wants to hear from you.",
        "You deserve to suffer for what you did.",
        "I'm going to hurt you if you don't leave.",
        "You're a pathetic loser and a failure.",
        "Everyone hates you, just disappear.",
        "You should be ashamed of yourself.",
        "I wish you would just die already.",
        "You're not worth anyone's time.",
        "Go away, you're absolutely disgusting.",
        "I hope you get what you deserve.",
        "You're a piece of trash, worthless.",
        "Nobody cares about your pathetic life.",
        "You make me sick, I hate you.",
        "You're a disgrace to humanity.",
    ]
    
    messages = []
    labels = []
    
    # Generate safe messages
    n_safe = int(n_messages * 0.7)
    for i in range(n_safe):
        msg = np.random.choice(safe_messages)
        # Add some variation
        msg = msg + " " + np.random.choice(["", "Really!", "Thanks.", "Good.", "Nice."])
        messages.append(msg)
        labels.append(0)  # Safe
    
    # Generate abusive messages
    n_abusive = n_messages - n_safe
    for i in range(n_abusive):
        msg = np.random.choice(abusive_messages)
        # Add some variation
        msg = msg + " " + np.random.choice(["", "!!!!", "...", "???", "!!!"])
        messages.append(msg)
        labels.append(1)  # Abusive
    
    # Create DataFrame
    df = pd.DataFrame({
        'Message_ID': np.arange(1, n_messages + 1),
        'Message': messages,
        'Label': labels,
        'Message_Length': [len(msg) for msg in messages],
        'Word_Count': [len(msg.split()) for msg in messages],
        'Exclamation_Count': [msg.count('!') for msg in messages],
        'Question_Count': [msg.count('?') for msg in messages],
        'Capital_Ratio': [sum(1 for c in msg if c.isupper()) / len(msg) if len(msg) > 0 else 0 for msg in messages]
    })
    
    print("=" * 90)
    print("ABUSIVE MESSAGE DETECTION SYSTEM - DATASET OVERVIEW")
    print("=" * 90)
    print(f"\nTotal Messages: {len(df)}")
    print(f"\nMessage Distribution:")
    print(f"  Safe Messages: {(df['Label'] == 0).sum()} ({(df['Label'] == 0).sum()/len(df)*100:.1f}%)")
    print(f"  Abusive Messages: {(df['Label'] == 1).sum()} ({(df['Label'] == 1).sum()/len(df)*100:.1f}%)")
    print(f"\nMessage Statistics:")
    print(f"  Average Length: {df['Message_Length'].mean():.1f} characters")
    print(f"  Average Words: {df['Word_Count'].mean():.1f}")
    print(f"  Avg Exclamation Marks: {df['Exclamation_Count'].mean():.2f}")
    print(f"  Avg Capital Ratio: {df['Capital_Ratio'].mean():.2f}")
    
    return df

# ============================================================================
# 2. NLP FEATURE EXTRACTION
# ============================================================================

def extract_nlp_features(df):
    """Extract NLP features from messages"""
    print("\n" + "=" * 90)
    print("NLP FEATURE EXTRACTION")
    print("=" * 90)
    
    # TF-IDF Vectorization
    print("\nExtracting TF-IDF features...")
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english', lowercase=True)
    tfidf_features = vectorizer.fit_transform(df['Message'])
    
    # Convert to dense array for easier handling
    tfidf_array = tfidf_features.toarray()
    
    # Combine with other features
    other_features = df[['Message_Length', 'Word_Count', 'Exclamation_Count', 
                         'Question_Count', 'Capital_Ratio']].values
    
    # Standardize other features
    scaler = StandardScaler()
    other_features_scaled = scaler.fit_transform(other_features)
    
    # Combine all features
    X = np.hstack([tfidf_array, other_features_scaled])
    y = df['Label'].values
    
    print(f"Total features extracted: {X.shape[1]}")
    print(f"  TF-IDF features: {tfidf_array.shape[1]}")
    print(f"  Linguistic features: {other_features_scaled.shape[1]}")
    
    return X, y, vectorizer, scaler

# ============================================================================
# 3. VISUALIZATION FUNCTIONS
# ============================================================================

def visualize_message_distribution(df):
    """Visualize message distribution"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Label distribution
    label_counts = df['Label'].value_counts()
    colors = ['#2E86AB', '#D62828']
    axes[0, 0].bar(['Safe', 'Abusive'], [label_counts[0], label_counts[1]], 
                   color=colors, edgecolor='black', alpha=0.8)
    axes[0, 0].set_title('Message Classification Distribution', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylabel('Number of Messages')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Message length distribution
    safe_length = df[df['Label'] == 0]['Message_Length']
    abusive_length = df[df['Label'] == 1]['Message_Length']
    axes[0, 1].hist([safe_length, abusive_length], label=['Safe', 'Abusive'], 
                    bins=30, color=['#2E86AB', '#D62828'], alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Message Length Distribution', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Message Length (characters)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # Exclamation marks
    safe_excl = df[df['Label'] == 0]['Exclamation_Count']
    abusive_excl = df[df['Label'] == 1]['Exclamation_Count']
    axes[1, 0].boxplot([safe_excl, abusive_excl], labels=['Safe', 'Abusive'])
    axes[1, 0].set_title('Exclamation Marks by Message Type', fontweight='bold', fontsize=12)
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].grid(alpha=0.3)
    
    # Capital letter ratio
    safe_cap = df[df['Label'] == 0]['Capital_Ratio']
    abusive_cap = df[df['Label'] == 1]['Capital_Ratio']
    axes[1, 1].boxplot([safe_cap, abusive_cap], labels=['Safe', 'Abusive'])
    axes[1, 1].set_title('Capital Letter Ratio by Message Type', fontweight='bold', fontsize=12)
    axes[1, 1].set_ylabel('Ratio')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/message_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Message distribution visualization saved")
    plt.close()

def visualize_model_comparison(results):
    """Visualize model performance comparison"""
    models = list(results.keys())
    accuracy = [results[m]['Accuracy'] for m in models]
    precision = [results[m]['Precision'] for m in models]
    recall = [results[m]['Recall'] for m in models]
    f1 = [results[m]['F1'] for m in models]
    
    x = np.arange(len(models))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(x - 1.5*width, accuracy, width, label='Accuracy', alpha=0.8, edgecolor='black')
    ax.bar(x - 0.5*width, precision, width, label='Precision', alpha=0.8, edgecolor='black')
    ax.bar(x + 0.5*width, recall, width, label='Recall', alpha=0.8, edgecolor='black')
    ax.bar(x + 1.5*width, f1, width, label='F1-Score', alpha=0.8, edgecolor='black')
    
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=12)
    ax.set_ylabel('Score')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Model comparison visualization saved")
    plt.close()

def visualize_confusion_matrices(y_test, y_pred_lr, y_pred_rf, y_pred_gb):
    """Visualize confusion matrices"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    models_data = [
        ('Logistic Regression', y_pred_lr),
        ('Random Forest', y_pred_rf),
        ('Gradient Boosting', y_pred_gb)
    ]
    
    for idx, (name, y_pred) in enumerate(models_data):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                   xticklabels=['Safe', 'Abusive'],
                   yticklabels=['Safe', 'Abusive'])
        axes[idx].set_title(f'Confusion Matrix - {name}', fontweight='bold')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("✓ Confusion matrices visualization saved")
    plt.close()

def visualize_roc_curves(y_test, y_pred_proba_lr, y_pred_proba_rf, y_pred_proba_gb):
    """Visualize ROC curves"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    models_data = [
        ('Logistic Regression', y_pred_proba_lr),
        ('Random Forest', y_pred_proba_rf),
        ('Gradient Boosting', y_pred_proba_gb)
    ]
    
    for name, y_proba in models_data:
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        ax.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {auc:.4f})')
    
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    ax.set_title('ROC Curves - Model Comparison', fontweight='bold', fontsize=12)
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/roc_curves.png', dpi=300, bbox_inches='tight')
    print("✓ ROC curves visualization saved")
    plt.close()

def visualize_feature_importance(feature_names, rf_model):
    """Visualize feature importance"""
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(range(len(indices)), importances[indices], 
           color='#2E86AB', edgecolor='black', alpha=0.8)
    ax.set_xticks(range(len(indices)))
    ax.set_xticklabels([feature_names[i] for i in indices], rotation=45, ha='right')
    ax.set_title('Top 10 Feature Importance (Random Forest)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Importance Score')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Feature importance visualization saved")
    plt.close()

# ============================================================================
# 4. MODEL BUILDING AND TRAINING
# ============================================================================

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    print("\n" + "=" * 90)
    print("MODEL TRAINING")
    print("=" * 90)
    
    results = {}
    models = {}
    predictions = {}
    probabilities = {}
    
    # Logistic Regression
    print("\nTraining Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    y_proba_lr = lr_model.predict_proba(X_test)[:, 1]
    
    results['Logistic Regression'] = {
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr),
        'Recall': recall_score(y_test, y_pred_lr),
        'F1': f1_score(y_test, y_pred_lr),
        'ROC-AUC': roc_auc_score(y_test, y_proba_lr)
    }
    models['Logistic Regression'] = lr_model
    predictions['Logistic Regression'] = y_pred_lr
    probabilities['Logistic Regression'] = y_proba_lr
    
    # Random Forest
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    y_proba_rf = rf_model.predict_proba(X_test)[:, 1]
    
    results['Random Forest'] = {
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf),
        'Recall': recall_score(y_test, y_pred_rf),
        'F1': f1_score(y_test, y_pred_rf),
        'ROC-AUC': roc_auc_score(y_test, y_proba_rf)
    }
    models['Random Forest'] = rf_model
    predictions['Random Forest'] = y_pred_rf
    probabilities['Random Forest'] = y_proba_rf
    
    # Gradient Boosting
    print("Training Gradient Boosting Classifier...")
    gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    y_proba_gb = gb_model.predict_proba(X_test)[:, 1]
    
    results['Gradient Boosting'] = {
        'Accuracy': accuracy_score(y_test, y_pred_gb),
        'Precision': precision_score(y_test, y_pred_gb),
        'Recall': recall_score(y_test, y_pred_gb),
        'F1': f1_score(y_test, y_pred_gb),
        'ROC-AUC': roc_auc_score(y_test, y_proba_gb)
    }
    models['Gradient Boosting'] = gb_model
    predictions['Gradient Boosting'] = y_pred_gb
    probabilities['Gradient Boosting'] = y_proba_gb
    
    return results, models, predictions, probabilities, y_pred_lr, y_pred_rf, y_pred_gb, y_proba_lr, y_proba_rf, y_proba_gb

# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 90)
    print("AI-POWERED ABUSIVE MESSAGE DETECTION AND SAFE CONTENT CLASSIFICATION PLATFORM")
    print("=" * 90)
    
    # Generate dataset
    print("\n[Step 1] Generating Message Dataset...")
    df = generate_message_dataset(n_messages=1000)
    
    # Extract NLP features
    print("\n[Step 2] Extracting NLP Features...")
    X, y, vectorizer, scaler = extract_nlp_features(df)
    
    # Split data
    print("\n[Step 3] Splitting Data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training set size: {len(X_train)} messages")
    print(f"Test set size: {len(X_test)} messages")
    
    # Generate visualizations
    print("\n[Step 4] Generating Visualizations...")
    print("Creating message distribution visualization...")
    visualize_message_distribution(df)
    
    # Train models
    print("\n[Step 5] Training Classification Models...")
    results, models, predictions, probabilities, y_pred_lr, y_pred_rf, y_pred_gb, y_proba_lr, y_proba_rf, y_proba_gb = train_models(
        X_train, X_test, y_train, y_test
    )
    
    # Print results
    print("\n" + "=" * 90)
    print("MODEL PERFORMANCE RESULTS")
    print("=" * 90)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
    
    # Generate additional visualizations
    print("\n[Step 6] Generating Additional Visualizations...")
    print("Creating model comparison...")
    visualize_model_comparison(results)
    
    print("Creating confusion matrices...")
    visualize_confusion_matrices(y_test, y_pred_lr, y_pred_rf, y_pred_gb)
    
    print("Creating ROC curves...")
    visualize_roc_curves(y_test, y_proba_lr, y_proba_rf, y_proba_gb)
    
    # Get feature names for importance plot
    feature_names = [f"TF-IDF_{i}" for i in range(100)] + ['Message_Length', 'Word_Count', 'Exclamation_Count', 'Question_Count', 'Capital_Ratio']
    print("Creating feature importance...")
    visualize_feature_importance(feature_names, models['Random Forest'])
    
    print("\n" + "=" * 90)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 90)
    print("\nGenerated Visualizations:")
    print("  1. message_distribution.png")
    print("  2. model_comparison.png")
    print("  3. confusion_matrices.png")
    print("  4. roc_curves.png")
    print("  5. feature_importance.png")
    
    return df, X_train, X_test, y_train, y_test, results, models

if __name__ == "__main__":
    df, X_train, X_test, y_train, y_test, results, models = main()
