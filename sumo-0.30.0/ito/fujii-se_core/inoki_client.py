from __future__ import division, print_function, absolute_import, unicode_literals

import socket
from contextlib import closing

if 'SE_HOME' in os.environ:

    tools = os.path.join(os.environ['SE_HOME'], 'tools')

    sys.path.append(tools)

    from infrastructure.shared.baseclient import BaseClient

else:

    sys.path.append("../")

    from infrastructure.shared.baseclient import BaseClient

class ParkingClient(BaseClient):
    



