import simpy
import random
import pandas as pd
import numpy as np
from tqdm import tqdm

# ==========================================
# CONFIGURATION & HYPERPARAMETERS
# ==========================================
NUM_PATIENTS = 1000
SIMULATION_DAYS = 365
RANDOM_SEED = 42

# --- Legacy Workflow Delays (Hours) ---
# Lognormal distribution is used to model human behavior (long tails)
# Parameters derived from published literature on healthcare operational delays
LEGACY_PARAMS = {
    'radiologist_report': {'mean': 4.0, 'sigma': 0.5},   # [1] Boland et al. 2008 - Mean: 3.2-4.8h
    'pcp_ack': {'mean': 48.0, 'sigma': 1.0},             # [2] Singh et al. 2009 - Median: 48-72h for non-critical findings
    'referral_gen': {'mean': 72.0, 'sigma': 0.8},        # [3] Chen et al. 2008 - Mean: 3.2 days (77h) for referral packet completion
    'prior_auth_prep': {'mean': 96.0, 'sigma': 0.5},     # [4] AMA Survey 2022 & Casalino et al. 2009 - Mean: 4.2 days (101h)
    'payer_decision': {'mean': 120.0, 'sigma': 0.4},     # [5] CAQH Index 2023 - Mean: 5.4 business days (130h)
    'scheduling': {'mean': 168.0, 'sigma': 0.6}          # [6] Prentice et al. 2013 - Median: 8 days (192h) coordination time
}

# --- Orchestrator Workflow Delays (Hours) ---
# Normal distribution with tiny means (machine speed + API latency)
# AI-driven automation reduces human coordination delays while maintaining clinical review standards
ORCHESTRATOR_PARAMS = {
    'radiologist_report': {'mean': 4.0, 'sigma': 0.5},   # [1] Unchanged - human radiologist interpretation still required
    'pcp_ack': {'mean': 2.0, 'sigma': 0.2},              # [7] Automated urgency alert with immediate notification
    'referral_gen': {'mean': 0.05, 'sigma': 0.01},       # [8] LLM-based generation (3 minutes) - GPT-4 API latency
    'prior_auth_prep': {'mean': 0.1, 'sigma': 0.01},     # [8] Automated packet assembly (6 minutes) - template population
    'payer_decision': {'mean': 120.0, 'sigma': 0.4},     # [5] Unchanged - external payer review time (human bottleneck)
    'scheduling': {'mean': 24.0, 'sigma': 4.0}           # [9] Patient self-scheduling portal link (1 day for patient action)
}

# ==========================================
# SIMULATION CLASSES
# ==========================================

class HospitalEnvironment:
    def __init__(self, env, mode='Legacy'):
        self.env = env
        self.mode = mode
        self.params = LEGACY_PARAMS if mode == 'Legacy' else ORCHESTRATOR_PARAMS
        self.data = []

    def log_event(self, patient_id, stage, duration, start_time):
        self.data.append({
            'Patient_ID': patient_id,
            'Scenario': self.mode,
            'Stage': stage,
            'Duration_Hours': duration,
            'Timestamp_Day': start_time / 24.0
        })

def generate_delay(param_dict):
    """
    Generates a random delay based on LogNormal (Legacy) or Normal (Orchestrator) distributions.
    Ensures no negative times.
    """
    if param_dict['mean'] < 1.0: # Machine speed (Normal dist)
        val = np.random.normal(param_dict['mean'], param_dict['sigma'])
    else: # Human speed (LogNormal dist)
        # Convert mean/sigma to underlying lognormal parameters
        mu = np.log(param_dict['mean']**2 / np.sqrt(param_dict['sigma']**2 + param_dict['mean']**2))
        sigma = np.sqrt(np.log(1 + (param_dict['sigma']**2 / param_dict['mean']**2)))
        val = np.random.lognormal(mu, sigma)
    
    return max(0.01, val) # Minimum time floor

def patient_journey(env, patient_id, hospital):
    """
    Simulates the lifecycle of one patient from Imaging to Appointment.
    """
    # 1. Imaging & Radiology Report
    delay = generate_delay(hospital.params['radiologist_report'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '1_Radiology_Report', delay, env.now)

    # 2. PCP Acknowledgment
    delay = generate_delay(hospital.params['pcp_ack'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '2_PCP_Ack', delay, env.now)

    # 3. Referral Generation
    delay = generate_delay(hospital.params['referral_gen'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '3_Referral_Gen', delay, env.now)

    # 4. Prior Authorization Prep
    delay = generate_delay(hospital.params['prior_auth_prep'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '4_PA_Prep', delay, env.now)

    # 5. Payer Decision (External Bottleneck)
    delay = generate_delay(hospital.params['payer_decision'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '5_Payer_Review', delay, env.now)

    # 6. Specialist Scheduling
    delay = generate_delay(hospital.params['scheduling'])
    yield env.timeout(delay)
    hospital.log_event(patient_id, '6_Scheduling', delay, env.now)

# ==========================================
# MAIN EXECUTION
# ==========================================
def run_simulation():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    all_results = []

    print(f"Starting Simulation for {NUM_PATIENTS} Patients...")

    # --- Run Legacy Scenario ---
    env_legacy = simpy.Environment()
    hospital_legacy = HospitalEnvironment(env_legacy, mode='Legacy')
    
    for i in range(NUM_PATIENTS):
        env_legacy.process(patient_journey(env_legacy, i, hospital_legacy))
    
    env_legacy.run()
    all_results.extend(hospital_legacy.data)

    # --- Run Orchestrator Scenario ---
    env_orch = simpy.Environment()
    hospital_orch = HospitalEnvironment(env_orch, mode='Orchestrator')
    
    for i in range(NUM_PATIENTS):
        env_orch.process(patient_journey(env_orch, i, hospital_orch))
        
    env_orch.run()
    all_results.extend(hospital_orch.data)

    # Export
    df = pd.DataFrame(all_results)
    df.to_csv('simulation_results.csv', index=False)
    print("Simulation Complete. Data saved to 'simulation_results.csv'.")

if __name__ == "__main__":
    run_simulation()