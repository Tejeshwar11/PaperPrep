"""Exploratory finite transition model, not a vendor implementation.
Python 3.10+, no dependencies. Run: python3 extended_model.py > evidence/python_results.json
"""
from collections import deque
from dataclasses import dataclass,replace,asdict
import json
@dataclass(frozen=True)
class S:
    issued:int=0
    ack:int=0
    policy:int=0
    disk:int=0
    receipt:int=0
    conn:int=0
    alive:bool=True
    active:bool=False
    rebooted:bool=False
MODES=['local_ack','volatile_receipt','regressive_policy','session_bypass','protected']
def next_states(s,mode,limit):
    if s.alive and s.issued==s.ack and s.issued<limit:
        yield 'issue_epoch_'+str(s.issued+1),replace(s,issued=s.issued+1)
    for g in range(s.issued+1):
        if (mode=='regressive_policy' and g!=s.policy) or g>s.policy:
            yield 'deliver_policy_'+str(g),replace(s,policy=g,conn=-1)
    if s.policy>s.disk:
        yield 'persist_epoch_'+str(s.policy),replace(s,disk=s.policy)
    source=s.policy if mode=='volatile_receipt' else s.disk
    if s.alive and source>s.receipt:
        yield 'receive_receipt_'+str(source),replace(s,receipt=source)
    if s.alive and s.issued>s.ack and (mode=='local_ack' or s.receipt>=s.issued):
        yield 'acknowledge_epoch_'+str(s.issued),replace(s,ack=s.issued)
    for g in range(0,s.issued+1,2):
        if g!=s.conn and (mode=='session_bypass' or g==s.policy):
            yield 'deliver_session_'+str(g),replace(s,conn=g)
    if not s.rebooted:
        yield 'backup_restart_from_disk',replace(s,policy=s.disk,conn=0,rebooted=True)
    if s.alive and s.issued>0:
        yield 'primary_crash',replace(s,alive=False)
    if not s.alive and not s.active:
        yield 'backup_takeover',replace(s,active=True)
def admit(s,mode):
    if s.active:
        return s.conn>=0 if mode=='session_bypass' else s.policy%2==0 and s.conn==s.policy
    return s.alive and s.issued%2==0
def safe(s,mode):
    return not(s.ack%2==1 and s.issued==s.ack and admit(s,mode))
def trace(s,parent):
    out=[]
    while parent[s] is not None:
        s,event=parent[s];out.append(event)
    return out[::-1]
def run(mode,limit):
    start=S();q=deque([start]);parent={start:None};bad=[];edges=0;ack3=0;allow2=0;first_allow=None
    while q:
        s=q.popleft()
        if mode=='protected':assert s.ack<=s.receipt<=s.disk<=s.policy<=s.issued
        if not safe(s,mode):bad.append(s)
        if s.active and s.ack==3:ack3+=1
        if s.active and s.issued==s.ack==2 and admit(s,mode):
            allow2+=1
            if first_allow is None:first_allow=s
        for event,t in next_states(s,mode,limit):
            edges+=1
            if t not in parent:parent[t]=(s,event);q.append(t)
    return dict(mode=mode,max_epoch=limit,reachable_states=len(parent),transitions=edges,
        violating_states=len(bad),acknowledged_second_revocation_takeover_states=ack3,
        authorized_epoch2_takeover_states=allow2,
        shortest_counterexample=trace(bad[0],parent) if bad else None,
        counterexample_state=asdict(bad[0]) if bad else None,
        authorized_reuse_witness=trace(first_allow,parent) if first_allow else None)
def main():
    rows=[run(m,k) for k in [1,2,3,5,7] for m in MODES]
    for r in rows:
        assert (r['violating_states']==0)==(r['mode']=='protected')
        if r['max_epoch']>=2:assert r['authorized_epoch2_takeover_states']>0
        if r['max_epoch']==3:assert r['acknowledged_second_revocation_takeover_states']>0
    print(json.dumps({'scope':'one mutable target, one implicit unaffected control flow; even epochs allow, odd epochs deny, bounds 1/2/3/5/7; one primary crash, one atomic backup restart; authentic replayable messages; no split brain','results':rows},indent=2))
if __name__=='__main__':main()
