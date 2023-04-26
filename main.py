from fastapi import FastAPI
from typing import List
from yandex_tracker_client import TrackerClient
from dotenv import load_dotenv
from pydantic import BaseModel
from isodate import parse_duration
import os

load_dotenv()

app = FastAPI()
client = TrackerClient(token=os.getenv('TOKEN'), org_id=os.getenv('ORG_ID'))

class Worklog(BaseModel):
    staff: str
    issue_name: str
    issue_key: str
    duration: str

@app.get('/test_task', response_model=List[Worklog])
def issues():
    worklog_list = []
    issues = client.issues.get_all()
    for issue in issues:
        worklog = issue.worklog.get_all()
        for w in worklog:
            worklog_list.append({
                'staff': '{} {}'.format(w.createdBy.firstName, w.createdBy.lastName),
                'issue_name': str(w.issue.summary),
                'issue_key': str(w.issue.key),
                'duration': str(parse_duration(w.duration))})
    return [worklog for worklog in worklog_list]
