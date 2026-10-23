"""Kira numerical substrate: exact rational coordinates, no graph primitives.
Identity is opaque and independent of numeric coordinates. Sorted range index is a
specialized optimization, not an assumed spatial topology.
"""
import sqlite3
from bisect import bisect_left, bisect_right, insort
from fractions import Fraction


def rational(value):
    if isinstance(value, Fraction): return value
    if isinstance(value, (int, str)): return Fraction(value)
    raise TypeError('use int, Fraction or decimal/rational string; floats rejected')


class NumericCore:
    def __init__(self, path=':memory:'):
        self.db=sqlite3.connect(path)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('CREATE TABLE IF NOT EXISTS numeric_items (id INTEGER PRIMARY KEY, numerator TEXT NOT NULL, denominator TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS numeric_evidence (item_id INTEGER NOT NULL REFERENCES numeric_items(id), source TEXT NOT NULL, numerator TEXT NOT NULL, denominator TEXT NOT NULL, count INTEGER NOT NULL DEFAULT 1, PRIMARY KEY(item_id,source,numerator,denominator))')
        self.db.commit()
        self._ordered=[]
        for identity,num,den in self.db.execute('SELECT id,numerator,denominator FROM numeric_items'):
            insort(self._ordered,(Fraction(int(num),int(den)),identity))

    def observe(self, value, identity=None, source='observed'):
        """Persist one observation. Existing identity can acquire additional evidence;
        its indexed representative stays stable until explicitly revised.
        """
        v=rational(value)
        with self.db:
            if identity is None:
                cur=self.db.execute('INSERT INTO numeric_items(numerator,denominator) VALUES (?,?)',(str(v.numerator),str(v.denominator)))
                identity=cur.lastrowid
                insort(self._ordered,(v,identity))
            elif not self.db.execute('SELECT 1 FROM numeric_items WHERE id=?',(identity,)).fetchone():
                raise KeyError(identity)
            self.db.execute('INSERT INTO numeric_evidence(item_id,source,numerator,denominator,count) VALUES (?,?,?,?,1) ON CONFLICT(item_id,source,numerator,denominator) DO UPDATE SET count=count+1',(identity,source,str(v.numerator),str(v.denominator)))
        return identity

    def value(self,identity):
        row=self.db.execute('SELECT numerator,denominator FROM numeric_items WHERE id=?',(identity,)).fetchone()
        if row is None: raise KeyError(identity)
        return Fraction(int(row[0]),int(row[1]))

    def range(self, value, tolerance):
        """Exact numerical range query O(log n + k) on the in-memory sorted index.
        O(n) insertion due to Python list shifts; index occupies O(n) RAM.
        """
        x,t=rational(value),rational(tolerance)
        if t<0: raise ValueError('negative tolerance')
        lo=bisect_left(self._ordered,(x-t,-1))
        hi=bisect_right(self._ordered,(x+t,float('inf')))
        return [(identity,v) for v,identity in self._ordered[lo:hi]]

    def evidence(self,identity):
        return [(src,Fraction(int(n),int(d)),cnt) for src,n,d,cnt in self.db.execute('SELECT source,numerator,denominator,count FROM numeric_evidence WHERE item_id=? ORDER BY source,numerator,denominator',(identity,))]

    def close(self): self.db.close()
