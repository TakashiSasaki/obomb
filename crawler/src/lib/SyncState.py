from config import *
from sqlalchemy import Column, Integer, String, DateTime
from lib.DeclarativeBase import DeclarativeBase
from lib.GvizDataTableMixin import GvizDataTableMixin
from lib.TableMixin import TableMixin
from uuid import uuid1

class SyncState(DeclarativeBase, GvizDataTableMixin, TableMixin):
    __tablename__ = "SyncState" 
    stateUuid = Column(String, primary_key=True, index=True, nullable=False)
    lockBegin = Column(DateTime, nullable = False)
    lockEnd = Column(DateTime, nullable = True)
    stateBeforeLock = Column(String, nullable = False)
    stateAfterLock = Column(String, nullable = True)
    agetnId = Column(String, nullable = True)
    userName = Column(String, nullable = True)
    userDomain = Column(String, nullable = True)

    def __init__(self):
        self.stateUuid = uuid1().get_hex()
    
    def setLockBegin(self, lock_begin = None):
        if lock_begin is None:
            lock_begin = utcnow()
        self.lockBegin = lock_begin
    
    def setLockEnd(self, lock_end = None):
        if lock_end is None:
            lock_end = utcnow()
        self.lockEnd = lock_end
    
    def setStateBeforeLock(self, state_before_lock = None):
        if state_before_lock is None:
            state_before_lock = uuid1().get_hex()
        assert isinstance(state_before_lock, str)
        self.stateBeforeLock = state_before_lock
        
    def setStateAfterLock(self, state_after_lock = None):
        if state_after_lock is None:
            state_after_lock = uuid1().get_hex()
        assert isinstance(state_after_lock, str)
        self.stateAfterLock = state_after_lock
        
    @classmethod
    def getLast(cls, limit=1):
        query = cls.getQuery()
        query = query.order_by(cls.lockBegin.desc()).limit(limit)
        return query.all()
        

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        
    def testGeenrateDummyRows(self):
        count_before = SyncState.count()
        session = Session()
        for x in ["a", "b", "c", "d"]:
            sync_state = SyncState()
            sync_state.setStateBeforeLock(x + uuid1().get_hex())
            sync_state.setLockBegin()
            sync_state.setLockEnd()
            sync_state.setStateAfterLock(x + uuid1().get_hex())
            session.add(sync_state)
        session.commit()
        session.close()
        count_after = SyncState.count()
        self.assertEqual(count_before + 4, count_after)
        
    def testGetLast(self):
        last = SyncState.getLast(2)
        self.assertIsInstance(last, list)
        self.assertEqual(len(last), 2)
        self.assertGreaterEqual(last[0].lockBegin, last[1].lockBegin)

    def tearDown(self):
        TestCase.tearDown(self)

if __name__ == "__main__":
    main()
