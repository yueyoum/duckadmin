VERSION = (0, 2, 0)
__version__ = '.'.join([str(i) for i in VERSION])


from duckadmin.forms import DuckForm
from duckadmin.admin import DuckAdmin
