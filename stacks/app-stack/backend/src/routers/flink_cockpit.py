import os

from fastapi import APIRouter, HTTPException
from typing import List
from models.flink import FlinkJob, FlinkJobException
import requests

FLINK_REST_URL = os.getenv('FLINK_REST_URL')

router = APIRouter(tags=["Flink Cockpit"])

@router.get("/flink-cockpit/jobs", response_model=List[FlinkJob])
def list_jobs():
    resp = requests.get(f"{FLINK_REST_URL}/jobs/overview")
    jobs = resp.json()["jobs"]
    return [FlinkJob(
        id=job["jid"],
        name=job["name"],
        state=job["state"],
        start_time=job.get("start-time")
    ) for job in jobs]

@router.post("/flink-cockpit/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    resp = requests.patch(f"{FLINK_REST_URL}/jobs/{job_id}", json={"state": "CANCELED"})
    if resp.status_code != 202:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"status": "cancelled"}

@router.get("/flink-cockpit/jobs/{job_id}/exceptions", response_model=FlinkJobException)
def job_exceptions(job_id: str):
    resp = requests.get(f"{FLINK_REST_URL}/jobs/{job_id}/exceptions")
    return FlinkJobException(**resp.json())

@router.get("/flink-cockpit/jobs/{job_id}/details")
def job_details(job_id: str):
    resp = requests.get(f"{FLINK_REST_URL}/jobs/{job_id}")
    return resp.json() 