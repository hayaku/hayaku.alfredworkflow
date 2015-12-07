#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2015 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-11-26
#

"""
Post notifications via the OS X Notification Center.
"""

from __future__ import print_function, unicode_literals

import os
import subprocess


import workflow


_wf = None
_log = None


def wf():
    """Return `Workflow` object for this module.

    Returns:
        workflow.Workflow: `Workflow` object for current workflow.
    """
    global _wf
    if _wf is None:
        _wf = workflow.Workflow()
    return _wf


def log():
    """Return logger for this module.

    Returns:
        logging.Logger: Logger for this module.
    """
    global _log
    if _log is None:
        _log = wf().logger
    return _log


def notifier_program():
    """Return path to notifier applet executable.

    Returns:
        unicode: Path to Notify.app `applet` executable.
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'extras',
        'Notify.app',
        'Contents',
        'MacOS',
        'applet')


def notify(title='', text='', sound=''):
    """Post notification via Notify.app helper.

    Args:
        title (str, optional): Notification title.
        text (str, optional): Notification body text.
        sound (str, optional): Name of sound to play.

    Raises:
        ValueError: Raised if both `title` and `text` are empty.

    Returns:
        bool: `True` if notification was posted, else `False`.
    """
    if title == text == '':
        raise ValueError('Empty notification')

    n = notifier_program()
    env = os.environ.copy()
    env['NOTIFY_TITLE'] = title
    env['NOTIFY_MESSAGE'] =  text
    env['NOTIFY_SOUND'] = sound
    cmd = [n]
    p = subprocess.Popen(cmd, env=env)
    p.wait()
    if p.returncode == 0:
        return True
    log().error('Notify.app exited with status {0}.'.format(p.returncode))
    return False


# def notify_native(title='', text='', sound=''):
#     """Post notification via the native API (via pyobjc).

#     At least one of `title` or `text` must be specified.

#     This method will *always* show the Python launcher icon (i.e. the
#     rocket with the snakes on it).

#     Args:
#         title (str, optional): Notification title.
#         text (str, optional): Notification body text.
#         sound (str, optional): Name of sound to play.

#     """

#     if title == text == '':
#         raise ValueError('Empty notification')

#     import Foundation

#     sound = sound or Foundation.NSUserNotificationDefaultSoundName

#     n = Foundation.NSUserNotification.alloc().init()
#     n.setTitle_(title)
#     n.setInformativeText_(text)
#     n.setSoundName_(sound)
#     nc = Foundation.NSUserNotificationCenter.defaultUserNotificationCenter()
#     nc.deliverNotification_(n)


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('--title', help="Notiication title.", default='')
    p.add_argument('--text', help="Notification body text.", default='')
    p.add_argument('--sound', help="Optional sound.", default='')
    o = p.parse_args()
    print(repr(o))

    if o.title == o.text == '':
        log().error('Empty notification.')
    else:
        notify(o.title, o.text, o.sound)
