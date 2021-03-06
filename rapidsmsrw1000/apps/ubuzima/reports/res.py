####SAMPLE MESSAGE #####
##res_EN = "The correct format message is: RES MOTHER_ID REPORTED_SYMPTOMS LOCATION_CODE INTERVENTION_CODE MOTHER_STATUS CHILD_STATUS"
##res_FR = "Andika: RES INDANGAMUNTU IBIBAZO_BYATANZWE AHO_AHEREREYE UBUTABAZI_BWAKOZWE UKO_UMUBYEYI AMEZE UKO_UMWANA_AMEZE"
##msg = "RES 1198156435491265 FE HO AA MW"
###m = re.search("res\s+(\d+)\s?(.*)\s(hp|cl|ho|or)\s(pt|pr|tr|aa|al|at|na)\s(mw|ms|cw|cs)s?(.*)", msg, re.IGNORECASE)   
###groups = ('1198156435491265', 'FE', 'HO', 'AA', 'mw', '')
#        nid = m.group(1)
#        ibibazo = m.group(2)
#        location = m.group(3)
#        intervention = m.group(4)
#        mstatus = m.group(5)
#        cstatus = m.group(6)

    @keyword("\s*res(.*)")
    def res(self, message, notice):
        """Risk result report, represents a possible response from a problem with a pregnancy, can trigger alerts."""
        
        if not getattr(message, 'reporter', None):
            message.respond(_("You need to be registered first, use the REG keyword"))
            return True
            
        m = re.search("res\s+(\d+)\s?(.*)\s(hp|cl|ho|or)\s(pt|pr|tr|aa|al|at|na)\s(mw|ms|cw|cs)s?(.*)", message.text, re.IGNORECASE)
        if not m:
            message.respond(_("The correct format message is: RES MOTHER_ID REPORTED_SYMPTOMS LOCATION_CODE INTERVENTION_CODE MOTHER_STATUS CHILD_STATUS"))
            return True

        nid = m.group(1)
        ibibazo = m.group(2)
        location = m.group(3)
        intervention = m.group(4)
        mstatus = m.group(5)
        cstatus = m.group(6)

        # get or create the patient
        patient = self.get_or_create_patient(message.reporter, nid)

        report = self.create_report('Result', patient, message.reporter)
        
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
        
        fields.append(self.read_key(location))
        fields.append(self.read_key(intervention))
        fields.append(self.read_key(mstatus))
        for st in self.read_fields(cstatus, False, False)[0]:	fields.append(st)

    	#print fields
        for field in fields:
            field.save()
            report.fields.add(field)
            
        # either send back our advice text or our default response
        try:	response = self.run_triggers(message, report)
        except:	response = None
        if response:
            message.respond(response)
        else:
            message.respond(_("Thank you! Risk Result report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	self.cc_supervisor(message, report)
   	except:	pass  
        

        return True
