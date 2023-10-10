import pandas as pd

form = pd.read_csv('form.csv')
numberOfStudents = form.shape[0]

Students = []
amtOfEventsPerStudent = 5
team_dict = {}

teamCounter = 0


def createListofStudents():
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


class Student:
    def __init__(self, name, event1, event2, event3, event4, event5, partnersEvent1, partnersEvent2, partnersEvent3,
                 partnersEvent4, partnersEvent5):
        self.name = name
        self.firstEvent = event1
        self.secondEvent = event2
        self.thirdEvent = event3
        self.fourthEvent = event4
        self.fifthEvent = event5
        self.events = [event1, event2, event3, event4, event5]

        if "," in partnersEvent1:
            partnersEvent1 = partnersEvent1.split(",")
        try:
            if "," in partnersEvent2:
                partnersEvent2 = partnersEvent2.split(",")
        except TypeError:
            partnersEvent2 = None
        try:
            if "," in partnersEvent3:
                partnersEvent3 = partnersEvent3.split(",")
        except TypeError:
            partnersEvent3 = None
        try:
            if "," in partnersEvent4:
                partnersEvent4 = partnersEvent4.split(",")
        except TypeError:
            partnersEvent4 = None
        try:
            if "," in partnersEvent5:
                partnersEvent5 = partnersEvent5.split(",")
        except TypeError:
            partnersEvent5 = None


        self.partnersFirstEvent = partnersEvent1
        self.partnersSecondEvent = partnersEvent2
        self.partnersThirdEvent = partnersEvent3
        self.partnersFourthEvent = partnersEvent4
        self.partnersFifthEvent = partnersEvent5
        self.partners = [partnersEvent1, partnersEvent2, partnersEvent3, partnersEvent4, partnersEvent5]


class Team:
    def __init__(self, person1, person2, person3, event):
        self.members = [person1, person2, person3]
        self.event = event


def createTeam(person1, person2, person3=None):
    global teamCounter
    if person3 is not None:
        team_dict[f"Team {teamCounter}"] = Team(person1, person2, person3)
    else:
        team_dict[f"Team {teamCounter}"] = Team(person1, person2)

    teamCounter += 1


def compare_names(student, partner):
    if isinstance(partner, list):
        for p in partner:
            if compare_names(student, p):
                return True
        return False
    return student == partner

def createTeams():

    if compare_names(Students[0].name, Students[1].partners[1]):
        if isinstance(Students[1].partners[1], list):
            createTeam(Students[0].name, Students[1].partners[1][0], Students[1].partners[1][1])
        else:

            createTeam(Students[0].name, Students[1].partners[1], )
    # students = 0
    # for students in range(len(Students)):
    #     otherStudents = 0  # Reset otherStudents for each student
    #     for otherStudents in range(len(Students)):
    #         for i in range(amtOfEventsPerStudent):
    #             print(Students[students].name, Students[otherStudents].partners[i])
    #
    #             if compare_names(Students[students].name, Students[otherStudents].partners[i]):
    #                 createTeam(Students[students].name, Students[otherStudents].partners[i])
    #             i += 1
    #         otherStudents += 1
    #     students += 1

def main():
    createListofStudents()
    createTeams()
    i = 0
    print(team_dict)

if __name__ == "__main__":
    main()
