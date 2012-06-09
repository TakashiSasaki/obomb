from config import *
import lib
import time

class TableMixin(object):

    def getTableMixin(self):
        assert issubclass(self.table, lib.DeclarativeBase.DeclarativeBase)
        assert issubclass(self.table, lib.GvizDataTableMixin.GvizDataTableMixin)
        assert issubclass(self.table, lib.TableMixin.TableMixin)
        
        if self.request.path_info == "" or self.request.path_info == "/":
            session = Session()
            try:
                data_table = self.table.getGvizDataTable(session)
                session.close()
                self.response.set_status(200)
                self.response.expires = time.time()
                tqx = self.request.GET["tqx"]
                self.response.out.write(data_table.ToResponse(tqx=tqx))
            except Exception, e:
                self.response.set_status(500)
                assert len(e.message) > 0
                self.response.out.write(e.message)
            return True

        if self.request.path_info == "/create":
            try:
                self.table.create()
                self.response.set_status(200)
                self.response.out.write("%s.createTable" % self.table.getTable())
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True
        
        if self.request.path_info == "/drop":
            try:
                self.table.drop()
                self.response.set_status(200)
                self.response.out.write("%s.dropTable" % self.table.getTable())
            except Exception,e :
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True

        if self.request.path_info == "/dummy":
            try:
                self.table.dummy()
                self.response.set_status(200)
                self.response.out.write("%s.insertDummyRecords" % self.table.getTable())
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True
        return False
