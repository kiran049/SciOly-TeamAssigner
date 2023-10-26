import pandas as pd

form = pd.read_csv('SciOly.csv')

Students = []
amtOfEventsPerStudent = 5
team_dict = {}
Teams = []

# create an exceptions file, also clear it for each run
exceptions = open("exceptions.txt", "w")

teamCounter = 1
event_overlaps = pd.read_csv('eventOverlaps.csv')
allEvents = pd.read_csv('allEvents.csv')
allEvents = allEvents['Events']
allEvents = allEvents.values.tolist()
#normalize all events in the allEvents list using .strip and .lower
for k in range(len(allEvents)):
    allEvents[k] = allEvents[k].replace(" ", "").lower()


def createListofStudents():
    Students.extend([
        Student(
            form.iat[i, 1],  # name of student
            form.iat[i, 3],  # event 1
            form.iat[i, 5],  # event 2
            form.iat[i, 7],  # event 3
            form.iat[i, 9],  # event 4
            form.iat[i, 11],  # event 5
            form.iat[i, 4],  # partners for event 1
            form.iat[i, 6],  # partners for event 2
            form.iat[i, 8],  # partners for event 3
            form.iat[i, 10],  # partners for event 4
            form.iat[i, 12]  # partners for event 5
        )
        for i in range(form.shape[0])
    ])

    for student in Students:
        student.partnerValuesToObjects()



def createListofTeams():
    for student in Students:
        for index, event in enumerate(student.events):
            if event != 'nan':
                if event != "Experimental Design".replace(" ","").lower() and event != "Codebusters".lower():

                    # if no partner, assign them one
                    if not student.partners[index]:
                        startContinue = True
                        for otherStudent in Students:  # search other students
                            if otherStudent != student:  # ensure not checking same student
                                # see if they both want same event
                                for otherIndex, otherEvent in enumerate(otherStudent.events):
                                    if otherEvent == event and not otherStudent.partners[
                                        otherIndex] and otherEvent != 'nan':  # ensure they both want same event, do not have a partner, and the event for student2 is not none
                                        # assign each other as partners
                                        student.partners[index] = otherStudent
                                        otherStudent.partners[otherIndex] = student
                                        startContinue = False
                        if startContinue:
                            continue

                    student2 = student.partners[index]
                    # retrieve student2 preference index
                    try:
                        for count, student2event in enumerate(student2.events):
                            if student2event == event:
                                count = count
                                break
                    except AttributeError:
                        print(student2)
                    createTeam(student, student2, event, index, count)
                # IF 3 PERSON EVENT
                else:
                    if not student.partners[index]:
                        raise Exception(
                            f"{student.name} has the 3 person event, {event}, and has no partners listed, there is no support to find matching students with no partners for 3 person events currently")
                    try:
                        student2 = student.partners[index][0]
                        student3 = student.partners[index][1]
                    except TypeError:
                        raise Exception(
                            f"{student.name} has the 3 person event, {event}, but only has 1 partner listed")
                    for newCount, student2event in enumerate(student2.events):
                        if student2event == event:
                            newCount = newCount
                            break
                    for otherCount, student3event in enumerate(student3.events):
                        if student3event == event:
                            otherCount = otherCount
                            break
                    createTeam(student, student2, event, index, newCount, student3, otherCount)


class Student:
    def __init__(self, name, event1, event2, event3, event4, event5, partnersEvent1, partnersEvent2, partnersEvent3,
                 partnersEvent4, partnersEvent5):
        self.teams = []
        self.name = name.strip()
        self.events = [str(event1).replace(" ", "").lower(), str(event2).replace(" ", "").lower(),
                       str(event3).replace(" ", "").lower(), str(event4).replace(" ", "").lower(),
                       str(event5).replace(" ", "").lower()]
        self.partners = [self.extract_partner_list(partnersEvent1), self.extract_partner_list(partnersEvent2),
                         self.extract_partner_list(partnersEvent3),
                         self.extract_partner_list(partnersEvent4), self.extract_partner_list(partnersEvent5)]

    def partnerValuesToObjects(self):
        for index, partner in enumerate(self.partners):
            if len(partner) == 1:
                for student in Students:
                    if str(partner[0]).strip().lower() == str(student.name).strip().lower():
                        self.partners[index] = student
            if len(partner) == 2:
                for j in range(len(partner)):
                    for student in Students:
                        if str(partner[j]).strip().lower() == str(student.name).strip().lower():
                            self.partners[index][j] = student

    def extract_partner_list(self, partners_str):
        if partners_str is None:
            return []
        elif isinstance(partners_str, str) and "," in partners_str:
            return [partner.strip() for partner in partners_str.split(",")]
        elif isinstance(partners_str, str):
            return [partners_str.strip()]
        else:
            return []  # handle the case where partners_str is not a string or is None

    def checkForOverlappingEvents(self, wantBoolReturn=False):
        student_events = set(self.events)
        row_num = event_overlaps.shape[1] - 1
        for i in range(row_num):
            row = (event_overlaps[f'row {i + 1}']).to_list()
            row = set(row)
            if len(student_events.intersection(row)) > 1:
                if wantBoolReturn:
                    return True

                print(
                    f'WARNING: STUDENT {self.name} has overlapping events in row {i + 1} of the overlapping event CSV.')
                # write to exceptions file
                exceptions.write(
                    f"EVENT OVERLAP: {self.name} has overlapping events in row {i + 1} of the overlapping event CSV.\n")
        if wantBoolReturn:
            return False


class Team:
    def __init__(self, teamNumber, event, person1, person2, person1EventPreference, person2EventPreference, person3,
                 person3EventPreference):
        strippedTeamNumber = str(teamNumber).strip("{}")
        self.teamNumber = strippedTeamNumber
        self.person1 = person1
        person1.teams.append(teamNumber)
        self.person2 = person2
        person2.teams.append(teamNumber)
        self.person3 = person3
        self.person1EventPreference = person1EventPreference
        self.person2EventPreference = person2EventPreference
        self.person3EventPreference = person3EventPreference

        if self.person3 is None:
            self.members = [person1, person2]
            try:
                self.groupEventPreference = (person1EventPreference + person2EventPreference) / 2
            except TypeError:
                raise TypeError(f"{person1.name} or {person2.name} has a CSV formatting error")
        else:
            self.members = [person1, person2, person3]
            try:
                self.groupEventPreference = (
                                                    person1EventPreference + person2EventPreference + person3EventPreference) / 3
            except TypeError:
                raise TypeError(
                    f"{person1.name} or {person2.name} or {person3.name} has a CSV formatting error. DEBUG INFO: EVENT NAME {event}")
            person3.teams.append(teamNumber)
        self.event = event

    eventsChecked = []

    def checkMaxEvents(self,maxTeamsForEachEvent):
        if self.event not in self.eventsChecked:
            self.eventsChecked.append(self.event)
        else:
            return

        TeamsWithSameEvent = [self]
        for team in Teams:
            if team != self:
                if team.event == self.event:
                    TeamsWithSameEvent.append(team)
        userOptOut = False
        while len(TeamsWithSameEvent) > maxTeamsForEachEvent:
            min_group_event_preference = max(team.groupEventPreference for team in
                                             TeamsWithSameEvent)  # max function used bc the preference and the preference integer are inversely proportional
            teams_with_lowest_preference = [team for team in TeamsWithSameEvent if
                                            team.groupEventPreference == min_group_event_preference]
            teamRemoved = []
            for team in teams_with_lowest_preference:
                teamRemoved = team
                TeamsWithSameEvent.remove(teamRemoved)

            # adjust student partner values and event values to reflect the removal of the team
            for student in teamRemoved.members:
                for index, event in enumerate(student.events):
                    if event == teamRemoved.event:
                        student.events[index] = 'nan'
                        student.partners[index] = []
                        break

            print(
                f"Team {teamRemoved.teamNumber} with the minimum group event preference for {self.event} has been removed.")
            # write to exceptions file
            names = []
            for member in teamRemoved.members:
                names.append(member.name)
            exceptions.write(
                f"{names} had the minimum group event preference for {self.event} and did not get the event.\n")
            # delete the teamRemoved object from the Teams list, and the object itself
            Teams.remove(teamRemoved)
            del teamRemoved
            updateStudentTeamsVariable()


def updateStudentTeamsVariable():
    for student in Students:
        student.teams = []
    for team in Teams:
        for student in team.members:
            student.teams.append(team.teamNumber)


def createTeam(person1, person2, event, person1EventPreference, person2EventPreference, person3=None,
               person3EventPreference=None):
    global teamCounter

    # check if a team with the same members and event already exists
    for team in Teams:
        if team.event == event:
            if person3:
                if set([person1, person2, person3]) == set(team.members):
                    return  # a team with the same members and event already exists
            else:
                if set([person1, person2]) == set(team.members):
                    return  # a team with the same members and event already exists

    # if there is not a duplicate, create the team
    if person3:
        team_dict[f"Team {teamCounter}"] = Team({teamCounter}, event, person1, person2, person1EventPreference,
                                                person2EventPreference, person3, person3EventPreference)
        Teams.append(team_dict[f"Team {teamCounter}"])
        teamCounter += 1
    elif person3 is None:
        team_dict[f"Team {teamCounter}"] = Team({teamCounter}, event, person1, person2, person1EventPreference,
                                                person2EventPreference, person3, person3EventPreference)
        Teams.append(team_dict[f"Team {teamCounter}"])
        teamCounter += 1
    else:
        raise Exception("failed to make a team")

def checkIfAllEventsCovered():
    #convert all events to a set
    allEventsSet = set(allEvents)
    eventsInTeams = []
    # check every team's event and then compare to the set of all events, then if events dont match state which event(s) are missing
    for team in Teams:
        eventsInTeams.append(team.event)
    eventsInTeams = set(eventsInTeams)
    if eventsInTeams != allEventsSet:
        missingEvents = allEventsSet.difference(eventsInTeams)
        print(f"WARNING: The following events are not covered by any team: {missingEvents}.")
        # write to the exceptions file
        exceptions.write(f"WARNING: The following events are not covered by any team: {missingEvents}.\n")
        # userInput = input(f"WARNING: The following events are not covered by any team: {missingEvents}. Would you like to assign students who want to do the events? (y/n)")
        # if userInput.strip().lower() == "y" or userInput.strip().lower() == "yes":
        #     handleMissingEvents(missingEvents)


def handleMissingEvents(missingEvents):
    print('implementation not made yet to handle missing events')

def main(maxEventFixChoice,maxTeamsForEachEvent):
    createListofStudents()
    createListofTeams()
    if maxEventFixChoice == 1:
        for team in Teams:
            if maxTeamsForEachEvent == "":
                raise Exception("Please enter a number for the max teams for each event, or uncheck the box")
            team.checkMaxEvents(int(maxTeamsForEachEvent))

    for student in Students:
        student.checkForOverlappingEvents()

    checkIfAllEventsCovered()

    team_data = {
        'Team Number': [team.teamNumber for team in Teams],
        'Event': [team.event for team in Teams],
        'Members': [', '.join([member.name for member in team.members]) for team in Teams],
    }
    team_df = pd.DataFrame(team_data)

    student_data = {
        'Student Name': [student.name for student in Students],
        'Teams': [', '.join([f"Team {team}" for team in student.teams]) for student in Students],
    }

    student_df = pd.DataFrame(student_data)
    try:
        student_df.to_excel("students.xlsx")
        team_df.to_excel("teams.xlsx")
        print("successfully made excel files")
    except PermissionError:
        raise Exception('Please close all excel files before running the program!')

