class Student:
    def __init__(self, zid, name):
        self.zid = zid
        self.name = name
        self.year = 1

    def advance_year(self):
        self.year += 1

    def email_address(self):
        return self.zid + "@unsw.edu.au"

    def skip_years(self, skipped_years):
        self.year += skipped_years

rob = Student("z3254687", "Robert Leonard Clifton-Everest")
hayden = Student("z3418003", "Hayden Smith")

class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def email_address(self):
        return self.code + "@cse.unsw.edu.au"

comp1531 = Course("cs1531", "Software Engineering Fundamentals")

def contact_info(authority):
    heading = f"Contact info for {authority.name}"
    body = f"You can reach {authority.name} via {authority.email_address()}"
    return heading + "\n\n" + body
