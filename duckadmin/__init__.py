VERSION = (0, 1, 2)
__version__ = '.'.join([str(i) for i in VERSION])


from duckadmin.forms import DuckForm
from duckadmin.admin import DuckAdmin
