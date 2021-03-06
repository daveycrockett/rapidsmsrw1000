####SAMPLE MESSAGE #####
##res_EN = "The correct format message is: PRE MOTHER_ID LAST_MENSES NEXT_VISIT PREVIOUS_RISK CURRENT_RISK LOCATION_CODE MOTHER_WEIGHT MOTHER_HEIGHT SANITATION TELEPHONE"
##res_FR = "Andika: ANC INDANGAMUNTU ITARIKI_YIMIHANGO IYOGUSUBIRAYO INSHURO_YASAMYE IZAVUTSE IBIBAZO_KERA IBISHYA AHO_YAPIMIWE IBIRO UBUREBURE UMUSARANI KANDAGIRA TELEFONI"
##msg = "RED 1198156435491265 HE CO HO WT70.1"
###m = re.search("red\s+(\d+)\s?(.*)\s(hp|cl|ho|or)\s(wt\d+\.?\d)\s?(.*)", msg, re.IGNORECASE)   
###groups = ('1198156435491265', 'FE PA', 'HO', 'WT75.0', '')
#        nid = m.group(1)
#        ibibazo = m.group(2)
#        location = m.group(3)
#        weight = m.group(4)
    @keyword("\s*red(.*)")
    def red_alert(self, message, notice):
        """RED Alert report, represents a possible problem with a pregnancy, can trigger alerts."""
        
        if not getattr(message, 'reporter', None):
            message.respond(_("You need to be registered first, use the REG keyword"))
            return True
            
        m = re.search("red\s+(\d+)\s?(.*)\s(hp|cl|ho|or)\s(wt\d+\.?\d)\s?(.*)", message.text, re.IGNORECASE)
        if not m:
            message.respond(_("The correct format message is: RED MOTHER_ID ACTION_CODE LOCATION_CODE MOTHER_WEIGHT"))
            return True

        nid = m.group(1)
        ibibazo = m.group(2)
        location = m.group(3)
        weight = m.group(4)

        # get or create the patient
        patient = self.get_or_create_patient(message.reporter, nid)

        report = self.create_report('Red Alert', patient, message.reporter)
        
        # Line below may be needed in case Risk reports are sent without previous Pregnancy reports
        #location = message.reporter.location
        
        # read our fields
        try:
            (fields, dob) = self.read_fields(ibibazo, False, True)
        except Exception, e:
            # there were invalid fields, respond and exit
            message.respond("%s" % e)
            return True

        # save the report
        report.save()
        
	# then associate all our fields with it
        fields.append(self.read_weight(weight, weight_is_mothers=True))
        fields.append(self.read_key(location))
        for field in fields:
            field.save()
            report.fields.add(field)
            
        # either send back our advice text or our default response
        try:	response = self.run_triggers(message, report)
        except:	response = None
        if response:
            message.respond(response)
        else:
            message.respond(_("Thank you! RED Alert report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	self.cc_supervisor(message, report)
   	except:	pass  
        

        return True
