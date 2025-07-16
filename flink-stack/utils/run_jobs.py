#!/usr/bin/env python3
"""
Job runner for Flink streaming jobs
"""

import sys
import os
import time
import importlib.util
from pathlib import Path

def load_job_module(job_file):
    """Dynamically load a job module"""
    try:
        spec = importlib.util.spec_from_file_location("job_module", job_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading job module {job_file}: {e}")
        return None

def run_job(job_name):
    """Run a specific Flink job"""
    job_file = Path(__file__).parent / f"{job_name}.py"
    
    if not job_file.exists():
        print(f"Job file {job_file} not found!")
        return False
    
    print(f"Running job: {job_name}")
    print(f"Job file: {job_file}")
    
    try:
        # Load and run the job
        module = load_job_module(job_file)
        if module:
            print(f"Job {job_name} started successfully!")
            return True
        else:
            print(f"Failed to load job {job_name}")
            return False
    except Exception as e:
        print(f"Error running job {job_name}: {e}")
        return False

def list_available_jobs():
    """List all available job files"""
    src_dir = Path(__file__).parent
    job_files = list(src_dir.glob("*_job.py"))
    
    print("Available jobs:")
    for job_file in job_files:
        job_name = job_file.stem
        print(f"  - {job_name}")
    
    return [job.stem for job in job_files]

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python run_jobs.py <job_name>")
        print("Available jobs:")
        list_available_jobs()
        sys.exit(1)
    
    job_name = sys.argv[1]
    
    if job_name == "list":
        list_available_jobs()
        return
    
    if job_name == "all":
        # Run all jobs
        available_jobs = list_available_jobs()
        for job in available_jobs:
            print(f"\n{'='*50}")
            print(f"Running {job}")
            print(f"{'='*50}")
            success = run_job(job)
            if not success:
                print(f"Job {job} failed!")
            time.sleep(2)  # Small delay between jobs
    else:
        # Run specific job
        success = run_job(job_name)
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main() 