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

class ChiHandler (KeywordHandler):
    """
    Child health Report REGISTRATION
    """

    keyword = "chi"
    
    def filter(self):
        if not getattr(message, 'connection', None):
            self.respond(_("You need to be registered first, use the REG keyword"))
            return True 
    def help(self):
        self.respond("The correct format message is: CHI MOTHER_ID CHILD_NUM DOB VACCINS VACCIN_SERIE ACTION_CODE LOCATION_CODE CHILD_WEIGHT MUAC")

    def handle(self, text):
        #print self.msg.text
        return self.child(self.msg)
        self.respond(text)

    def child(self, message):

    	try:
            message.reporter = PersistantConnection.objects.get(identity = message.connection.identity).reporter
        except Exception, e:
            message.respond(_("You need to be registered first, use the REG keyword"))
            return True

        m = re.search("chi\s+(\d+)\s+([0-9]+)\s([0-9.]+)\s(v1|v2|v3|v4|v5|v6)\s(vc|vi)\s?(.*)\s(ho|hp|cl|or)\s(wt\d+\.?\d*)\s(muac\d+\.?\d*)\s?(.*)",\
                         message.text, re.IGNORECASE)
        if not m:
            message.respond(_("The correct format message is: CHI MOTHER_ID CHILD_NUM DOB VACCINS VACCIN_SERIE ACTION_CODE LOCATION_CODE CHILD_WEIGHT MUAC"))
            return True

        nid = m.group(1)
        number = m.group(2)
        chidob = m.group(3)
        vaccins = m.group(4)
        vaccin_serie = m.group(5)
        ibibazo = m.group(6)
        location = m.group(7)
        weight = m.group(8)
        muac = m.group(9)

        # get or create the patient
        patient = get_or_create_patient(message.reporter, nid)
        
        report = create_report('Child Health', patient, message.reporter)
        
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
        fields.append(read_weight(weight, weight_is_mothers=False))
        fields.append(read_key(vaccins))
        fields.append(read_key(vaccin_serie))
        fields.append(read_key(location))
        fields.append(read_muac(muac))
        
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
            message.respond(_("Thank you! Child Health report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	cc_supervisor(message, report)
        except:	pass      
            	
        return True 

