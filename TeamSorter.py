import pandas as pd

form = pd.read_csv('form.csv')

Students = []
amtOfEventsPerStudent = 5
team_dict = {}
Teams = []
maxTeamsForEachEvent = 3

teamCounter = 1


def createListofStudents():
    numberOfStudents = form.shape[0]
    names = []  # names of students

    i = 0
    for i in range(numberOfStudents):
        names.append(form.iat[i, 1])
        i += 1
    j = 0
    for j in range(numberOfStudents):
        names[j] = Student(names[j], form.iat[j, 3], form.iat[j, 5], form.iat[j, 7], form.iat[j, 9], form.iat[j, 11],
                           form.iat[j, 4], form.iat[j, 6], form.iat[j, 8], form.iat[j, 10], form.iat[j, 12])
        Students.append(names[j])
        j += 1

    k = 0
    for k in range(numberOfStudents):
        Students[k].partnerValuesToObjects()
        k += 1


class Student:
    def __init__(self, name, event1, event2, event3, event4, event5, partnersEvent1, partnersEvent2, partnersEvent3,
                 partnersEvent4, partnersEvent5):
        self.teams = []

        self.name = name
        self.firstEvent = str(event1)
        self.secondEvent = str(event2)
        self.thirdEvent = str(event3)
        self.fourthEvent = str(event4)
        self.fifthEvent = str(event5)
        self.events = [self.firstEvent, self.secondEvent, self.thirdEvent, self.fourthEvent, self.fifthEvent]

        self.partnersForFirstEvent = self.extract_partner_list(partnersEvent1)
        self.partnersForSecondEvent = self.extract_partner_list(partnersEvent2)
        self.partnersForThirdEvent = self.extract_partner_list(partnersEvent3)
        self.partnersForFourthEvent = self.extract_partner_list(partnersEvent4)
        self.partnersForFifthEvent = self.extract_partner_list(partnersEvent5)
        self.partners = [self.partnersForFirstEvent, self.partnersForSecondEvent, self.partnersForThirdEvent,
                         self.partnersForFourthEvent, self.partnersForFifthEvent]

    def partnerValuesToObjects(self):
        for i in range(amtOfEventsPerStudent):
            if isinstance(self.partners[i], list):
                for j in range(len(self.partners[i])):
                    partner_name = self.partners[i][j]
                    if partner_name:
                        # Use strip() and lower() to normalize the strings for comparison
                        for student in Students:
                            if str(partner_name).strip().lower() == str(student.name).strip().lower():
                                self.partners[i][j] = student
            elif self.partners[i] is not None:
                # Handle the case where self.partners[i] is not a list
                partner_name = self.partners[i]
                for student in Students:
                    if str(partner_name).strip().lower() == str(student.name).strip().lower():
                        self.partners[i] = student

    def extract_partner_list(self, partners_str):
        if partners_str is None:
            return []
        elif isinstance(partners_str, str) and "," in partners_str:
            return [partner.strip() for partner in partners_str.split(",")]
        elif isinstance(partners_str, str):
            return [partners_str.strip()]
        else:
            return []  # Handle the case where partners_str is not a string or is None

    def checkForOverlappingEvents(self):
        overlapping_event_sets = {
            "row 1": set(["Anatomy & Physiology", "Dynamic Planet", "Wind Power"]),
            "row 2": set(["Can't Judge a Powder", "Ecology", "WIDI"]),
            "row 3": set(["Experimental Design", "Fossils", "Microbe Mission"]),
            "row 4": set(["Disease Detectives", "Fast Facts", "Meteorology"]),
            "row 5": set(["Code Busters", "Forestry", "Reach for the Stars"]),
            "row 6": set(["Crime Busters", "Optics", "Road Scholar"])
        }

        for set_name, event_set in overlapping_event_sets.items():
            overlapping_events = [event for event in self.events if event in event_set]
            if len(overlapping_events) > 1:
                print(
                    f'WARNING: STUDENT {self.name} HAS OVERLAPPING EVENTS IN {set_name} of the Overlapping Events image')


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
            self.groupEventPreference = (person1EventPreference + person2EventPreference) / 2
        else:
            self.members = [person1, person2, person3]
            self.groupEventPreference = (person1EventPreference + person2EventPreference + person3EventPreference) / 3
            person3.teams.append(teamNumber)
        self.event = event

    def checkMaxEvents(self):
        TeamsWithSameEvent = [self]
        for team in Teams:
            if team != self:
                if team.event == self.event:
                    TeamsWithSameEvent.append(team)
        userOptOut = False
        while len(TeamsWithSameEvent) > maxTeamsForEachEvent and not userOptOut:
            maxEventsFixDecision = input(
                f"MAX EVENT # REACHED: There are more than {maxTeamsForEachEvent} teams for event {self.event}. Would you like to assign a random event to one (or more) of these groups (random)? Y or N ")
            if maxEventsFixDecision.lower() == "yes" or maxEventsFixDecision.lower() == "y":
                min_group_event_preference = max(team.groupEventPreference for team in TeamsWithSameEvent)

                teams_with_lowest_preference = [team for team in TeamsWithSameEvent if
                                                team.groupEventPreference == min_group_event_preference]
                teamRemoved = []
                for team in teams_with_lowest_preference:
                    teamRemoved = team
                    TeamsWithSameEvent.remove(teamRemoved)

                teamRemoved.event = "Preferred Event was full, ask group which event they would like instead"

                print(
                    f"Team {teamRemoved.teamNumber} with the minimum group event preference for {self.event} has been removed.")
            elif maxEventsFixDecision.lower() == "no" or maxEventsFixDecision.lower() == "n":
                userOptOut = True


def createTeam(person1, person2, event, person1EventPreference, person2EventPreference, person3=None, person3EventPreference=None):
    global teamCounter

    # Check if a team with the same members and event already exists
    for team in Teams:
        if team.event == event:  # Ensure the same event
            if person3:
                if set([person1, person2, person3]) == set(team.members):
                    return  # A team with the same members and event already exists
            else:
                if set([person1, person2]) == set(team.members):
                    return  # A team with the same members and event already exists

    # If no matching team is found, create a new team
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



def createTeamIfNoPartner():
    for student1 in Students:
        for student2 in Students:
            if student1 != student2:
                for index, partner in enumerate(student1.partners):
                    for otherIndex, otherPartner in enumerate(student2.partners):
                        if not partner and not otherPartner:
                            if student1.events[index] != 'nan' and student2.events[otherIndex] != 'nan':
                                if student1.events[index] != 'Experimental Design' and student1.events[
                                    index] != 'Code Busters' and student2.events[
                                    otherIndex] != "Experimental Design" and student2.events[
                                    otherIndex] != "Code Busters":
                                    student1.partners[index] = [student2]
                                    student2.partners[otherIndex] = [student1]

                                    event  = None
                                    # check who wants to do their event more
                                    if index < otherIndex: #  lower index = higher preference
                                        student1.events[index] = student1.events[index]
                                        student2.events[otherIndex] = student1.events[index]
                                        event = student1.events[index]
                                    else:
                                        student1.events[index] = student2.events[otherIndex]
                                        student2.events[otherIndex] = student2.events[otherIndex]
                                        event = student2.events[otherIndex]

                                    person3 = None
                                    person3EventPref = None
                                    createTeam(student1,student2,event,index,otherIndex,person3,person3EventPref)
                                else:
                                    raise Exception(
                                        f'{student1.name} or {student2.name} do not have partners down for a 3 person event (experimental design or code busters)')



def createTeams():
    createTeamIfNoPartner()
    # Iterate through each student
    for student1 in Students:
        # Iterate through all other students
        for student2 in Students:
            if student1 != student2:  # not comparing the same student
                for partner in student2.partners:
                    event = None
                    student3 = None
                    person3EventPreference = None
                    person2EventPreference = None
                    person1EventPreference = None
                    if not partner:
                        break

                    if len(partner) == 2:  # check if in the partners list there is a list of 2 people, indicating a 3 person team
                        if partner[0] == student1:
                            student3 = partner[1]
                        elif partner[1] == student1:
                            student3 = partner[0]
                        else:
                            raise Exception('failed to locate 3rd partner in 1 or more groups that contain 3 members')

                        # find event index
                        for index, partner3 in enumerate(student3.partners):
                            if len(partner3) == 2:
                                if set(partner3) == set([student1, student2]):
                                    event = student3.events[index]
                                    person3EventPreference = index
                                    break

                        for index, partner2 in enumerate(student2.partners):
                            if len(partner2) == 2:
                                if set(partner2) == set([student1, student3]):
                                    person2EventPreference = index
                                    break

                        for index, partner1 in enumerate(student1.partners):
                            if len(partner1) == 2:
                                if set(partner1) == set([student2, student3]):
                                    person1EventPreference = index
                                    break
                        createTeam(student1, student2, event, person1EventPreference, person2EventPreference, student3,
                                   person3EventPreference)

                    elif student1 == partner[0]:  # 2-person team
                        for index, partner1 in enumerate(student1.partners):
                            if len(partner1) == 1:
                                if partner1[0] == student2:
                                    event = student1.events[index]
                                    person1EventPreference = index

                        for index, partner2 in enumerate(student2.partners):

                            if len(partner2) == 1:
                                if partner2[0] == student1:
                                    person2EventPreference = index
                        createTeam(student1, student2, event, person1EventPreference, person2EventPreference, student3,
                                   person3EventPreference)


def main():
    createListofStudents()
    createTeams()


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
    except PermissionError:
        raise Exception('Please close all excel files before running the program!')


if __name__ == "__main__":
    main()
