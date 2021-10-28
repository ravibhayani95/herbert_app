# -*- coding: utf-8 -*-
# Copyright (c) 2019, John Vincent Fiel and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from dateutil.parser import parse

"""

Mao ni ila standard shift:

CI - 7.00AM
CO - 12NN

CI - 1PM
CO - 5PM

Ot Na ang remaining if mu ingon mi nga mag OT sila

"""
def get_employee_time(employee):
    schedule = frappe.db.sql("""SELECT time_in_am as am_in, time_out_am as am_out,
                                          time_in as pm_in, time_out as pm_out
                                    FROM `tabHD Employee Schedules`
                                    INNER JOIN `tabHD Employee Schedule`
                                          ON `tabHD Employee Schedule`.name = `tabHD Employee Schedules`.parent
                                            WHERE `tabHD Employee Schedule`.employee=%s
                                            AND `tabHD Employee Schedules`.parentfield='schedules' ORDER BY `tabHD Employee Schedules`.idx""",(employee),as_dict=True)
    # schedules = []

    # return [{"am_in":"","am_out":"","pm_in":"","pm_out":""}]

    return schedule

def get_employee_time_holiday(employee):
    schedule = frappe.db.sql("""SELECT time_in_am as am_in, time_out_am as am_out,
                                          time_in as pm_in, time_out as pm_out
                                    FROM `tabHD Employee Schedules`
                                    INNER JOIN `tabHD Employee Schedule`
                                          ON `tabHD Employee Schedule`.name = `tabHD Employee Schedules`.parent
                                            WHERE `tabHD Employee Schedule`.employee=%s
                                            AND `tabHD Employee Schedules`.parentfield='holidays'""",(employee),as_dict=True)
    # schedules = []

    # return [{"am_in":"","am_out":"","pm_in":"","pm_out":""}]

    return schedule

def convert_time(time,allowance_mins=0):
    # print "> convert time"
    time = time.split(":")
    # print time
    import datetime
    now = datetime.datetime.now()
    # today8am = now.replace(hour=hr or int(time[0]), minute=mins or int(time[1]), second=int(time[2]), microsecond=0)
    today8am = now.replace(hour=int(time[0]), minute=int(time[1]), second=int(time[2]), microsecond=0) \
               + datetime.timedelta(minutes=allowance_mins)
    # print time,allowance_hr,today8am
    return today8am

def get_time_diff(s1,s2):
    from datetime import datetime
    # s1 = '10:33:26'
    # s2 = '11:15:49'  # for example
    FMT = '%H:%M:%S'
    # print s1,s2
    if s1 and s2:
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        # print tdelta
        return  tdelta
    else:
        return None

# def check_if_holiday(date):
#     print (date)
#     from dateutil.parser import parse
#     date_obj = parse(date)
#     holiday = frappe.db.sql("""SELECT name FROM `tabHoliday` WHERE holiday_date=%s""",(date_obj.date()))
#     print (holiday)
#     if holiday != ():
#         return True
#     else:
#         return False

def check_if_holiday(date,emp_no):
    # print (date)
    from dateutil.parser import parse
    date_obj = parse(date)
    holiday = frappe.db.sql("""SELECT time_in_am as am_in,time_out_am as am_out,time_in as pm_in,time_out as pm_out
                                  FROM `tabHD Schedules Holiday`
                                  INNER JOIN `tabHD Employee Schedule`
                                    ON `tabHD Employee Schedule`.name = `tabHD Schedules Holiday`.parent
                                    WHERE `tabHD Schedules Holiday`.date=%s AND `tabHD Employee Schedule`.name=%s""",(date_obj.date(),emp_no),as_dict=True)
    # print (holiday)
    if holiday != []:

        return holiday[0]
    else:
        return False

class UploadHDTime(Document):
    def read_dat(self):
        import csv

        # read flash.dat to a list of lists
        datContent = [i.strip().split() for i in open(frappe.utils.get_site_path()+self.upload_dat).readlines()]

        # write it as a new CSV file
        # with open("./flash.csv", "wb") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(datContent)

        from operator import itemgetter
        self.hd_time = []
        self.hd_time_computed = []
        current_date = ""
        current_emp = ""
        current_data = {
                        "employee":"",
                        "am":{"time_in":"","time_out":"","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""},
                        "pm": {"time_in": "", "time_out": "","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""}}

        schedule = []
        schedule_holiday = []

        times = sorted(datContent, key=itemgetter(0))
        final_data = []

        for t in times:
            # print "==========",t[1]

            if self.select_employee:
                select_employee = self.select_employee.replace("EMP/","")
                select_employee = int(select_employee) #remove zeros
                select_employee = str(select_employee)
                if select_employee != t[0]:
                    continue

            # print parse(t[1])
            if parse(t[1]) >= parse(self.from_date) and parse(t[1]) <= parse(self.to_date):
                None
                # print "date not belong."
                final_data.append(t)
            else:
                # print "date not belong"
                continue

        for i,dat in enumerate(final_data):
            # print(dat)

            if not current_date:

                current_data = {
                    "employee": dat[0],
                    "am": {"time_in": "", "time_out": "","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""},
                    "pm": {"time_in": "", "time_out": "","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""}}
                current_date = dat[1]
                current_emp = dat[0]
                schedule = get_employee_time(current_emp)
                schedule_holiday = get_employee_time_holiday(current_emp)

            # print current_date,dat[1]
            if current_date != dat[1] or current_emp != dat[0]:
                # print(" passed ")
                # print current_data
                nl = self.append('hd_time_computed', {})
                nl.employee = current_data['employee']
                nl.date = current_date
                nl.time_in = current_data['am']['time_in']
                nl.time_out = current_data['am']['time_out']
                nl.ut_hrs = current_data['am']['ut_hrs']
                nl = self.append('hd_time_computed', {})
                nl.employee = current_data['employee']
                nl.date = current_date
                nl.time_in = current_data['pm']['time_in']
                nl.time_out = current_data['pm']['time_out']
                nl.ut_hrs = current_data['pm']['ut_hrs']
                nl.ot_hrs = current_data['pm']['ot_hrs']

                current_data = {
                    "employee": dat[0],
                    "am": {"time_in": "", "time_out": "","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""},
                    "pm": {"time_in": "", "time_out": "","ut_hrs":"","time_in_str":"","time_out_str":"", "ot_hrs":""}}
                current_date = dat[1]
                current_emp = dat[0]
                schedule = get_employee_time(current_emp)
                schedule_holiday = get_employee_time_holiday(current_emp)


            date_obj = parse(current_date)
            weekday = date_obj.date().weekday()

            # print "============== Weekday =============="
            # print date_obj.date(), weekday

            # print(dat[2])

            UT = 0.00
            OT = 0.00


            #check holiday

            is_holiday = 0
            # dat[1] = '01-06-2019'
            is_holiday = check_if_holiday(dat[1],dat[0])
            # is_holiday = 1
            if is_holiday:

                if not schedule_holiday:
                    frappe.throw("Please setup holiday schedules for employee " + dat[0])

                # print("============= HOLIDAY HURRAY !!! =============")
                if (convert_time(dat[2]) >= convert_time(str(is_holiday['am_in'])) or convert_time(dat[2]) <= convert_time(str(is_holiday['am_in']))) \
                                        and convert_time(dat[2]) <= convert_time(str(is_holiday['am_out'])):

                    if convert_time(dat[2]) >= convert_time(str(is_holiday['am_in'])) \
                            and convert_time(dat[2]) <= convert_time(str(is_holiday['am_in']),allowance_mins=300):
                        current_data['am'].update({"time_in": dat[1] + ' ' + dat[2],
                                                   "time_in_str": dat[2]})

                    elif convert_time(dat[2]) >= convert_time(str(is_holiday['am_in']),allowance_mins=300) \
                            and convert_time(dat[2]) <= convert_time(str(is_holiday['am_out'])):
                        # print(" time out ")
                        if not current_data['am']['time_out']:
                            # early check in sa hapon
                            # e.g. check out sa morning kay 12:20:00
                            # & check in sa hapon kay 12:30:00
                            current_data['am'].update({"time_out": dat[1] + ' ' + dat[2],
                                                       "time_out_str": dat[2]})
                            UT = get_time_diff(current_data['am']['time_in_str'],current_data['am']['time_out_str'])
                            if UT:
                                if 4 - int(str(UT).split(":")[0]) > 0:
                                    current_data['am'].update({'ut_hrs':4-int(str(UT).split(":")[0])})

                if convert_time(dat[2]) >= convert_time(str(is_holiday['pm_in'])) \
                        and convert_time(dat[2]) <= convert_time(str(is_holiday['pm_out'])):
                    if convert_time(dat[2]) >= convert_time(str(is_holiday['pm_in'])) \
                            and convert_time(dat[2]) <= convert_time(str(is_holiday['pm_in']),allowance_mins=60):
                        # print(" time in ")
                        current_data['pm'].update({"time_in": dat[1] + ' ' + dat[2]})
                        current_data['pm'].update({"time_in_str": dat[2]})
                    elif convert_time(dat[2]) >= convert_time(str(is_holiday['pm_in']),allowance_mins=60) \
                        and convert_time(dat[2]) < convert_time(str(is_holiday['pm_out'])):
                        # print(" time out ")
                        current_data['pm'].update({"time_out": dat[1] + ' ' + dat[2]})
                        current_data['pm'].update({"time_out_str": dat[2]})

                        UT = get_time_diff(current_data['pm']['time_in_str'], current_data['am']['time_out_str'])
                        if UT:
                            current_data['pm'].update({'ut_hrs': 4 - int(str(UT).split(":")[0])})

                        # dat[2] = "19:00:00" #test
                        if convert_time(dat[2]) > convert_time(str(schedule_holiday[weekday]['pm_out'])):
                            # print dat[2], str(schedule_holiday[weekday]['pm_out'])
                            OT = get_time_diff(str(schedule_holiday[weekday]['pm_out']),dat[2])
                            # print OT
                            if OT:
                                current_data['pm'].update({'ot_hrs': str(OT).split(":")[0]})

            else:

                if not schedule:
                    # frappe.throw("Please setup normal schedules for employee " + dat[0])
                    frappe.msgprint("Please setup normal schedules for employee " + dat[0])


                else:

                    if weekday > len(schedule)-1:
                        continue

                    print("------------------------------",len(schedule))
                    # print dat, schedule, weekday
                    print(schedule)
                    print(weekday)
                    print("Weekday/",weekday,str(schedule[weekday]['am_out']))


                    if weekday < len(schedule): #sunday is holiday
                        # print dat[1], dat[2], convert_time(str(schedule[weekday]['am_in']))
                        print("raw data",dat[1], dat[2])
                        print("Out/",convert_time(str(schedule[weekday]['am_out']),allowance_mins=10))
                        if (convert_time(dat[2]) >= convert_time(str(schedule[weekday]['am_in'])) or convert_time(dat[2]) < convert_time(str(schedule[weekday]['am_in']))) \
                                                and convert_time(dat[2]) <= convert_time(str(schedule[weekday]['am_out']),allowance_mins=10): ####IN


                            print(">>>>>>>>>>>>>>>",convert_time(str(schedule[weekday]['am_in']),allowance_mins=30))
                            if (convert_time(dat[2]) >= convert_time(str(schedule[weekday]['am_in'])) or convert_time(dat[2]) < convert_time(str(schedule[weekday]['am_in']))) \
                                    and convert_time(dat[2]) <= convert_time(str(schedule[weekday]['am_in']),allowance_mins=30):
                                current_data['am'].update({"time_in": dat[1] + ' ' + dat[2],
                                                           "time_in_str": dat[2]})

                            elif convert_time(dat[2]) >= convert_time(str(schedule[weekday]['am_in']),allowance_mins=30) \
                                    and convert_time(dat[2]) <= convert_time(str(schedule[weekday]['am_out']),allowance_mins=10): #Out
                                # print("///// time out ")
                                if not current_data['am']['time_out']:
                                    # early check in sa hapon
                                    # e.g. check out sa morning kay 12:20:00
                                    # & check in sa hapon kay 12:30:00
                                    current_data['am'].update({"time_out": dat[1] + ' ' + dat[2],
                                                               "time_out_str": dat[2]})
                                    UT = get_time_diff(current_data['am']['time_in_str'],current_data['am']['time_out_str'])
                                    if UT:
                                        if 4-int(str(UT).split(":")[0]) > 0:
                                            current_data['am'].update({'ut_hrs':4-int(str(UT).split(":")[0])})


                        print(convert_time(str(schedule[weekday]['pm_in']),allowance_mins=60))
                        if (convert_time(dat[2]) >= convert_time(str(schedule[weekday]['pm_in']),allowance_mins=-29)):
                            if convert_time(dat[2]) >= convert_time(str(schedule[weekday]['pm_in']),allowance_mins=-15  ) \
                                    and convert_time(dat[2]) <= convert_time(str(schedule[weekday]['pm_in']),allowance_mins=60):
                                # print(" time in ")
                                current_data['pm'].update({"time_in": dat[1] + ' ' + dat[2]})
                                current_data['pm'].update({"time_in_str": dat[2]})
                            elif convert_time(dat[2]) >= convert_time(str(schedule[weekday]['pm_in']),allowance_mins=60):
                                print(" time out ")
                                current_data['pm'].update({"time_out": dat[1] + ' ' + dat[2]})
                                current_data['pm'].update({"time_out_str": dat[2]})

                                UT = get_time_diff(current_data['pm']['time_in_str'], current_data['am']['time_out_str'])
                                if UT and convert_time(dat[2]) < convert_time(str(schedule[weekday]['pm_out'])):
                                    current_data['pm'].update({'ut_hrs': 4 - int(str(UT).split(":")[0])})

                                # dat[2] = "19:00:00" #test
                                if convert_time(dat[2]) > convert_time(str(schedule[weekday]['pm_out'])):
                                    print(dat[2], str(schedule[weekday]['pm_out']))
                                    OT = get_time_diff(str(schedule[weekday]['pm_out']),dat[2])
                                    print(OT)
                                    if OT:
                                        current_data['pm'].update({'ot_hrs': str(OT).split(":")[0]})

            nl = self.append('hd_time', {})
            nl.employee = dat[0]
            nl.date_and_time = dat[1] + ' ' +dat[2]
            nl.check_in = dat[3]
            nl.check_out = dat[4]
            nl.ot_in = dat[5]
            nl.ot_out = dat[6]
            # nl.is_out
            # nl.is_undertime



            # if i == 20-1:
            #     break


        # print(datContent)

        return datContent

    def reload_dat(self):
        self.read_dat()
