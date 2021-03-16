# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from os.path import join, expanduser
import os.path
import psutil
from stat import S_ISREG, ST_MTIME, ST_MODE, ST_SIZE
from ovos_utils.signal import *
import os


def resolve_resource_file(res_name):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for ~/.mycroft/res_name first, and
    if not found will look at /opt/mycroft/res_name,
    then finally it will look for res_name in the 'mycroft/res'
    folder of the source code package.

    Example:
    With mycroft running as the user 'bob', if you called
        resolve_resource_file('snd/beep.wav')
    it would return either '/home/bob/.mycroft/snd/beep.wav' or
    '/opt/mycroft/snd/beep.wav' or '.../mycroft/res/snd/beep.wav',
    where the '...' is replaced by the path where the package has
    been installed.

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """
    # First look for fully qualified file (e.g. a user setting)
    if os.path.isfile(res_name):
        return res_name

    data_dir = expanduser("~/.tts")

    # Now look for ~/.tts/res_name (in user folder)
    filename = join(data_dir, res_name)
    if os.path.isfile(filename):
        return filename

    # Next look for ~/.tts/res/res_name
    filename = join(data_dir, "res", res_name)
    if os.path.isfile(filename):
        return filename

    # look in sounds folder
    sounds = ["wav", "mp3", "ogg"]
    if filename.split(".")[-1] in sounds:
        filename = join(data_dir, "res", "snd", res_name)
        if os.path.isfile(filename):
            return filename

    # look in text folder
    if filename.split(".")[-1] in ["txt", "md"]:
        filename = join(data_dir, "res", "text", res_name)
        if os.path.isfile(filename):
            return filename

    # look in media folder
    filename = join(data_dir, "res", "media", res_name)
    if os.path.isfile(filename):
        return filename

    return None  # Resource cannot be resolved


def remove_last_slash(url):
    if url and url.endswith('/'):
        url = url[:-1]
    return url


def curate_cache(directory, min_free_percent=5.0, min_free_disk=50):
    """Clear out the directory if needed

    This assumes all the files in the directory can be deleted as freely

    Args:
        directory (str): directory path that holds cached files
        min_free_percent (float): percentage (0.0-100.0) of drive to keep free,
                                  default is 5% if not specified.
        min_free_disk (float): minimum allowed disk space in MB, default
                               value is 50 MB if not specified.
    """

    # Simpleminded implementation -- keep a certain percentage of the
    # disk available.
    # TODO: Would be easy to add more options, like whitelisted files, etc.
    space = psutil.disk_usage(directory)

    # convert from MB to bytes
    min_free_disk *= 1024 * 1024
    # space.percent = space.used/space.total*100.0
    percent_free = 100.0 - space.percent
    if percent_free < min_free_percent and space.free < min_free_disk:
        LOG.info('Low diskspace detected, cleaning cache')
        # calculate how many bytes we need to delete
        bytes_needed = (min_free_percent - percent_free) / 100.0 * space.total
        bytes_needed = int(bytes_needed + 1.0)

        # get all entries in the directory w/ stats
        entries = (os.path.join(directory, fn) for fn in os.listdir(directory))
        entries = ((os.stat(path), path) for path in entries)

        # leave only regular files, insert modification date
        entries = ((stat[ST_MTIME], stat[ST_SIZE], path)
                   for stat, path in entries if S_ISREG(stat[ST_MODE]))

        # delete files with oldest modification date until space is freed
        space_freed = 0
        for moddate, fsize, path in sorted(entries):
            try:
                os.remove(path)
                space_freed += fsize
            except Exception:
                pass

            if space_freed > bytes_needed:
                return  # deleted enough!


def get_cache_directory(domain=None, base_path=None):
    """Get a directory for caching data

    This directory can be used to hold temporary caches of data to
    speed up performance.  This directory will likely be part of a
    small RAM disk and may be cleared at any time.  So code that
    uses these cached files must be able to fallback and regenerate
    the file.

    Args:
        domain (str): The cache domain.  Basically just a subdirectory.

    Return:
        str: a path to the directory where you can cache data
    """
    if not base_path:
        # If not defined, use /tmp/text2speech/cache
        base_path = os.path.join(tempfile.gettempdir(), "text2speech", "cache")
    return ensure_directory_exists(base_path, domain)

