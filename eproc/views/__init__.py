"""
Package initialization for eproc.views.
Exposes all view functions from sub-modules to maintain 100% backward
compatibility with eproc/urls.py and global imports.
"""

from .dashboard_views import *
from .setup_views import *
from .purchase_views import *
from .inventory_views import *
from .damage_return_views import *
from .fuel_views import *
from .fleet_views import *
from .maintenance_views import *
from .report_views import *
from .notification_views import *