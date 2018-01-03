# -*- coding: utf-8 -*-
#
# File: AnnouncementsFolder.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 1.5.2
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """John DeStefano <jd (at) bnl (dot) gov>"""
__docformat__ = 'plaintext'

import transaction

# import Zope tools:
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.Announcements.config import *

# import content types:
from Products.ATContentTypes.content.folder import ATFolderSchema, ATFolder
from Products.ATContentTypes.content.event import ATEventSchema, ATEvent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFolder, IATEvent, ICalendarSupport

# import Plone translation:
from Products.CMFPlone.i18nl10n import utranslate

##code-section module-header #fill in your manual code here
##/code-section module-header

#schema = Schema((
#
#),
#)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AnnouncementsFolderSchema = ATFolderSchema.copy() + Schema(())

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AnnouncementsFolderMeta(type):
    def __init__(self, name, bases, attrs):
        cls = super(AnnouncementsFolderMeta, self).__init__(name, bases, attrs)
        if cls.platform is not None:
            register_announcementsfolder_implementation(klass.platform, cls)
        return cls

class AnnouncementsFolder(ATFolder):
    """A folder that contains all site Announcement objects."""
    schema = AnnouncementsFolderSchema
    _at_rename_after_creation = True
    # This name appears in the 'add' box
    archetype_name = 'Announcements Folder'
    typeDescription = "A container for site Announcements."
    typeDescMsgId = 'description_edit_announcementsfolder'
    # Enable marshalling via WebDAV/FTP/ExternalEditor:
    __dav_marshall__ = True

    assocMimetypes = ()
    assocFileExt   = ()
    cmf_edit_kws   = ()

    meta_type = portal_type = 'AnnouncementsFolder'
    allowed_content_types = ['Announcement','CalendarX','Topic']
#    filter_content_types = 1
#    global_allow = 1
#    content_icon = 'AnnouncementsFolder.gif'
    default_view = 'base_view'
    immediate_view = 'base_view'
    suppl_views = ('folder_summary_view', 'folder_tabular_view', 'atct_album_view', 'atct_topic_view')

    transaction.savepoint()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

finalizeATCTSchema(AnnouncementsFolderSchema, folderish=True, moveDiscussion=False)

    # Methods

registerType(AnnouncementsFolder, PROJECTNAME)

# end of class AnnouncementsFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer
