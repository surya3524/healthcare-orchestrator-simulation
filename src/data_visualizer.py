import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Plot Styles for IEEE Access (Times New Roman / Serif)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16

def load_and_prep_data(filepath='simulation_results.csv'):
    df = pd.read_csv(filepath)
    
    # Calculate Total Duration per Patient
    total_time = df.groupby(['Patient_ID', 'Scenario'])['Duration_Hours'].sum().reset_index()
    total_time['Total_Days'] = total_time['Duration_Hours'] / 24.0
    
    return df, total_time

def plot_histogram(total_time_df):
    """Generates Figure 1: Comparative Latency Histogram"""
    plt.figure(figsize=(10, 6), dpi=300)
    
    palette = {'Legacy': '#d62728', 'Orchestrator': '#2ca02c'} # Red vs Green
    
    sns.histplot(
        data=total_time_df,
        x='Total_Days',
        hue='Scenario',
        kde=True,
        element='step',
        palette=palette,
        alpha=0.3
    )
    
    plt.title('Distribution of Total Care-Path Latency (N=1,000)', fontweight='bold')
    plt.xlabel('Total Days from Imaging to Appointment')
    plt.ylabel('Patient Count')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('Fig1_Latency_Histogram.png')
    print("Saved Fig1_Latency_Histogram.png")

def plot_heatmap(raw_df):
    """Generates Figure 2: Bottleneck Heatmap"""
    # Pivot data for Heatmap: Rows=Patient, Cols=Stage, Values=Days
    # We take a sample of 25 patients from each scenario for readability
    
    sample_ids = list(range(0, 25))
    
    # Filter and Pivot Legacy
    legacy_df = raw_df[(raw_df['Scenario'] == 'Legacy') & (raw_df['Patient_ID'].isin(sample_ids))]
    legacy_pivot = legacy_df.pivot(index='Patient_ID', columns='Stage', values='Duration_Hours') / 24.0
    
    # Filter and Pivot Orchestrator
    orch_df = raw_df[(raw_df['Scenario'] == 'Orchestrator') & (raw_df['Patient_ID'].isin(sample_ids))]
    orch_pivot = orch_df.pivot(index='Patient_ID', columns='Stage', values='Duration_Hours') / 24.0
    
    # Order columns logically
    col_order = ['1_Radiology_Report', '2_PCP_Ack', '3_Referral_Gen', '4_PA_Prep', '5_Payer_Review', '6_Scheduling']
    legacy_pivot = legacy_pivot.reindex(columns=col_order)
    orch_pivot = orch_pivot.reindex(columns=col_order)

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), dpi=300, sharey=True)
    
    sns.heatmap(legacy_pivot, ax=axes[0], cmap='Reds', annot=False, vmin=0, vmax=7, cbar=False)
    axes[0].set_title('Legacy Workflow (Human Delays)', fontweight='bold')
    axes[0].set_ylabel('Patient ID (Sample)')
    axes[0].set_xlabel('Care Path Stage')
    
    sns.heatmap(orch_pivot, ax=axes[1], cmap='Greens', annot=False, vmin=0, vmax=7, cbar=True, cbar_kws={'label': 'Delay (Days)'})
    axes[1].set_title('Orchestrator Workflow (AI Agent Speed)', fontweight='bold')
    axes[1].set_xlabel('Care Path Stage')
    
    plt.tight_layout()
    plt.savefig('Fig2_Bottleneck_Heatmap.png')
    print("Saved Fig2_Bottleneck_Heatmap.png")

if __name__ == "__main__":
    raw_data, total_data = load_and_prep_data()
    plot_histogram(total_data)
    plot_heatmap(raw_data)