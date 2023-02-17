import random
import pandas as pd

#This is the parent class for all subcategories of user type.
class Subject:
    def __init__(self, firstName, lastName, gender, interests, ID):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.ID = ID
        self.social = random.randint(0, 100)
        #connectData here is used for the edge data in gephi
        self.connectData = []
        self.connectMembers = []
        self.timeline = []
        self.interests = interests
        self.compromised = False
        self.historicCompromise = False
        self.mitigationFlag = False
        self.mitigationCount = 0
        self.disinfoAgent = False
        self.disinfoSubject = random.choice(self.interests)

        #note: these are the behaviour variables that need to change between subject types
        self.checkAmountUpperBound = 20
        self.checkAmountLowerBound = 15
        self.shareChanceUpperBound = 75
        self.shareChanceLowerBound = 25
        self.createChance = 1
        self.wakeTimeDefault = 960
        self.sleepTimeDefault = 480
        self.activeTimeDefaultUpper = 4
        self.activeTimeDefaultLower = 3
        self.inactiveTimeDefaultUpper = 20
        self.inactiveTimeDefaultLower = 15
        self.userType = "Default"

        #On initiation the subject will either be asleep or awake, this randomly determines
        #which one is true. If the subject is asleep then research suggests that the subject
        #will begin checking their social media once they wake up so they'll default to active.
        #if the subject is awake then another random determination will be made to see if the
        #user is currently active or inactive.
        s = random.randint(0,1)
        if s == 0:
            self.wakeTime = 0
            self.sleepTime = random.randint(1, self.sleepTimeDefault)
            self.activeTime = random.randint(1, self.activeTimeDefaultUpper)
            self.inactiveTime = 0
        elif s == 1:
            self.sleepTime = 0
            self.wakeTime = random.randint(1, self.wakeTimeDefault)
            q = random.randint(0,1)
            if q == 0:
                self.activeTime = random.randint(1, self.activeTimeDefaultUpper)
                self.inactiveTime = 0
            elif q == 1:
                self.inactiveTime = random.randint(1, self.inactiveTimeDefaultUpper)
                self.activeTime = 0
        


    def getName(self):
        name = self.firstName + " " + self.lastName
        return name

    # This is the method to network users to one another.
    def network(self, other):

        # This variable is derived from the difference in the social value between two subjects
        q = abs(self.social - other.social)

        # This variable is a random figure between 0 and 100 and is used to determine whether the subjects will network.
        #Performers will be disinclined to follow other users except for performers. Habitual and casual users will be
        #more inclined to follow performers for entertainment value.
        if other.userType == "Performer" and self.userType != "Performer" and self.userType != "Investigator":
            s = random.randint (10, 60)
        elif self.userType == "Performer" and other.userType != "Performer":
            s = random.randint(0, 10)
        elif self.userType == "Performer" and other.userType == "Performer":
            s = random.randint(10, 30)
        else:
            s = random.randint(0, 30)

        # If the s value is higher than the q value a connection will occur. If not then there will be no connection.
        if s > q:
            self.connectData.append([self.ID, other.ID, 'directed'])
            self.connectMembers.append(other)
            return
        else:
            return

    #this method runs a check on the subject's current level of activity. It is intended to run once after each cycle
    #of the simulation. The variables for activity, inactivity and waking or sleeping will count down. Once either
    #variable finishes counting down the corresponding other will refill to the default. If the waking variable runs
    #down then the inactivity variable will default to 0 and the activity variable will refill so they can resume
    #activity once they wake up.
    def activityCheck(self):
        if self.sleepTime > 0:
            self.sleepTime -= 1
            if self.sleepTime == 0:
                self.wakeTime = self.wakeTimeDefault
        elif self.inactiveTime > 0:
            self.inactiveTime -= 1
            self.wakeTime -= 1
            if self.inactiveTime == 0:
                self.activeTime = random.randint(self.activeTimeDefaultLower, self.activeTimeDefaultUpper)
            if self.wakeTime == 0:
                self.sleepTime = self.sleepTimeDefault
                self.inactiveTime = 0
                self.activeTime = random.randint(self.activeTimeDefaultLower, self.activeTimeDefaultUpper)
        elif self.activeTime > 0:
            self.activeTime -= 1
            self.wakeTime -= 1
            if self.activeTime == 0:
                self.inactiveTime = random.randint(self.inactiveTimeDefaultLower, self.inactiveTimeDefaultUpper)
            if self.wakeTime == 0:
                self.sleepTime = self.sleepTimeDefault
                self.activeTime = random.randint(self.activeTimeDefaultLower, self.activeTimeDefaultUpper)

    #mitigated users will not exectue the functionality of non-mitigated users, this is assigned manually through
    #breaks in the simulation to determine areas within the network that spread of disinformation can be mitigated.
    def mitigationCountDown(self):
        if self.mitigationCount > 0:
            self.mitigationCount -= 1
        else:
            self.mitigationFlag = False


    #used to check content against the users interests
    def checkContent(self, content):
        s = random.randint(0, 100)
        q = random.randint(0,50)
        lifeSpanTotal = 100/content.lifeSpanTotal
        lifeSpanChance = content.lifeSpan * lifeSpanTotal

        if q < lifeSpanChance:
            if content.submatter in self.interests:
                if s < self.shareChanceUpperBound:
                    self.updatetl(content)
                    return
                else:
                    return
            elif s < self.shareChanceLowerBound:
                self.updatetl(content)
                return
            else:
                return
        else:
            return

    #this method will update the timeline of the user, attaching the most recent item of content to the front
    #and removed the item of content that was available the longest from the back. If there is an item of
    #disinformation in the timeline then the compromise variable is set to true along with a historic compromise
    #variable. If the timeline contains no disinfo then the compromise variable is set to False, but the historic
    #compromise variable remains true.
    def updatetl(self, content):
        self.timeline.insert(0,content)
        if len(self.timeline) > 20:
            self.timeline.pop()
        compromiseCheck = False
        for i in self.timeline:
            if i.authenticity == False:
                self.compromised = True
                compromiseCheck = True
                self.historicCompromise = True
        if compromiseCheck == False:
            self.compromised = False


    #this method will check the timeline positions of each person the subject follows one after another
    #once a full cycle has been completed it will check each subsequent position of each member. It will repeat
    #this until all items have been checked.
    def observetl(self):
        p = random.randint(self.checkAmountLowerBound, self.checkAmountUpperBound)
        q = p - 1
        for i in range(0, p):
            for j in self.connectMembers:
                self.checkContent(j.timeline[q])
            q -= 1

    #This method creates an item of content for the subject. It's a slightly inelegant solution
    #as it references a method from the sim class and passes itself as an argument. It works otherwise!
    def createContent(self, sim):
        s = random.randint(0, 100)
        if s <= self.createChance:
            subject = random.choice(self.interests)
            sim.genContent(True, self, subject, sim.contentLifeSpan, sim.contentLifeSpan, 'new')

class Casual(Subject):
    def __init__(self, firstName, lastName, gender, interests, ID):
        super().__init__(firstName,lastName,gender,interests,ID)
        self.userType = "Casual"
        self.checkAmountUpperBound = 10
        self.checkAmountLowerBound = 6
        self.shareChanceUpperBound = 99
        self.shareChanceLowerBound = 50
        self.createChance = 30
        
class Habitual(Subject):
    def __init__(self, firstName, lastName, gender, interests, ID):
        super().__init__(firstName,lastName,gender,interests,ID)
        self.userType = "Habitual"
        self.checkAmountUpperBound = 20
        self.checkAmountLowerBound = 5
        self.shareChanceUpperBound = 60
        self.shareChanceLowerBound = 30
        self.createChance = 40

class Investigator(Subject):
    def __init__(self, firstName, lastName, gender, interests, ID):
        super().__init__(firstName,lastName,gender,interests,ID)
        self.userType = "Investigator"
        self.checkAmountUpperBound = 20
        self.checkAmountLowerBound = 15
        self.shareChanceUpperBound = 50
        self.shareChanceLowerBound = 25
        self.createChance = 30
        
class Performer(Subject):
    def __init__(self, firstName, lastName, gender, interests, ID):
        super().__init__(firstName,lastName,gender,interests,ID)
        self.userType = "Performer"
        self.checkAmountUpperBound = 10
        self.checkAmountLowerBound = 6
        self.shareChanceUpperBound = 40
        self.shareChanceLowerBound = 10
        self.createChance = 80


class Content:
    contentID = 0
    def __init__(self, ID, authenticity, submatter, lifespan, lifespanCurrent, type):
        self.ID = ID
        self.authenticity = authenticity
        self.submatter = submatter
        self.lifeSpanTotal = lifespan
        self.lifeSpan = lifespanCurrent
        self.type = type

    def degradation(self):
        if self.lifeSpan > 1:
            self.lifeSpan -= 1


class Simulation:
    malenames = ["Liam", "Noah", "Oliver", "William", "Elijah", "James", "Benjamin", "Lucas", "Mason", "Ethan",
                 "Alexander",
                 "Henry", "Jacob", "Michael", "Daniel", "Logan", "Jackson", "Sebastian", "Jack", "Aiden", "Owen",
                 "Samuel",
                 "Matthew", "Joseph", "Levi", "Mateo", "David", "John", "Wyatt", "Carter", "Julian", "Luke", "Grayson",
                 "Isaac", "Jayden", "Theodore", "Gabriel", "Anthony", "Dylan", "Leo", "Lincoln", "Jaxon", "Asher",
                 "Christopher", "Josiah", "Andrew", "Thomas", "Joshua", "Ezra", "Hudson", "Charles", "Caleb", "Isaiah",
                 "Ryan", "Nathan", "Adrian", "Christian", "Maverick", "Colton", "Elias", "Aaron", "Eli", "Landon",
                 "Jonathan",
                 "Nolan", "Hunter", "Cameron", "Connor", "Santiago", "Jeremiah", "Ezekiel", "Angel", "Roman", "Easton",
                 "Miles", "Robert", "Jameson", "Nicholas", "Greyson", "Cooper", "Ian", "Carson", "Axel", "Jaxson",
                 "Dominic",
                 "Leonardo", "Luca", "Austin", "Jordan", "Adam", "Xavier", "Jose", "Jace", "Everett", "Declan", "Evan",
                 "Kayden", "Parker", "Wesley", "Kai", "Brayden", "Bryson", "Weston", "Jason", "Emmett", "Sawyer",
                 "Silas",
                 "Bennett", "Brooks", "Micah", "Damian", "Harrison", "Waylon", "Ayden", "Vincent", "Ryder", "Kingston",
                 "Rowan", "George", "Luis", "Chase", "Cole", "Nathaniel", "Zachary", "Ashton", "Braxton", "Gavin",
                 "Tyler",
                 "Diego", "Bentley", "Amir", "Beau", "Gael", "Carlos", "Ryker", "Jasper", "Max", "Juan", "Ivan",
                 "Brandon",
                 "Jonah", "Giovanni", "Kaiden", "Myles", "Calvin", "Lorenzo", "Maxwell", "Jayce", "Kevin", "Legend",
                 "Tristan", "Jesus", "Jude", "Zion", "Justin", "Maddox", "Abel", "King", "Camden", "Elliott", "Malachi",
                 "Milo", "Emmanuel", "Karter", "Rhett", "Alex", "August", "River", "Xander", "Antonio", "Brody", "Finn",
                 "Elliot", "Dean", "Emiliano", "Eric", "Miguel", "Arthur", "Matteo", "Graham", "Alan", "Nicolas",
                 "Blake",
                 "Thiago", "Adriel", "Victor", "Joel", "Timothy", "Hayden", "Judah", "Abraham", "Edward", "Messiah",
                 "Zayden",
                 "Theo", "Tucker", "Grant", "Richard", "Alejandro", "Steven", "Jesse", "Dawson", "Bryce", "Avery",
                 "Oscar",
                 "Patrick", "Archer", "Barrett", "Leon", "Colt", "Charlie", "Peter", "Kaleb", "Lukas", "Beckett",
                 "Jeremy",
                 "Preston", "Enzo", "Luka", "Andres", "Marcus", "Felix", "Mark", "Ace", "Brantley", "Atlas",
                 "Remington",
                 "Maximus", "Matias", "Walker", "Kyrie", "Griffin", "Kenneth", "Israel", "Javier", "Kyler", "Jax",
                 "Amari",
                 "Zane", "Emilio", "Knox", "Adonis", "Aidan", "Kaden", "Paul", "Omar", "Brian", "Louis", "Caden",
                 "Maximiliano", "Holden", "Paxton", "Nash", "Bradley", "Bryan", "Simon", "Phoenix", "Lane", "Josue",
                 "Colin",
                 "Rafael", "Kyle", "Riley", "Jorge", "Beckham", "Cayden", "Jaden", "Emerson", "Ronan", "Karson", "Arlo",
                 "Tobias", "Brady", "Clayton", "Francisco", "Zander", "Erick", "Walter", "Daxton", "Cash", "Martin",
                 "Damien",
                 "Dallas", "Cody", "Chance", "Jensen", "Finley", "Jett", "Corbin", "Kash", "Reid", "Kameron", "Andre",
                 "Gunner", "Jake", "Hayes", "Manuel", "Prince", "Bodhi", "Cohen"]

    femalenames = ["Olivia", "Emma", "Ava", "Sophia", "Isabella", "Charlotte", "Amelia", "Mia", "Harper", "Evelyn",
                   "Abigail",
                   "Emily", "Ella", "Elizabeth", "Camila", "Luna", "Sofia", "Avery", "Mila", "Aria", "Scarlett",
                   "Penelope",
                   "Layla", "Chloe", "Victoria", "Madison", "Eleanor", "Grace", "Nora", "Riley", "Zoey", "Hannah",
                   "Hazel",
                   "Lily", "Ellie", "Violet", "Lillian", "Zoe", "Stella", "Aurora", "Natalie", "Emilia", "Everly",
                   "Leah",
                   "Aubrey", "Willow", "Addison", "Lucy", "Audrey", "Bella", "Nova", "Brooklyn", "Paisley", "Savannah",
                   "Claire", "Skylar", "Isla", "Genesis", "Naomi", "Elena", "Caroline", "Eliana", "Anna", "Maya",
                   "Valentina",
                   "Ruby", "Kennedy", "Ivy", "Ariana", "Aaliyah", "Cora", "Madelyn", "Alice", "Kinsley", "Hailey",
                   "Gabriella",
                   "Allison", "Gianna", "Serenity", "Samantha", "Sarah", "Autumn", "Quinn", "Eva", "Piper", "Sophie",
                   "Sadie",
                   "Delilah", "Josephine", "Nevaeh", "Adeline", "Arya", "Emery", "Lydia", "Clara", "Vivian", "Madeline",
                   "Peyton", "Julia", "Rylee", "Brielle", "Reagan", "Natalia", "Jade", "Athena", "Maria", "Leilani",
                   "Everleigh", "Liliana", "Melanie", "Mackenzie", "Hadley", "Raelynn", "Kaylee", "Rose", "Arianna",
                   "Isabelle", "Melody", "Eliza", "Lyla", "Katherine", "Aubree", "Adalynn", "Kylie", "Faith", "Mary",
                   "Margaret", "Ximena", "Iris", "Alexandra", "Jasmine", "Charlie", "Amaya", "Taylor", "Isabel",
                   "Ashley",
                   "Khloe", "Ryleigh", "Alexa", "Amara", "Valeria", "Andrea", "Parker", "Norah", "Eden", "Elliana",
                   "Brianna", "Emersyn", "Valerie", "Anastasia", "Eloise", "Emerson", "Cecilia", "Remi", "Josie",
                   "Alina", "Reese", "Bailey", "Lucia", "Adalyn", "Molly", "Ayla", "Sara", "Daisy", "London", "Jordyn",
                   "Esther", "Genevieve", "Harmony", "Annabelle", "Alyssa", "Ariel", "Aliyah", "Londyn", "Juliana",
                   "Morgan", "Summer", "Juliette", "Trinity", "Callie", "Sienna", "Blakely", "Alaia", "Kayla", "Teagan",
                   "Alaina", "Brynlee", "Finley", "Catalina", "Sloane", "Rachel", "Lilly", "Ember", "Kimberly",
                   "Juniper",
                   "Sydney", "Arabella", "Gemma", "Jocelyn", "Freya", "June", "Lauren", "Amy", "Presley", "Georgia",
                   "Journee", "Elise", "Rosalie", "Ada", "Laila", "Brooke", "Diana", "Olive", "River", "Payton",
                   "Ariella",
                   "Daniela", "Raegan", "Alayna", "Gracie", "Mya", "Blake", "Noelle", "Ana", "Leila", "Paige", "Lila",
                   "Nicole", "Rowan", "Hope", "Ruth", "Alana", "Selena", "Marley", "Kamila", "Alexis", "Mckenzie",
                   "Zara",
                   "Millie", "Magnolia", "Kali", "Kehlani", "Catherine", "Maeve", "Adelyn", "Sawyer", "Elsie", "Lola",
                   "Jayla", "Adriana", "Journey", "Vera", "Aspen", "Joanna", "Alivia", "Angela", "Dakota", "Camille",
                   "Nyla", "Tessa", "Brooklynn", "Malia", "Makayla", "Rebecca", "Fiona", "Mariana", "Lena", "Julianna",
                   "Vanessa", "Juliet", "Camilla", "Kendall", "Harley", "Cali", "Evangeline", "Mariah", "Jane", "Zuri",
                   "Elaina", "Sage", "Amira", "Adaline", "Lia", "Charlee", "Delaney", "Lilah", "Miriam", "Angelina",
                   "Mckenna", "Aniyah", "Phoebe", "Michelle", "Thea", "Hayden", "Maggie", "Lucille", "Amiyah", "Annie",
                   "Alexandria", "Myla"]

    lastNames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
                 "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
                 "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez",
                 "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart",
                 "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
                 "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks",
                 "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez",
                 "Castillo",
                 "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry",
                 "Russell",
                 "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez",
                 "Simmons",
                 "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace",
                 "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar",
                 "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "Mcdonald",
                 "Woods",
                 "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman",
                 "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva", "Shaw",
                 "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black",
                 "Robertson",
                 "Boyd", "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza",
                 "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant",
                 "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos",
                 "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll",
                 "Lane",
                 "Riley", "Andrews", "Alvarado", "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston",
                 "Matthews",
                 "Pena", "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George",
                 "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene", "Nunez", "Wheeler", "Valdez", "Harper",
                 "Burke", "Larson", "Santiago", "Maldonado", "Morrison", "Franklin", "Carlson", "Austin", "Dominguez",
                 "Carr", "Lawson", "Jacobs", "Obrien", "Lynch", "Singh", "Vega", "Bishop", "Montgomery", "Oliver",
                 "Jensen", "Harvey", "Williamson", "Gilbert", "Dean", "Sims", "Espinoza", "Howell", "Li", "Wong",
                 "Reid",
                 "Hanson", "Le", "Mccoy", "Garrett", "Burton", "Fuller", "Wang", "Weber", "Welch", "Rojas", "Lucas",
                 "Marquez", "Fields", "Park", "Yang", "Little", "Banks", "Padilla", "Day", "Walsh", "Bowman", "Schultz",
                 "Luna", "Fowler", "Mejia", "Davidson", "Acosta", "Brewer", "May", "Holland", "Juarez", "Newman",
                 "Pearson",
                 "Curtis", "Cortez", "Douglas", "Schneider", "Joseph", "Barrett", "Navarro", "Figueroa", "Keller",
                 "Avila",
                 "Wade", "Molina", "Stanley", "Hopkins", "Campos", "Barnett", "Bates", "Chambers", "Caldwell", "Beck",
                 "Lambert", "Miranda", "Byrd", "Craig", "Ayala", "Lowe", "Frazier", "Powers", "Neal", "Leonard",
                 "Gregory",
                 "Carrillo", "Sutton", "Fleming", "Rhodes", "Shelton", "Schwartz", "Norris", "Jennings", "Watts",
                 "Duran",
                 "Walters", "Cohen", "Mcdaniel", "Moran", "Parks", "Steele", "Vaughn", "Becker", "Holt", "Deleon",
                 "Barker",
                 "Terry", "Hale", "Leon", "Hail", "Benson", "Haynes", "Horton", "Miles", "Lyons", "Pham", "Graves",
                 "Bush",
                 "Thornton", "Wolfe", "Warner", "Cabrera", "Mckinney", "Mann", "Zimmerman", "Dawson", "Lara",
                 "Fletcher",
                 "Page", "Mccarthy", "Love", "Robles", "Cervantes", "Solis", "Erickson", "Reeves", "Chang", "Klein",
                 "Salinas", "Fuentes", "Baldwin", "Daniel", "Simon", "Velasquez", "Hardy", "Higgins", "Aguirre", "Lin",
                 "Cummings", "Chandler", "Sharp", "Barber", "Bowen", "Ochoa", "Dennis", "Robbins", "Liu", "Ramsey",
                 "Francis", "Griffith", "Paul", "Blair", "Oconnor", "Cardenas", "Pacheco", "Cross", "Calderon", "Quinn",
                 "Moss", "Swanson", "Chan", "Rivas", "Khan", "Rodgers", "Serrano", "Fitzgerald", "Rosales", "Stevenson",
                 "Christensen", "Manning", "Gill", "Curry", "Mclaughlin", "Harmon", "Mcgee", "Gross", "Doyle", "Garner",
                 "Newton", "Burgess", "Reese", "Walton", "Blake", "Trujillo", "Adkins", "Brady", "Goodman", "Roman",
                 "Webster", "Goodwin", "Fischer", "Huang", "Potter", "Delacruz", "Montoya", "Todd", "Wu", "Hines",
                 "Mullins", "Castaneda", "Malone", "Cannon", "Tate", "Mack", "Sherman", "Hubbard", "Hodges", "Zhang",
                 "Guerra", "Wolf", "Valencia", "Franco", "Saunders", "Rowe", "Gallagher", "Farmer", "Hammond",
                 "Hampton",
                 "Townsend", "Ingram", "Wise", "Gallegos", "Clarke", "Barton", "Schroeder", "Maxwell", "Waters",
                 "Logan",
                 "Camacho", "Strickland", "Norman", "Person", "Colon", "Parsons", "Frank", "Harrington", "Glover",
                 "Osborne", "Buchanan", "Casey", "Floyd", "Patton", "Ibarra", "Ball", "Tyler", "Suarez", "Bowers",
                 "Orozco", "Salas", "Cobb", "Gibbs", "Andrade", "Bauer", "Conner", "Moody", "Escobar", "Mcguire",
                 "Lloyd",
                 "Mueller", "Hartman", "French", "Kramer", "Mcbride", "Pope", "Lindsey", "Velazquez", "Norton",
                 "Mccormick",
                 "Sparks", "Flynn", "Yates", "Hogan", "Marsh", "Macias", "Villanueva", "Zamora", "Pratt", "Stokes",
                 "Owen",
                 "Ballard", "Lang", "Brock", "Villarreal", "Charles", "Drake", "Barrera", "Cain", "Patrick", "Pineda",
                 "Burnett", "Mercado", "Santana", "Shepherd", "Bautista", "Ali", "Shaffer", "Lamb", "Trevino",
                 "Mckenzie",
                 "Hess", "Beil", "Olsen", "Cochran", "Morton", "Nash", "Wilkins", "Petersen", "Briggs", "Shah", "Roth",
                 "Nicholson", "Holloway", "Lozano", "Flowers", "Rangel", "Hoover", "Arias", "Short", "Mora",
                 "Valenzuela",
                 "Bryan", "Meyers", "Weiss", "Underwood", "Bass", "Greer", "Summers", "Houston", "Carson", "Morrow",
                 "Clayton", "Whitaker", "Decker", "Yoder", "Collier", "Zuniga", "Carey", "Wilcox", "Melendez", "Poole",
                 "Roberson", "Larsen", "Conley", "Davenport", "Copeland", "Massey", "Lam", "Huff", "Rocha", "Cameron",
                 "Jefferson", "Hood", "Monroe", "Anthony", "Pittman", "Huynh", "Randall", "Singleton", "Kirk", "Combs",
                 "Mathis", "Christian", "Skinner", "Bradford", "Richard", "Galvan", "Wall", "Boone", "Kirby",
                 "Wilkinson",
                 "Bridges", "Bruce", "Atkinson", "Velez", "Meza", "Roy", "Vincent", "York", "Hodge", "Villa", "Abbott",
                 "Allison", "Tapia", "Gates", "Chase", "Sosa", "Sweeney", "Farrell", "Wyatt", "Dalton", "Horn",
                 "Barron",
                 "Phelps", "Yu", "Dickerson", "Heath", "Foley", "Atkins", "Mathews", "Bonilla", "Acevedo", "Benitez",
                 "Zavala", "Hensley", "Glenn", "Cisneros", "Harrell", "Shields", "Rubio", "Choi", "Huffman", "Boyer",
                 "Garrison", "Arroyo", "Bond", "Kane", "Hancock", "Callahan", "Dillon", "Cline", "Wiggins", "Grimes",
                 "Arellano", "Melton", "Oneill", "Savage", "Ho", "Beltran", "Pitts", "Parrish", "Ponce", "Rich",
                 "Booth",
                 "Koch", "Golden", "Ware", "Brennan", "Mcdowell", "Marks", "Cantu", "Humphrey", "Baxter", "Sawyer",
                 "Clay",
                 "Tanner", "Hutchinson", "Kaur", "Berg", "Wiley", "Gilmore", "Russo", "Villegas", "Hobbs", "Keith",
                 "Wilkerson", "Ahmed", "Beard", "Mcclain", "Montes", "Mata", "Rosario", "Vang", "S", "S", "Walter",
                 "Henson", "Oneal", "Mosley", "Mcclure", "Beasley", "Stephenson", "Snow", "Huerta", "Preston", "Vance",
                 "Barry", "Johns", "Eaton", "Blackwell", "Dyer", "Prince", "Macdonald", "Solomon", "Guevara",
                 "Stafford",
                 "English", "Hurst", "Woodard", "Cortes", "Shannon", "Kemp", "Nolan", "Mccullough", "Merritt",
                 "Murillo",
                 "Moon", "Salgado", "Strong", "Kline", "Cordova", "Barajas", "Roach", "Rosas", "Winters", "Jacobson",
                 "Lester", "Knox", "Bullock", "Kerr", "Leach", "Meadows", "Davila", "Orr", "Whitehead", "Pruitt",
                 "Kent",
                 "Conway", "Mckee", "Barr", "David", "Dejesus", "Marin", "Berger", "Mcintyre", "Blankenship", "Gaines",
                 "Palacios", "Cuevas", "Bartlett", "Durham", "Dorsey", "Mccall", "Odonnell", "Stein", "Browning",
                 "Stout",
                 "Lowery", "Sloan", "Mclean", "Hendricks", "Calhoun", "Sexton", "Chung", "Gentry", "Hull", "Duarte",
                 "Ellison", "Nielsen", "Gillespie", "Buck", "Middleton", "Sellers", "Leblanc", "Esparza", "Hardin",
                 "Bradshaw", "Mcintosh", "Howe", "Livingston", "Frost", "Glass", "Morse", "Knapp", "Herman", "Stark",
                 "Bravo", "Noble", "Spears", "Weeks", "Corona", "Frederick", "Buckley", "Mcfarland", "Hebert",
                 "Enriquez",
                 "Hickman", "Quintero", "Randolph", "Schaefer", "Walls", "Trejo", "House", "Reilly", "Pennington",
                 "Michael", "Conrad", "Giles", "Benjamin", "Crosby", "Fitzpatrick", "Donovan", "Mays", "Mahoney",
                 "Valentine", "Raymond", "Medrano", "Hahn", "Mcmillan", "Small", "Bentley", "Felix", "Peck", "Lucero",
                 "Boyle", "Hanna", "Pace", "Rush", "Hurley", "Harding", "Mcconnell", "Bernal", "Nava", "Ayers",
                 "Everett",
                 "Ventura", "Avery", "Pugh", "Mayer", "Bender", "Shepard", "Mcmahon", "Landry", "Case", "Sampson",
                 "Moses",
                 "Magana", "Blackburn", "Dunlap", "Gould", "Duffy", "Vaughan", "Herring", "Mckay", "Espinosa", "Rivers",
                 "Farley", "Bernard", "Ashley", "Friedman", "Potts", "Truong", "Costa", "Correa", "Blevins", "Nixon",
                 "Clements", "Fry", "Delarosa", "Best", "Benton", "Lugo", "Portillo", "Dougherty", "Crane", "Haley",
                 "Phan",
                 "Villalobos", "Blanchard", "Horne", "Finley", "Quintana", "Lynn", "Esquivel", "Bean", "Dodson",
                 "Mullen",
                 "Xiong", "Hayden", "Cano", "Levy", "Huber", "Richmond", "Moyer", "Lim", "Frye", "Sheppard", "Mccarty",
                 "Avalos", "Booker", "Waller", "Parra", "Woodward", "Jaramillo", "Krueger", "Rasmussen", "Brandt",
                 "Peralta", "Donaldson", "Stuart", "Faulkner", "Maynard", "Galindo", "Coffey", "Estes", "Sanford",
                 "Burch",
                 "Maddox", "Vo", "Oconnell", "Vu", "S", "S", "Andersen", "Spence", "Mcpherson", "Church", "Schmitt",
                 "Stanton", "Leal", "Cherry", "Compton", "Dudley", "Sierra", "Pollard", "Alfaro", "Hester", "Proctor",
                 "Lu", "Hinton", "Novak", "Good", "Madden", "Mccann", "Terrell", "Jarvis", "Dickson", "Reyna",
                 "Cantrell",
                 "Mayo", "Branch", "Hendrix", "Rollins", "Rowland", "Whitney", "Duke", "Odom", "Daugherty", "Travis",
                 "Tang"
                 ]

    submatter = ["Dog", "Cat", "Rat", "Pigeon", "Hyena", "Gorilla", "Dolphin", "Chimpanzee", "Goldfish", "Ostrich",
                 "Rooster", "Butterfly", "Cockroach", "Manatee", "Mole", "Mosquito", "Peacock", "Iguana", "Mouse",
                 "Crocodile", "Camel", "Moose", "Yak", "Budgerigar", "Prawn", "Goat", "Jaguar", "Squirrel", "Crow",
                 "Deer", "Mammoth", "Amoeba", "Goose", "Pig", "Panda"]

    def __init__(self, ID, totalCycles, breakpoint, lifespan, breakTimeBetween, autoEvaluate):
        self.ID = ID
        self.subjects = []
        self.disinfoAgents = []
        self.contentlist = []
        self.nodeframe = pd
        self.edgeframe = pd
        self.totalCycles = totalCycles
        self.remainingCycles = totalCycles
        self.iteration = 0
        self.compCount = 0
        self.breakpoint = breakpoint
        self.breakFlag = False
        self.breakTimeBetween = breakTimeBetween
        self.breakCountdown = self.breakTimeBetween
        self.autoEvaluate = autoEvaluate
        self.evaluationFlag = False
        self.disinfoScheme = "none"
        self.disinfoCount = 0
        self.disinfoTimer = 0
        self.disinfoRandomCount = 0
        self.disinfoType = "none"
        self.disinfoSubjectMatter = "none"
        self.contentLifeSpan = lifespan

    #this displays the configuration of the currently loaded sim
    def displaySim(self):
        print("Sim ID: ", self.ID)
        print("Number of subjects: ",len(self.subjects))
        print("Total cycles: ", self.totalCycles)
        print("Remaining cycles ", self.remainingCycles)

    # this loop generates the initial content to construct pre-sim timelines. it takes the contentID number
    # as a class variable and increments it by one
    def initialContent(self):
        for i in range(1, 1000):
            lifespanCurrent = random.randint(0, self.contentLifeSpan)
            self.contentlist.append(Content(Content.contentID,
                                             True,
                                             random.choice(Simulation.submatter),
                                            self.contentLifeSpan,
                                            lifespanCurrent,
                                             'initial'))
            Content.contentID += 1

    # This loop creates the subjects using the Subject constructor It requires gender
    # to first be selected (which is random) and then gives a male or female name
    # accordingly.
    def genSubjects(self, casuals, habituals, investigators, performers):
        def subjectLogic():
            gender = random.choice(['male', 'female'])
            interests = random.sample(Simulation.submatter, 5)
            if gender == 'male':
                return(random.choice(Simulation.malenames),
                                      random.choice(Simulation.lastNames),
                                      gender, interests)
            elif gender == 'female':
                return(random.choice(Simulation.femalenames),
                                              random.choice(Simulation.lastNames),
                                              gender, interests)
        for i in range(0, casuals):
            subjectTuple = subjectLogic()
            self.subjects.append(Casual(subjectTuple[0],subjectTuple[1],subjectTuple[2],subjectTuple[3],i))

        for i in range(0, habituals):
            q = casuals + i
            subjectTuple = subjectLogic()
            self.subjects.append(Habitual(subjectTuple[0],subjectTuple[1],subjectTuple[2],subjectTuple[3],q))

        for i in range(0, investigators):
            q = casuals + habituals + i
            subjectTuple = subjectLogic()
            self.subjects.append(Investigator(subjectTuple[0],subjectTuple[1],subjectTuple[2],subjectTuple[3],q))

        for i in range(0, performers):
            q = casuals + habituals + investigators + i
            subjectTuple = subjectLogic()
            self.subjects.append(Performer(subjectTuple[0],subjectTuple[1],subjectTuple[2],subjectTuple[3],q))


    # the initial timeline construction algorithm for each subject
    def genTimelines(self):
        for i in self.subjects:
            while len(i.timeline) < 20:
                i.checkContent(random.choice(self.contentlist))

    # this algorithm creates a new piece of content and appends it to the subject's timeline
    def genContent(self, authenticity, target, subject, lifespanTotal, lifespanCurrent, type):
        thisContent = Content(Content.contentID,
                                authenticity,
                                subject,
                                lifespanTotal,
                                lifespanCurrent,
                                type
                                )
        target.updatetl(thisContent)
        Content.contentID += 1

    #This method runs the user's specified disinformation scheme. It runs one of two different types of scheme, either
    #by selecting a random user to apply disinformation to, or by selecting from a pool of designated users. The subject
    #matter of the disinfo can be set as either a predefined string, one of the subject's own interests or an entirely
    #random item of subject matter.
    def runDisinfoScheme(self):
        def subjectMatterGet(subject):
            if self.disinfoType == "fixed":
                return(self.disinfoSubjectMatter)
            elif self.disinfoType == "interests":
                return(random.choice(subject.interests))
            elif self.disinfoType == "random":
                return(random.choice(Simulation.submatter))
        self.disinfoCount -= 1
        if self.disinfoCount == 0:
            self.disinfoCount = self.disinfoTimer
            if self.disinfoScheme == "random":
                for i in range(0,self.disinfoRandomCount):
                    target = random.choice(self.subjects)
                    subjectMatter = subjectMatterGet(target)
                    self.genContent(False, target, subjectMatter, self.contentLifeSpan, self.contentLifeSpan, 'disinfo')
            elif self.disinfoScheme == "pool":
                for i in self.disinfoAgents:
                    target = i
                    subjectMatter = subjectMatterGet(target)
                    self.genContent(False, target, subjectMatter, self.contentLifeSpan, self.contentLifeSpan, 'disinfo')




    # the initial networking alg:
    def networking(self):
        for i in self.subjects:
            for j in self.subjects:
                if i.getName() != j.getName():
                    i.network(j)

    #this checks the number of total compromised users in the current simulation
    def compCountUpdate(self):
        compCount = 0
        for i in self.subjects:
            if i.compromised == True:
                compCount += 1
        self.compCount = compCount

    # this method calculates the percentage total of the number of compromised subjects. if they exceed the
    # designated breakpoint percentage the method will return true in order to stop the simulation and export data
    def breakPointCheck(self):
        num = self.compCount
        denom = len(self.subjects)
        percent = num/denom * 100
        if percent >= self.breakpoint:
            self.breakFlag = True
            return(True)
        else:
            return(False)

    def breakPointNotice(self, flag):
        if flag == "firstBreak":
            print("ALERT: Disinformation breakpoint reached!")
            print(self.breakpoint, "% of total ", len(self.subjects), "subjects have been compromised.")
        else:
            print("ALERT: Re-evaluation breakpoint reached!")
        print("Data from this simulation is ready to be exported to excel or gephi.")
        if self.breakFlag == True:
            print("The next run of this simulation will execute ", self.breakTimeBetween, " cycles before re-evaluation.")
        else:
            print("The next run of this simulation will execute ", self.breakTimeBetween, " cycles before re-evaluation.")
            cont = True
            while cont:
                selection = input("break flag is FALSE but evaluation flag is TRUE. Continue evaluating simulation y/n?: ")
                if "y" in selection.lower():
                    cont = False
                    print("Re-evaluation will commence in ", self.breakTimeBetween, " cycles.")
                if "n" in selection.lower():
                    cont = False
                    self.evaluationFlag = False
                    print("Re-evaluation period over. Re-evaluation flag will be set to TRUE when next breakpoint reached.")
                    print("To disable this the auto-evaluation flag must be reconfigured from the main menu.")



    #this formats the data from the subject pool into a dictionary that can be exported into a node dataframe
    def nodeDataCollect(self):
        nodes = {'Id': [],
                 'Label': [],
                 'First Name': [],
                 'Last Name': [],
                 'Gender': [],
                 'User Type': [],
                 'Active': [],
                 'Awake': [],
                 'Disinfo Agent': [],
                 'Interests': [],
                 'Compromise': [],
                 'Historic Compromise': [],
                 'Compromise Count': [],
                 'Iteration': []
                 }

        for i in self.subjects:
            nodes['Id'].append(i.ID)
            nodes['Label'].append(i.getName())
            nodes['First Name'].append(i.firstName)
            nodes['Last Name'].append(i.lastName)
            nodes['Gender'].append(i.gender)
            nodes['User Type'].append(i.userType)
            if i.wakeTime > 0:
                nodes['Awake'].append(True)
                if i.activeTime > 0:
                    nodes['Active'].append(True)
                else:
                    nodes['Active'].append(False)
            else:
                nodes['Awake'].append(False)
                nodes['Active'].append(False)
            nodes['Disinfo Agent'].append(i.disinfoAgent)
            nodes['Interests'].append(i.interests)
            nodes['Compromise'].append(i.compromised)
            nodes['Historic Compromise'].append(i.historicCompromise)
            nodes['Compromise Count'].append(self.compCount)
            nodes['Iteration'].append(self.iteration)
        return (nodes)

    # this formats the data from the subject pool into a dictionary that can be exported into an edge dataframe
    def edgeDataCollect(self):
        edges = {'Source': [],
                 'Target': [],
                 'Type': []

                 }
        for i in self.subjects:
            edgelist = i.connectData
            for j in edgelist:
                edges['Source'].append(j[0])
                edges['Target'].append(j[1])
                edges['Type'].append(j[2])

        return (edges)

    #acquires the initial data for export to gephi
    def initialDataGet(self):
        nodes = self.nodeDataCollect()
        edges = self.edgeDataCollect()
        self.nodeframe = pd.DataFrame(nodes)
        self.edgeframe = pd.DataFrame(edges)

    # simulates an entire cycle of each subject checking the timelines of each of their followers
    # for the specified range. Number of compromised nodes is also counted.
    def simActual(self):
        for i in range(1, self.remainingCycles):
            for j in self.subjects:
                if j.inactiveTime == 0 and j.sleepTime == 0 and j.mitigationFlag == False:
                    j.observetl()
                    j.createContent(self)
                if j.mitigationFlag == True:
                    j.mitigationCountDown()
                j.activityCheck()
            self.runDisinfoScheme()
            for i in self.contentlist:
                i.degradation()
            self.compCountUpdate()
            self.remainingCycles -= 1
            self.iteration += 1
            nodes = self.nodeDataCollect()
            edges = self.edgeDataCollect()
            tempnodeframe = pd.DataFrame(nodes)
            tempedgeframe = pd.DataFrame(edges)
            self.nodeframe = pd.concat([self.nodeframe, tempnodeframe], ignore_index=True)
            self.edgeframe = pd.concat([self.edgeframe, tempedgeframe], ignore_index=True)
            if self.breakFlag == False:
                if self.breakPointCheck() == True:
                    if self.autoEvaluate == True and self.evaluationFlag == False:
                        self.evaluationFlag = True
                    self.breakFlag = True
                    self.breakCountdown = self.breakTimeBetween
                    self.breakPointNotice("firstBreak")
                    break
                elif self.evaluationFlag == True:
                    if self.breakCountdown > 1:
                        self.breakCountdown -= 1
                    else:
                        self.breakCountdown = self.breakTimeBetween
                        self.breakPointNotice("subsequent")
                        break
            elif self.breakFlag == True:
                if self.breakCountdown > 1:
                    self.breakCountdown -= 1
                else:
                    self.breakCountdown = self.breakTimeBetween
                    if self.breakPointCheck() == True:
                        self.breakPointNotice("subsequent")
                        break
                    else:
                        self.breakFlag = False
                        if self.evaluationFlag == True:
                            self.breakPointNotice("subsequent")
                            break