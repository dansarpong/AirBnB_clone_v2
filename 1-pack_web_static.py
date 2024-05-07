#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive
from the contents of the web_static folder"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """
    generates .tgz archive from the contents of the web_static folder
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(now)

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None
