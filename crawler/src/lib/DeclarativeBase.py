from config import *
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
DeclarativeBase = _declarative_base(metadata=_MetaData())
