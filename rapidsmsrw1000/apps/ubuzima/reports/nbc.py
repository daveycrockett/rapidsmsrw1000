####SAMPLE MESSAGE #####
##res_EN = "The correct format message is: NBC MOTHER_ID CHILD_NUM NBC_ROUND DOB SYMPTOMS BREASTFEEDING INTERVENTION CHILD_STATUS"
##res_FR = "Andika: NBC INDANGAMUNTU NUMERO INSHURO ITARIKI_YAVUTSE IBIBAZO KONKA UBUTABAZI UKO_UMWANA_AMEZE"
##msg = "NBC 1198156435491265 01 NBC2 13.02.2011 CO NB PR CS"
###m = re.search("nbc\s+(\d+)\s+([0-9]+)\s(nbc1|nbc2|nbc3)\s([0-9.]+)\s?(.*)\s(nb|bf1)\s(pt|pr|tr|aa|al|at|na)\s(mw|ms|cw|cs)\s?(.*)", msg, re.IGNORECASE)   
###groups = ('1198156435491265', '01', 'NBC2', '13.02.2011', 'CO', 'NB', 'PR', 'CS', '')
#        nid = m.group(1)
#        number = m.group(2)
#        tour = m.group(3)
#        chidob = m.group(4)
#        ibibazo = m.group(5)
#        bf1 = m.group(6)
#        intervention = m.group(7)
#        mstatus = m.group(8)
#        cstatus = m.group(9)

    #NBC keyword
    @keyword("\s*nbc(.*)")
    def nbc(self, message, notice):
        """NBC report.  """
        
        if not getattr(message, 'reporter', None):
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
        patient = self.get_or_create_patient(message.reporter, nid)
        
        report = self.create_report('Newborn Care', patient, message.reporter)
        
        # read our fields
        try:
            (fields, dob) = self.read_fields(ibibazo, False, False)
    	    dob = self.parse_dob(chidob)
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
        
        fields.append(self.read_key(tour))
        for st in self.read_fields(cstatus, False, False)[0]:	fields.append(st)
        fields.append(self.read_key(mstatus))
        fields.append(self.read_key(intervention))
        fields.append(self.read_key(bf1))

        for field in fields:
            field.save()
            report.fields.add(field)            
        
        # either send back the advice text or our default msg
        try:	response = self.run_triggers(message, report)
        except:	response = None
        if response:
            message.respond(response)
        else:
            message.respond(_("Thank you! NBC report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	self.cc_supervisor(message, report)
   	except:	pass  
    	        
        return True
    
        #NBC keyword

