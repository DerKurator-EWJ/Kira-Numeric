import tempfile,unittest
from pathlib import Path
from efficient_core import EfficientCore

def graph(rel,a='a',b='b'):
    return {'nodes':{a:'thing',b:'thing'},'edges':[[a,rel,b]]}

class Tests(unittest.TestCase):
    def test_routing_persistence_and_transfer(self):
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'kira.sqlite')
            k=EfficientCore(path)
            for i in range(12):
                self.assertEqual(k.observe('words',i%2)['route'],'token')
                k.observe('scene',graph('cold' if i%2==0 else 'warm'))
            self.assertEqual(k.predict('words',0)['predictions'][0]['token'],1)
            self.assertEqual(k.predict('scene',graph('cold','x','y'))['result']['edges'][0][1],'warm')
            k.close()
            k=EfficientCore(path)
            self.assertEqual(k.predict('words',0)['predictions'][0]['token'],1)
            self.assertEqual(k.predict('scene',graph('cold','x','y'))['result']['edges'][0][1],'warm')
            self.assertEqual(k.observe('words',0)['tick'],12)
            k.close()
    def test_reject_unknown(self):
        k=EfficientCore()
        with self.assertRaises(TypeError): k.observe('s','hello')
        with self.assertRaises(TypeError): k.predict('s',True)
        k.close()
    def test_stream_separation(self):
        k=EfficientCore()
        for _ in range(4):
            for t in [0,1]:k.observe('a',t)
            for t in [0,2]:k.observe('b',t)
        self.assertEqual(k.predict('a',0)['predictions'][0]['token'],1)
        self.assertEqual(k.predict('b',0)['predictions'][0]['token'],2)
        k.close()
if __name__=='__main__':unittest.main()
