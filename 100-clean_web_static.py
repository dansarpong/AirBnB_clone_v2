#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive
from the contents of the web_static folder"""

import os
from fabric.api import *
from datetime import datetime


env.hosts = ['18.234.107.21', '18.210.17.1']


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


def do_deploy(archive_path):
    """
    deploys the static files to the host servers
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    path = do_pack()
    return do_deploy(path) if path else False


def do_clean(number=0):
    """
    deletes out-of-date archives
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    number = 1 if int(number) == 0 else int(number)
    start = number
    
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
