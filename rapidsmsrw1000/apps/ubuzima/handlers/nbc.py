#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


##DJANGO LIBRARY
from django.utils.translation import ugettext as _
from django.utils.translation import activate, get_language
from decimal import *
from exceptions import Exception
import traceback
from datetime import *
from time import *
from django.db.models import Q

###DEVELOPED APPS
from rapidsmsrw1000.apps.ubuzima.reports.utils import *
from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsmsrw1000.apps.thousanddays.models import *

class NbcHandler (KeywordHandler):
    """
    New Born Care report REGISTRATION
    """

    keyword = "nbc"
    
    def filter(self):
        if not getattr(message, 'connection', None):
            self.respond(_("You need to be registered first, use the REG keyword"))
            return True 
    def help(self):
        self.respond("The correct format message is: NBC MOTHER_ID CHILD_NUM NBC_ROUND DOB SYMPTOMS INTERVENTION CHILD_STATUS")

    def handle(self, text):
        #print self.msg.text
        return self.nbc(self.msg)
        self.respond(text)

    def nbc(self, message):

    	try:
            message.reporter = PersistantConnection.objects.get(identity = message.connection.identity).reporter
        except Exception, e:
            message.respond(_("You need to be registered first, use the REG keyword"))
            return True

        m = re.search("nbc\s+(\d+)\s+([0-9]+)\s(nbc1|nbc2|nbc3)\s([0-9.]+)\s?(.*)\s(nb|bf1)\s(pt|pr|tr|aa|al|at|na)\s(mw|ms|cw|cs)\s?(.*)", message.text, re.IGNORECASE)
        if not m:
            message.respond(_("The correct format message is: NBC MOTHER_ID CHILD_NUM NBC_ROUND DOB SYMPTOMS INTERVENTION CHILD_STATUS"))
            return True

        nid = m.group(1)
        number = m.group(2)
        tour = m.group(3)
        chidob = m.group(4)
        ibibazo = m.group(5)
        bf1 = m.group(6)
        intervention = m.group(7)
        mstatus = m.group(8)
        cstatus = m.group(9)


        # get or create the patient
        patient = get_or_create_patient(message.reporter, nid)
        
        report = create_report('Newborn Care', patient, message.reporter)
        
        # read our fields
        try:
            (fields, dob) = read_fields(ibibazo, False, False)
    	    dob = parse_dob(chidob)
        except Exception, e:
            # there were invalid fields, respond and exit
            message.respond("%s" % e)
            return True

        # set the dob for the child if we got one
        if dob:
            report.set_date_string(dob)
            
        # set the child number
        child_num_type = FieldType.objects.get(key='child_number')
        fields.append(Field(type=child_num_type, value=Decimal(str(number))))

        # save the report
        report.save()
                
        # then associate all our fields with it
        
        fields.append(read_key(tour))
        for st in read_fields(cstatus, False, False)[0]:	fields.append(st)
        fields.append(read_key(mstatus))
        fields.append(read_key(intervention))
        fields.append(read_key(bf1))

        for field in fields:
            field.report = report
            field.save()
            report.fields.add(field)

	    # either send back the advice text or our default msg
        try:	response = run_triggers(message, report)
        except:	response = None
        if response:
            message.respond(response)
        else:
            message.respond(_("Thank you! NBC report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	cc_supervisor(message, report)
        except:	pass      
            	
        return True 


