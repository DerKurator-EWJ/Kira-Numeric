import tempfile,time,statistics,json,sqlite3
from pathlib import Path
from efficient_core import EfficientCore
from prediction import TransitionPredictor
from binary_learning import BinaryLearningRuntime

def graph(rel):return {'nodes':{'a':'thing','b':'thing'},'edges':[['a',rel,'b']]}

def run(kind,n=80):
    with tempfile.TemporaryDirectory() as tmp:
        path=str(Path(tmp)/'db.sqlite')
        start=time.perf_counter()
        if kind=='specialized':
            db=sqlite3.connect(path);p=TransitionPredictor(db,'token:s',max_context=1)
            h=[]
            for i in range(n):p.record(i,h[-1:],i%2);h.append(i%2)
            db.commit()
        elif kind=='rrm':
            r=BinaryLearningRuntime(path)
            for i in range(n):r.observe('graph:s',graph('cold' if i%2==0 else 'warm'))
        else:
            r=EfficientCore(path)
            for i in range(n):r.observe('s',i%2 if kind=='routed_token' else graph('cold' if i%2==0 else 'warm'))
        train=time.perf_counter()-start
        start=time.perf_counter()
        if kind=='specialized':res=p.distribution([0]);ok=res['predictions'][0]['token']==1
        elif kind=='rrm':res=r.predict('graph:s',graph('cold'));ok=res['status']=='HYPOTHESIS'
        elif kind=='routed_token':res=r.predict('s',0);ok=res['predictions'][0]['token']==1
        else:res=r.predict('s',graph('cold'));ok=res['status']=='HYPOTHESIS'
        inference=time.perf_counter()-start
        if kind=='specialized':db.close()
        else:r.close()
        return {'train_ms':round(train*1000,3),'predict_ms':round(inference*1000,3),'db_bytes':Path(path).stat().st_size,'correct':ok}

if __name__=='__main__':
    output={k:[run(k) for _ in range(5)] for k in ('specialized','routed_token','rrm','routed_graph')}
    print(json.dumps(output,indent=2));Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2))
