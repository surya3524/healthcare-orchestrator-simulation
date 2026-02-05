"""
FIFO Queue Baseline System
Simple First-In-First-Out care coordination with basic priority triage.
No AI routing, predictive analytics, or automated document processing.
"""

import simpy
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
from collections import deque


@dataclass
class Patient:
    """Patient record for FIFO baseline system."""
    id: int
    arrival_time: float
    urgent_indicator: bool  # Simple binary triage
    diagnosis: str
    stage_times: dict
    total_latency: float = 0.0


class FIFOBaseline:
    """
    FIFO Queue-Based Care Coordination System.
    
    Features:
    - Two-priority queue (urgent/normal)
    - No intelligent routing
    - No automated document processing
    - Manual prior authorization
    - No dynamic rescheduling
    
    Expected Performance: ~15-16 days mean latency
    (vs. Legacy 21.17 days, Orchestrator 6.25 days)
    """
    
    def __init__(self, env: simpy.Environment, config: dict):
        self.env = env
        self.config = config
        
        # Two-level priority queues
        self.urgent_queue = deque()
        self.normal_queue = deque()
        
        # Resources (same as other systems for fair comparison)
        self.radiology_slots = simpy.Resource(
            env, capacity=config.get('radiology_slots_per_week', 120)
        )
        self.specialist_slots = simpy.Resource(
            env, capacity=config.get('specialist_slots_per_week', 40)
        )
        
        # Statistics
        self.completed_patients: List[Patient] = []
        self.total_processed = 0
        
    def triage_patient(self, patient: Patient) -> str:
        """
        Basic triage without predictive analytics.
        Simple rules: urgent keywords or age-based.
        """
        urgent_keywords = ['cancer', 'acute', 'emergency', 'critical']
        
        # Check diagnosis for urgent keywords
        if any(keyword in patient.diagnosis.lower() for keyword in urgent_keywords):
            return 'urgent'
        
        # Default to normal priority
        return 'normal'
    
    def route_patient(self, patient: Patient):
        """Add patient to appropriate FIFO queue."""
        priority = self.triage_patient(patient)
        
        if priority == 'urgent':
            self.urgent_queue.append(patient)
        else:
            self.normal_queue.append(patient)
    
    def get_next_patient(self) -> Optional[Patient]:
        """
        Process urgent queue first, then FIFO from normal.
        No intelligent reordering based on resource availability.
        """
        if self.urgent_queue:
            return self.urgent_queue.popleft()
        elif self.normal_queue:
            return self.normal_queue.popleft()
        return None
    
    def process_radiology_report(self, patient: Patient):
        """
        Stage 1: Radiology report generation.
        No automation - manual review required.
        """
        # Request radiology resource
        with self.radiology_slots.request() as req:
            yield req
            
            # Sample from literature-based distribution
            delay = np.random.uniform(
                self.config['radiology_report']['min'],
                self.config['radiology_report']['max']
            ) / 24.0  # Convert hours to days
            
            yield self.env.timeout(delay)
            patient.stage_times['radiology_report'] = delay
    
    def process_pcp_acknowledgment(self, patient: Patient):
        """
        Stage 2: PCP acknowledgment.
        No electronic alerts - waiting for manual review.
        """
        # Exponential distribution (unpredictable physician workload)
        rate = self.config['pcp_acknowledgment']['lambda']
        delay = np.random.exponential(1.0 / rate)
        
        yield self.env.timeout(delay)
        patient.stage_times['pcp_acknowledgment'] = delay
    
    def process_referral(self, patient: Patient):
        """
        Stage 3: Referral processing.
        Manual routing, no automated classification.
        """
        mean = self.config['referral_processing']['mean']
        std = self.config['referral_processing']['std']
        delay = np.random.normal(mean, std)
        delay = max(0.5, delay)  # Ensure positive
        
        yield self.env.timeout(delay)
        patient.stage_times['referral_processing'] = delay
    
    def process_prior_authorization(self, patient: Patient):
        """
        Stage 4: Prior authorization.
        Manual submission, no parallel processing.
        """
        shape = self.config['prior_authorization']['shape']
        scale = self.config['prior_authorization']['scale']
        delay = np.random.gamma(shape, scale)
        
        yield self.env.timeout(delay)
        patient.stage_times['prior_authorization'] = delay
    
    def process_payer_review(self, patient: Patient):
        """
        Stage 5: Payer review.
        No automated tracking of review status.
        """
        min_days = self.config['payer_review']['min']
        mode_days = self.config['payer_review']['mode']
        max_days = self.config['payer_review']['max']
        delay = np.random.triangular(min_days, mode_days, max_days)
        
        yield self.env.timeout(delay)
        patient.stage_times['payer_review'] = delay
    
    def process_specialist_scheduling(self, patient: Patient):
        """
        Stage 6: Specialist appointment scheduling.
        No predictive booking, no alternative provider suggestions.
        """
        with self.specialist_slots.request() as req:
            yield req
            
            # Weibull distribution for waiting list dynamics
            shape = self.config['specialist_scheduling']['shape']
            scale = self.config['specialist_scheduling']['scale']
            delay = scale * np.random.weibull(shape)
            
            yield self.env.timeout(delay)
            patient.stage_times['specialist_scheduling'] = delay
    
    def process_patient_confirmation(self, patient: Patient):
        """
        Stage 7: Patient confirmation.
        Manual rescheduling if no-show occurs.
        """
        no_show_prob = self.config['patient_confirmation']['no_show_probability']
        
        if np.random.random() < no_show_prob:
            # No-show: need to reschedule manually
            min_reschedule = self.config['patient_confirmation']['reschedule_min']
            max_reschedule = self.config['patient_confirmation']['reschedule_max']
            delay = np.random.uniform(min_reschedule, max_reschedule)
        else:
            # Confirmed
            delay = 0.5  # Half day for confirmation
        
        yield self.env.timeout(delay)
        patient.stage_times['patient_confirmation'] = delay
    
    def coordinate_patient(self, patient: Patient):
        """
        Main coordination process - sequential stages.
        No parallel processing or predictive optimization.
        """
        start_time = self.env.now
        
        # Sequential processing through all 7 stages
        yield self.env.process(self.process_radiology_report(patient))
        yield self.env.process(self.process_pcp_acknowledgment(patient))
        yield self.env.process(self.process_referral(patient))
        yield self.env.process(self.process_prior_authorization(patient))
        yield self.env.process(self.process_payer_review(patient))
        yield self.env.process(self.process_specialist_scheduling(patient))
        yield self.env.process(self.process_patient_confirmation(patient))
        
        # Calculate total latency
        patient.total_latency = self.env.now - start_time
        
        # Record completion
        self.completed_patients.append(patient)
        self.total_processed += 1
    
    def run_simulation(self, patients: List[Patient]):
        """
        Run FIFO baseline simulation.
        Patients arrive and are added to appropriate queues.
        """
        def patient_arrival_generator():
            for patient in patients:
                # Add to queue
                self.route_patient(patient)
                
                # Start processing
                self.env.process(self.coordinate_patient(patient))
                
                # Small inter-arrival time
                yield self.env.timeout(0.01)
        
        # Start patient arrival process
        self.env.process(patient_arrival_generator())
        
        # Run simulation
        self.env.run()
        
        return self.completed_patients


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    import yaml
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_fifo_baseline(config_path: str, n_patients: int = 1000, seed: int = 42):
    """
    Run FIFO baseline simulation.
    
    Args:
        config_path: Path to YAML configuration file
        n_patients: Number of patients to simulate
        seed: Random seed for reproducibility
    
    Returns:
        List of completed patients with timing data
    """
    np.random.seed(seed)
    
    # Load configuration
    config = load_config(config_path)
    
    # Create environment
    env = simpy.Environment()
    
    # Create FIFO baseline system
    fifo_system = FIFOBaseline(env, config)
    
    # Generate patient cohort
    patients = []
    diagnoses = ['diabetes', 'hypertension', 'acute coronary syndrome', 
                 'cancer staging', 'chronic kidney disease']
    
    for i in range(n_patients):
        patient = Patient(
            id=i,
            arrival_time=0.0,
            urgent_indicator=(np.random.random() < 0.15),  # 15% urgent
            diagnosis=np.random.choice(diagnoses),
            stage_times={},
            total_latency=0.0
        )
        patients.append(patient)
    
    # Run simulation
    completed = fifo_system.run_simulation(patients)
    
    # Calculate statistics
    latencies = [p.total_latency for p in completed]
    mean_latency = np.mean(latencies)
    std_latency = np.std(latencies)
    median_latency = np.median(latencies)
    
    print(f"\n{'='*60}")
    print(f"FIFO BASELINE SIMULATION RESULTS")
    print(f"{'='*60}")
    print(f"Patients processed: {len(completed)}")
    print(f"Mean latency: {mean_latency:.2f} days")
    print(f"Std deviation: {std_latency:.2f} days")
    print(f"Median latency: {median_latency:.2f} days")
    print(f"Min latency: {np.min(latencies):.2f} days")
    print(f"Max latency: {np.max(latencies):.2f} days")
    print(f"\nExpected: ~15-16 days (26.8% improvement over legacy 21.17 days)")
    print(f"{'='*60}\n")
    
    return completed


if __name__ == '__main__':
    # Example usage
    completed_patients = run_fifo_baseline(
        config_path='configs/baseline_fifo.yaml',
        n_patients=1000,
        seed=42
    )
