# -*- coding: utf-8 -*-
#
# File: Announcement.py
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

from types import StringType
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.Archetypes import BaseObject
from Products.Announcements.config import *
from zope.interface import implements
from interfaces import IAnnouncement
from Products.ATContentTypes.atct import ATEvent
from Products.ATContentTypes.content.event import ATEventSchema
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

# import Plone translation:
from Products.CMFPlone.i18nl10n import utranslate

##code-section module-header #fill in your manual code here
##/code-section module-header

# copy and customize default fields from the ATEvent schema:
copied_fields = {}
copied_fields['title'] = ATEvent.schema['title'].copy()
copied_fields['title'].widget.label= "Event Name"
copied_fields['title'].widget.description = "Enter a brief but descriptive title for the anouncement or event."
copied_fields['title'].widget.description_msgid = "description_announcement_title"
copied_fields['title'].required = 1
copied_fields['title'].searchable = 1
copied_fields['title'].visible = {'view': 'hidden', 'edit': 'visible'},
copied_fields['description'] = ATEvent.schema['description'].copy()
copied_fields['description'].widget.description = "Enter a brief description of the announcement or event (you will add details later)."
copied_fields['description'].widget.description_msgid = "description_announcement_description"
copied_fields['description'].widget.rows = 2
copied_fields['description'].required = 1
copied_fields['description'].searchable = 1
# description field isn't showing up on object or in email; trying to "un-hide" it here:
#copied_fields['description'].widget.visible = {"view" : "visible"}
copied_fields['description'].visible = {'view': 'visible', 'edit': 'visible'},
copied_fields['text'] = ATEvent.schema['text'].copy()
copied_fields['text'].required = 1
copied_fields['text'].searchable = 1
#copied_fields['text'].widget = TextAreaWidget
copied_fields['text'].widget.label = "Event Detail"
copied_fields['text'].widget.description = "Enter a detailed description of the event."
copied_fields['text'].widget.description_msgid = "description_announcement_text"
copied_fields['text'].widget.rows = 8
#copied_fields['text'].validators = ('isTidyHtmlWithCleanup')
copied_fields['startDate'] = ATEvent.schema['endDate'].copy()
copied_fields['startDate'].widget.label= "Event Start Date and Time"
copied_fields['startDate'].widget.description = "Enter the start time and date of the event."
copied_fields['startDate'].widget.description_msgid = "description_announcement_start_time"
copied_fields['endDate'] = ATEvent.schema['endDate'].copy()
copied_fields['endDate'].widget.label= "Event End Date and Time"
copied_fields['endDate'].widget.description = "Enter the anticipated end time and date of the event."
copied_fields['endDate'].widget.description_msgid = "description_announcement_end_time"

AnnouncementSchema = ATEventSchema.copy() + Schema((
    
    #A brief but descriptive title for the announcement or event.
    copied_fields['title'],
#    StringField(
#        name='title',
#        widget=StringWidget(
#            label="Announcement Title",
#            description="Enter a brief but descriptive title for the anouncement or event.",
#            label_msgid='Announcements_label_title',
#            description_msgid='Announcements_help_title',
#            i18n_domain='Announcements',
#            visible={'view': 'hidden', 'edit': 'visible'},
#        ),
#        required=1,
#        accessor="Title",
#        searchable=1,
#    ),
    
    #A short description of the event.
    copied_fields['description'],
    
    #The start time and date of the event.
    copied_fields['startDate'],
    
    #The anticipated time and date of completion of the event.
    copied_fields['endDate'],
    
    #The name of the group responsible for the event.
    StringField(
        name='groupResponsible',
        widget=SelectionWidget(
            label="Group Responsible",
            description="Choose the name of the group responsible for the event.",
            label_msgid='Announcements_label_groupResponsible',
            description_msgid='Announcements_help_groupResponsible',
            i18n_domain='Announcements',
        ),
        required=1,
        vocabulary=["-- please select one value --",
                    "Central Storage",
                    "Databases",
                    "Farms",
                    "General Computing Environment",
                    "Grid Middleware",
                    "Mass Storage",
                    "Operations & Infrastructure",
                    "Software Environment & Development",
                    "Storage Management & Data Movement",
                    "RACF"],
        enforceVocabulary=True,
    ),
    
    #The facility areas or services impacted by this event.
    LinesField(
        name='affectedArea',
        widget=InAndOutWidget(
            label="Affected Area",
            description="Enter the facility areas or services impacted by this event.",
            label_msgid='Announcements_label_affectedArea',
            description_msgid='Announcements_help_affectedArea',
            i18n_domain='Announcements',
			size=7,
        ),
        required=1,
        multiValued=1,
        vocabulary=["Data Movement",
                    "Data Storage",
                    "Databases",
                    "Linux Farm",
                    "Shared Storage",
                    "Web",
                    "Other"],
        enforceVocabulary=True,
    ),
    
    #Terms that describe the nature of the event.
    LinesField(
        name='eventType',
        widget=InAndOutWidget(
            label="Type of Event",
            description="Choose one or more terms that describe the nature of the event (meeting, upgrade, etc.), and the affected experiment group(s).",
            label_msgid='Announcements_label_eventType',
            description_msgid='Announcements_help_eventType',
            i18n_domain='Announcements',
			size=7,
        ),
        required=1,
        multiValued=1,
        vocabulary=["Meeting or Workshop",
                    "Hardware Upgrade",
                    "Software Upgrade",
                    "Planned Downtime",
                    "Unplanned Downtime",
                    "Transparent Intervention",
                    "Other"],
        enforceVocabulary=True,
    ),
    
    #Experiment groups affected by the event.
    LinesField(
        name='experiments',
        widget=InAndOutWidget(
            label="Affected Experiments",
            description="Choose one or more experiment groups that may be affected by the event.",
            label_msgid='Announcements_label_experiments',
            description_msgid='Announcements_help_experiments',
            i18n_domain='Announcements',
        ),
        required=1,
        multiValued=1,
        vocabulary=["ATLAS",
                    "LSST",
                    "RHIC",
                    "None",
                    "Other"],
        enforceVocabulary=True,
    ),
    
    #A detailed description of the event.
    copied_fields['text'],
    
    #The mailing lists to which an announcement is sent.
    LinesField(
        name='mailingList',
        widget=InAndOutWidget(
            label="Announcement Mailing Lists",
            description="Choose one of more mailing lists to which this announcement should be sent.",
            label_msgid='Announcements_label_mailingList',
            description_msgid='Announcements_help_mailingList',
            i18n_domain='Announcements',
			size=10,
        ),
        label="Groups Notified",
        required=1,
        multiValued=1,
        vocabulary=DisplayList((
		   ('atlas-project-adc-operations@cern.ch','atlas-project-adc-operations'),
		   ('rhic-rcf-l@lists.bnl.gov','rhic-rcf-l'),
		   ('racf-wlcg-announce-l@lists.bnl.gov','racf-wlcg-announce-l'),
		   ('usatlas-computing-l@lists.bnl.gov','usatlas-computing-l'),
		   ('usatlas-ddm-l@lists.bnl.gov','usatlas-ddm-l'),
		   ('usatlas-grid-l@lists.bnl.gov','usatlas-grid-l'),
		   ('usatlas-prodsys-l@lists.bnl.gov','usatlas-prodsys-l'),
		   ('usatlas-users-l@lists.bnl.gov','usatlas-users-l'),
		   ('rcfstaff@bnl.gov','RACF Staff'),
                   ('jd@bnl.gov','John at BNL [test]'),
		   )),
        enforceVocabulary=True,
    ),

),
)

# remove the unused, default Event fields (this type uses custom fields instead):
AnnouncementSchema['location'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['location'].mode='r'
AnnouncementSchema['eventUrl'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['eventUrl'].mode='r'
AnnouncementSchema['contactName'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['contactName'].mode='r'
AnnouncementSchema['contactEmail'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['contactEmail'].mode='r'
AnnouncementSchema['contactPhone'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['contactPhone'].mode='r'
AnnouncementSchema['attendees'].widget.visible={'edit': 'hidden', 'view': 'invisible'}
AnnouncementSchema['attendees'].mode='r'
# description field isn't showing up on object or in email; trying to "un-hide" it here:
AnnouncementSchema['description'].widget.visible = {"view" : "visible"}

finalizeATCTSchema(AnnouncementSchema)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Announcement(ATEvent):
    """A facility announcement object.
    """
    security = ClassSecurityInfo()
    implements(IAnnouncement)
    
    # This name appears in the 'add' box:
    archetype_name = 'Facility Announcement'
    meta_type = 'Announcement'
    portal_type = 'Announcement'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'announcement-small.gif'
#    content_icon = 'announcement.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Announcement"
    typeDescMsgId = 'description_edit_announcement'
    _at_rename_after_creation = True
    schema = AnnouncementSchema
    _at_creation_flag = True
    
    ##code-section class-header #fill in your manual code here
    ##/code-section class-header
    
    # Methods

def at_post_create_script(self, obj):
    obj.unmarkCreationFlag()

registerType(Announcement, PROJECTNAME)
# end of class Announcement

##code-section module-footer #fill in your manual code here
##/code-section module-footer
