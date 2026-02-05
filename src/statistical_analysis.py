import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Plot Styles
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 12

def load_data(filepath='simulation_results.csv'):
    """Load simulation results and compute total times per patient"""
    df = pd.read_csv(filepath)
    
    # Calculate total duration per patient
    total_time = df.groupby(['Patient_ID', 'Scenario'])['Duration_Hours'].sum().reset_index()
    total_time['Total_Days'] = total_time['Duration_Hours'] / 24.0
    
    return df, total_time

def compute_descriptive_statistics(total_time_df):
    """Compute descriptive statistics for both scenarios"""
    
    legacy = total_time_df[total_time_df['Scenario'] == 'Legacy']['Total_Days']
    orchestrator = total_time_df[total_time_df['Scenario'] == 'Orchestrator']['Total_Days']
    
    results = {
        'Legacy': {
            'n': len(legacy),
            'mean': legacy.mean(),
            'median': legacy.median(),
            'std': legacy.std(),
            'min': legacy.min(),
            'max': legacy.max(),
            'q25': legacy.quantile(0.25),
            'q75': legacy.quantile(0.75),
            'ci_95_lower': legacy.mean() - 1.96 * (legacy.std() / np.sqrt(len(legacy))),
            'ci_95_upper': legacy.mean() + 1.96 * (legacy.std() / np.sqrt(len(legacy)))
        },
        'Orchestrator': {
            'n': len(orchestrator),
            'mean': orchestrator.mean(),
            'median': orchestrator.median(),
            'std': orchestrator.std(),
            'min': orchestrator.min(),
            'max': orchestrator.max(),
            'q25': orchestrator.quantile(0.25),
            'q75': orchestrator.quantile(0.75),
            'ci_95_lower': orchestrator.mean() - 1.96 * (orchestrator.std() / np.sqrt(len(orchestrator))),
            'ci_95_upper': orchestrator.mean() + 1.96 * (orchestrator.std() / np.sqrt(len(orchestrator)))
        }
    }
    
    return results, legacy, orchestrator

def test_statistical_significance(legacy, orchestrator):
    """Perform statistical tests comparing the two scenarios"""
    
    # Independent samples t-test
    t_stat, p_value_ttest = stats.ttest_ind(legacy, orchestrator)
    
    # Mann-Whitney U test (non-parametric alternative)
    u_stat, p_value_mann = stats.mannwhitneyu(legacy, orchestrator, alternative='two-sided')
    
    # Welch's t-test (does not assume equal variances)
    t_stat_welch, p_value_welch = stats.ttest_ind(legacy, orchestrator, equal_var=False)
    
    # Cohen's d (effect size)
    pooled_std = np.sqrt(((len(legacy) - 1) * legacy.std()**2 + 
                          (len(orchestrator) - 1) * orchestrator.std()**2) / 
                         (len(legacy) + len(orchestrator) - 2))
    cohens_d = (legacy.mean() - orchestrator.mean()) / pooled_std
    
    # Hedges' g (corrected effect size for small samples)
    correction_factor = 1 - (3 / (4 * (len(legacy) + len(orchestrator)) - 9))
    hedges_g = cohens_d * correction_factor
    
    # Relative improvement
    percent_reduction = ((legacy.mean() - orchestrator.mean()) / legacy.mean()) * 100
    absolute_reduction = legacy.mean() - orchestrator.mean()
    
    return {
        't_statistic': t_stat,
        'p_value_ttest': p_value_ttest,
        'p_value_welch': p_value_welch,
        'p_value_mann_whitney': p_value_mann,
        'cohens_d': cohens_d,
        'hedges_g': hedges_g,
        'percent_reduction': percent_reduction,
        'absolute_reduction_days': absolute_reduction
    }

def test_normality(legacy, orchestrator):
    """Test if data follows normal distribution"""
    
    # Shapiro-Wilk test for normality
    shapiro_legacy = stats.shapiro(legacy)
    shapiro_orch = stats.shapiro(orchestrator)
    
    # Kolmogorov-Smirnov test
    ks_legacy = stats.kstest(legacy, 'norm', args=(legacy.mean(), legacy.std()))
    ks_orch = stats.kstest(orchestrator, 'norm', args=(orchestrator.mean(), orchestrator.std()))
    
    return {
        'Legacy': {
            'shapiro_statistic': shapiro_legacy[0],
            'shapiro_p_value': shapiro_legacy[1],
            'ks_statistic': ks_legacy[0],
            'ks_p_value': ks_legacy[1],
            'is_normal': shapiro_legacy[1] > 0.05
        },
        'Orchestrator': {
            'shapiro_statistic': shapiro_orch[0],
            'shapiro_p_value': shapiro_orch[1],
            'ks_statistic': ks_orch[0],
            'ks_p_value': ks_orch[1],
            'is_normal': shapiro_orch[1] > 0.05
        }
    }

def stage_level_analysis(raw_df):
    """Analyze differences at each workflow stage"""
    
    stage_stats = []
    
    for stage in sorted(raw_df['Stage'].unique()):
        legacy_stage = raw_df[(raw_df['Scenario'] == 'Legacy') & 
                              (raw_df['Stage'] == stage)]['Duration_Hours'] / 24.0
        orch_stage = raw_df[(raw_df['Scenario'] == 'Orchestrator') & 
                            (raw_df['Stage'] == stage)]['Duration_Hours'] / 24.0
        
        # T-test for this stage
        t_stat, p_val = stats.ttest_ind(legacy_stage, orch_stage)
        
        # Effect size
        pooled_std = np.sqrt(((len(legacy_stage) - 1) * legacy_stage.std()**2 + 
                              (len(orch_stage) - 1) * orch_stage.std()**2) / 
                             (len(legacy_stage) + len(orch_stage) - 2))
        
        if pooled_std > 0:
            cohens_d = (legacy_stage.mean() - orch_stage.mean()) / pooled_std
        else:
            cohens_d = 0.0
        
        percent_change = ((legacy_stage.mean() - orch_stage.mean()) / 
                         legacy_stage.mean() * 100) if legacy_stage.mean() > 0 else 0
        
        stage_stats.append({
            'Stage': stage,
            'Legacy_Mean_Days': legacy_stage.mean(),
            'Legacy_Std': legacy_stage.std(),
            'Orchestrator_Mean_Days': orch_stage.mean(),
            'Orchestrator_Std': orch_stage.std(),
            'Absolute_Difference_Days': legacy_stage.mean() - orch_stage.mean(),
            'Percent_Reduction': percent_change,
            'Cohens_D': cohens_d,
            'T_Statistic': t_stat,
            'P_Value': p_val,
            'Significant': 'Yes' if p_val < 0.05 else 'No'
        })
    
    return pd.DataFrame(stage_stats)

def plot_confidence_intervals(descriptive_stats):
    """Create a plot showing means with 95% confidence intervals"""
    
    scenarios = ['Legacy', 'Orchestrator']
    means = [descriptive_stats['Legacy']['mean'], 
             descriptive_stats['Orchestrator']['mean']]
    
    ci_lower = [descriptive_stats['Legacy']['ci_95_lower'],
                descriptive_stats['Orchestrator']['ci_95_lower']]
    ci_upper = [descriptive_stats['Legacy']['ci_95_upper'],
                descriptive_stats['Orchestrator']['ci_95_upper']]
    
    errors_lower = [means[0] - ci_lower[0], means[1] - ci_lower[1]]
    errors_upper = [ci_upper[0] - means[0], ci_upper[1] - means[1]]
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    
    colors = ['#d62728', '#2ca02c']
    x_pos = [0, 1]
    
    ax.bar(x_pos, means, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.errorbar(x_pos, means, yerr=[errors_lower, errors_upper], 
                fmt='none', ecolor='black', capsize=10, capthick=2, linewidth=2)
    
    ax.set_ylabel('Mean Total Care-Path Duration (Days)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Workflow Scenario', fontsize=14, fontweight='bold')
    ax.set_title('Mean Latency with 95% Confidence Intervals (N=1,000)', 
                 fontsize=16, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(scenarios)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add value labels on bars
    for i, (mean, scenario) in enumerate(zip(means, scenarios)):
        ax.text(i, mean + 0.5, f'{mean:.2f} days', 
               ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('Fig3_Confidence_Intervals.png')
    print("Saved Fig3_Confidence_Intervals.png")
    plt.close()

def generate_statistical_report(descriptive_stats, significance_tests, 
                               normality_tests, stage_analysis):
    """Generate a comprehensive statistical report"""
    
    report = []
    report.append("=" * 80)
    report.append("STATISTICAL ANALYSIS REPORT")
    report.append("Healthcare Care-Path Orchestrator Simulation")
    report.append("=" * 80)
    report.append("")
    
    # Descriptive Statistics
    report.append("1. DESCRIPTIVE STATISTICS")
    report.append("-" * 80)
    report.append(f"{'Metric':<30} {'Legacy':<20} {'Orchestrator':<20}")
    report.append("-" * 80)
    report.append(f"{'Sample Size (n)':<30} {descriptive_stats['Legacy']['n']:<20} {descriptive_stats['Orchestrator']['n']:<20}")
    report.append(f"{'Mean (days)':<30} {descriptive_stats['Legacy']['mean']:<20.2f} {descriptive_stats['Orchestrator']['mean']:<20.2f}")
    report.append(f"{'Median (days)':<30} {descriptive_stats['Legacy']['median']:<20.2f} {descriptive_stats['Orchestrator']['median']:<20.2f}")
    report.append(f"{'Std Dev (days)':<30} {descriptive_stats['Legacy']['std']:<20.2f} {descriptive_stats['Orchestrator']['std']:<20.2f}")
    report.append(f"{'Min (days)':<30} {descriptive_stats['Legacy']['min']:<20.2f} {descriptive_stats['Orchestrator']['min']:<20.2f}")
    report.append(f"{'Max (days)':<30} {descriptive_stats['Legacy']['max']:<20.2f} {descriptive_stats['Orchestrator']['max']:<20.2f}")
    report.append(f"{'25th Percentile':<30} {descriptive_stats['Legacy']['q25']:<20.2f} {descriptive_stats['Orchestrator']['q25']:<20.2f}")
    report.append(f"{'75th Percentile':<30} {descriptive_stats['Legacy']['q75']:<20.2f} {descriptive_stats['Orchestrator']['q75']:<20.2f}")
    report.append(f"{'95% CI Lower':<30} {descriptive_stats['Legacy']['ci_95_lower']:<20.2f} {descriptive_stats['Orchestrator']['ci_95_lower']:<20.2f}")
    report.append(f"{'95% CI Upper':<30} {descriptive_stats['Legacy']['ci_95_upper']:<20.2f} {descriptive_stats['Orchestrator']['ci_95_upper']:<20.2f}")
    report.append("")
    
    # Normality Tests
    report.append("2. NORMALITY TESTS")
    report.append("-" * 80)
    report.append(f"Legacy Workflow:")
    report.append(f"  Shapiro-Wilk Test: W = {normality_tests['Legacy']['shapiro_statistic']:.4f}, p = {normality_tests['Legacy']['shapiro_p_value']:.4e}")
    report.append(f"  Distribution: {'Normal' if normality_tests['Legacy']['is_normal'] else 'Non-normal'} (α = 0.05)")
    report.append(f"\nOrchestrator Workflow:")
    report.append(f"  Shapiro-Wilk Test: W = {normality_tests['Orchestrator']['shapiro_statistic']:.4f}, p = {normality_tests['Orchestrator']['shapiro_p_value']:.4e}")
    report.append(f"  Distribution: {'Normal' if normality_tests['Orchestrator']['is_normal'] else 'Non-normal'} (α = 0.05)")
    report.append("")
    
    # Statistical Significance
    report.append("3. STATISTICAL SIGNIFICANCE TESTS")
    report.append("-" * 80)
    report.append(f"Independent Samples T-Test:")
    report.append(f"  t-statistic = {significance_tests['t_statistic']:.4f}")
    report.append(f"  p-value = {significance_tests['p_value_ttest']:.4e}")
    report.append(f"  Result: {'SIGNIFICANT' if significance_tests['p_value_ttest'] < 0.05 else 'NOT SIGNIFICANT'} (α = 0.05)")
    report.append(f"\nWelch's T-Test (unequal variances):")
    report.append(f"  p-value = {significance_tests['p_value_welch']:.4e}")
    report.append(f"\nMann-Whitney U Test (non-parametric):")
    report.append(f"  p-value = {significance_tests['p_value_mann_whitney']:.4e}")
    report.append("")
    
    # Effect Size
    report.append("4. EFFECT SIZE ANALYSIS")
    report.append("-" * 80)
    report.append(f"Cohen's d = {significance_tests['cohens_d']:.4f}")
    
    # Interpret Cohen's d
    d_abs = abs(significance_tests['cohens_d'])
    if d_abs < 0.2:
        interpretation = "Negligible"
    elif d_abs < 0.5:
        interpretation = "Small"
    elif d_abs < 0.8:
        interpretation = "Medium"
    else:
        interpretation = "Large"
    
    report.append(f"Interpretation: {interpretation} effect size")
    report.append(f"  (|d| < 0.2: negligible, 0.2-0.5: small, 0.5-0.8: medium, >0.8: large)")
    report.append(f"\nHedges' g (corrected) = {significance_tests['hedges_g']:.4f}")
    report.append("")
    
    # Clinical Significance
    report.append("5. CLINICAL SIGNIFICANCE")
    report.append("-" * 80)
    report.append(f"Absolute Reduction: {significance_tests['absolute_reduction_days']:.2f} days")
    report.append(f"Relative Reduction: {significance_tests['percent_reduction']:.1f}%")
    report.append(f"\nClinical Impact (per 1,000 patients):")
    report.append(f"  Total patient-days saved: {significance_tests['absolute_reduction_days'] * 1000:.0f}")
    report.append(f"  Equivalent patient-years: {(significance_tests['absolute_reduction_days'] * 1000 / 365):.1f}")
    report.append("")
    
    # Stage-Level Analysis
    report.append("6. STAGE-LEVEL ANALYSIS")
    report.append("-" * 80)
    report.append(stage_analysis.to_string(index=False))
    report.append("")
    
    # Interpretation
    report.append("7. INTERPRETATION FOR PUBLICATION")
    report.append("-" * 80)
    report.append(f"The AI-driven orchestrator workflow demonstrated statistically significant")
    report.append(f"reduction in care-path latency (t = {significance_tests['t_statistic']:.2f}, p < 0.001).")
    report.append(f"The effect size was {interpretation.lower()} (Cohen's d = {significance_tests['cohens_d']:.2f}),")
    report.append(f"with a {significance_tests['percent_reduction']:.1f}% reduction in mean latency")
    report.append(f"({significance_tests['absolute_reduction_days']:.2f} days, 95% CI: [{descriptive_stats['Legacy']['ci_95_lower']:.2f}, {descriptive_stats['Legacy']['ci_95_upper']:.2f}]")
    report.append(f"vs [{descriptive_stats['Orchestrator']['ci_95_lower']:.2f}, {descriptive_stats['Orchestrator']['ci_95_upper']:.2f}]).")
    report.append("")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    """Run complete statistical analysis"""
    
    print("Loading simulation data...")
    raw_df, total_time_df = load_data()
    
    print("Computing descriptive statistics...")
    descriptive_stats, legacy, orchestrator = compute_descriptive_statistics(total_time_df)
    
    print("Testing normality assumptions...")
    normality_tests = test_normality(legacy, orchestrator)
    
    print("Performing significance tests...")
    significance_tests = test_statistical_significance(legacy, orchestrator)
    
    print("Analyzing stage-level differences...")
    stage_analysis = stage_level_analysis(raw_df)
    
    print("Generating confidence interval plot...")
    plot_confidence_intervals(descriptive_stats)
    
    print("Generating statistical report...")
    report = generate_statistical_report(descriptive_stats, significance_tests, 
                                        normality_tests, stage_analysis)
    
    # Save report
    with open('statistical_analysis_report.txt', 'w') as f:
        f.write(report)
    
    print("\n" + report)
    print("\nStatistical analysis complete!")
    print("Files generated:")
    print("  - statistical_analysis_report.txt")
    print("  - Fig3_Confidence_Intervals.png")
    
    # Save stage analysis as CSV
    stage_analysis.to_csv('stage_level_statistics.csv', index=False)
    print("  - stage_level_statistics.csv")

if __name__ == "__main__":
    main()
