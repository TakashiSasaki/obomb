from __future__ import unicode_literals, print_function
from com.gmail.takashi316.lib.sqlite import *
from com.gmail.takashi316.lib.file import *
from com.gmail.takashi316.lib.debug import *
from com.gmail.takashi316.lib.datetime import * 
from ConfigParser import ConfigParser
from com.gmail.takashi316.lib.sqlalchemy import *
SqlAlchemySessionFactory("obomb", "v1")
from unittest import TestCase