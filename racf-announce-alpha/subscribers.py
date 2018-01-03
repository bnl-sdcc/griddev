# -*- coding: utf-8 -*-

def isEventTransitionOk(obj, event):
    """check for non-existing state (new objects)."""
    if event.transition is not None:
        return event.transition
    else:
        return False

def isObjectTypeOk(obj, event):
    """check for non-existing type (new objects)."""
    if obj.portal_type is not None:
        return obj.portal_type
    else:
        return False

def portalMessageModifier(obj, event):
    """custom portal info reminder message;
       this should fire *only* on unpublished announcement objects."""
    ##parameters=state_change
    from Products.CMFCore.utils import getToolByName
    from Products.Archetypes.interfaces import IObjectInitializedEvent,IObjectEditedEvent
    putils = getToolByName(obj, 'plone_utils')
    
    # this condition should catch any *new* announcement object in the process 
    # of being created:
    if obj.portal_type=='Announcement' and obj.checkCreationFlag():
#    if obj.checkCreationFlag() and event.transition:
        mymessage=(u"Please note: after you create this announcement, please remember to review and *Publish* it. Email notification will *not* be sent until you change the State of your announcement to *Published*!")
        putils.addPortalMessage(mymessage)

    # this condition should catch any *existing* announcement object that
    # has not been published:
    elif obj.portal_type=='Announcement' and event.transition and event.transition_id != 'publish':
        mymessage=(u"Please note: this announcement has been created, but email notification will *not* be sent until you change the State of your announcement to *Published*!")
        putils.addPortalMessage(mymessage)

    # this message should be displayed *only* when an announcement object is published:
    elif event.transition and event.transition_id == 'publish':
        mymessage=(u"Thank you. This announcement has been published via email to the specified lists.")
        putils.addPortalMessage(mymessage)

    # finally, if the object is not an announcement, *or* if no transition has occured,
    # *or* the object is in the process of being created, nothing should happen!
    else:
        return

def emailListListener(obj, event):
    """object state change subscriber; sends email to selected lists; fires on publish."""
    if not event.transition or \
        event.transition_id != 'publish':
        return  

    ##parameters=state_change

    # get membership info and the mailhost from the server:
    from Products.CMFCore.utils import getToolByName
#    mship = obj.portal_membership
    mship = getToolByName(obj,'portal_membership')
    mhost = obj.MailHost

    # get member's email address:
#    from Products.CMFCore.utils import getToolByName
    mymemberinfo = getToolByName(obj,'portal_membership')
    mymember = mymemberinfo.getAuthenticatedMember()
    memail = mymember.getProperty('email') 

    # set the 'from' address:
    emailFrom = 'RACF Facility Announcements <announce@rcf.rhic.bnl.gov>'
    # grab the object title and set the subject:
    emailSubject = "RACF Facility Announcement: " + obj.Title()

    # get the list of To: addresses from the mailingList:
    emailToList = obj.getMailingList()
    # check for member's email in the email list:
    to_list = list(emailToList)
    if not memail in to_list:
        to_list.append(memail)

    # get the other object values:
    # 
    # get the description field: description is in unicode; decode to UTF8 1st:
    rawDescription = obj.Description().encode('utf-8') 
    # affectedAreas is a tuple; get rid of the cruft, and convert it into a string:
    annAreas = str(', '.join(obj.getAffectedArea()))
    # eventType is a tuple; get rid of the cruft, and convert it into a string:
    annType = str(', '.join(obj.getEventType()))
    # experiments is a tuple; get rid of the cruft, and convert it into a string:
    annExperiments = str(', '.join(obj.getExperiments()))
    # get the event start time and convert it into a string:
    rawStartTime = obj.start()
    startTime = str(rawStartTime.strftime('%B %d, %Y, %I:%M %p %Z')) 

    # for testing; not needed now:
    #import pdb; pdb.set_trace()

    # get the event end time and convert it into a string:
    rawEndTime = obj.end()
    endTime = str(rawEndTime.strftime('%B %d, %Y, %I:%M %p %Z'))

    # get the object URL, and correct it for site/proxy domain:
    rawAnnUrl = obj.absolute_url()
    annUrl = "https://wwww.racf.bnl.gov/announcements/" + rawAnnUrl.split("/")[-1]

    # formulate the message body:
    msg = "Dear computing list subscriber," + "\n\n"
    msg += "A new RACF Computing Facility announcement has been posted:" + "\n" +  obj.Title() + "\n\n"
    # description isn't working at the moment; it seems to get pulled but then stripped out
    # before appearing in email or web object (bad decode function call?): 
    msg += "Description: " + "\n" + rawDescription + "\n\n"
    msg += "Duration: " + "\n" + startTime + " - "+ endTime + "\n\n"
    msg += "RACF Group: " + "\n" + obj.getGroupResponsible() + "\n\n"
    msg += "Affected Area(s) of Operations: " + "\n" + annAreas + "\n\n" 
    msg += "Affected Experiment Group(s): " + "\n" + annExperiments + "\n\n" 
    msg += "Type of event: " + "\n" + annType + "\n\n"
    # get object's main text, and strip its HTML code for emailing:
    msg += "Details: " + "\n" + obj.getText(mimetype="text/plain") + "\n\n"
    msg += "See this message in full on the RACF facility web site: " + "\n" + annUrl + "\n\n"
    msg += "With best regards," + "\n"
    msg += "RACF Site Administration" + "\n"

    # finally, send the message: 
    mhost.send(msg,to_list,emailFrom,emailSubject)
