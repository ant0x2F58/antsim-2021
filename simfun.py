import random
import simob
import pickle

def buildSim():
    #these are placeholder values to keep python from throwing errors, all of them should be replaced by the user.
    cycleTotal = 300
    breakpoint = 30
    lifespan = 15
    breakTime = 5
    autoEvaluation = False
    print("Please assign the necessary values to the variables of the simulation...")
    print("The simulation needs an identifying ID (string) when referenced in save data.")
    thisID = input("Enter sim ID: ")
    print("The simulation will cycle for each minute of its intended duration. It is intended to simulate a week.\n"
          "A week requires an integer value of 10080. 72 hours requires an integer value of 4320. etc.")
    cont = True
    while cont:
        try:
            cycleTotal = int(input("Enter total number of simulation cycles: "))
            if cycleTotal <= 0:
                print("Please enter an integer value greater than 0")
            else:
                cont = False
        except:
            print("Please enter an integer value.")



    print("For each cycles of the simulation each item of content that the users share will degrade in lifespan.\n"
          "Lifespan is intended to reflect the interest users have in content for how long it's been available.\n"
          "The longer the default lifespan for content is, the longer it takes to degrade into irrelevance.\n"
          "The recommended default is 15 minutes.")
    cont = True
    while cont:
        try:
            lifespan = int(input("Enter default content lifespan: "))
            if lifespan <= 0:
                print("Please enter an integer value greater than 0")
            else:
                cont = False
        except:
            print("Please enter an integer value.")



    print("After a certain percentage of total simulated users have been compromised by disinformation the\n"
          "simulation will pause for data analysis. This should be a percentile between 1 - 99. 30 is recommended.")
    cont = True
    while cont:
        try:
            breakpoint = int(input("Enter breakpoint percentage: "))
            if breakpoint <= 0:
                print("Please enter an integer value greater than 0")
            elif breakpoint >= 100:
                print("Please enter an integer value between 1 - 100")
            else:
                cont = False
        except:
            print("Please enter an integer value.")
    print("After the simulation pauses the simulation will run for a certain number of cycles before it pauses again.\n"
          "This is to evaluate the progression of disinformation after it is initially detected.")
    cont = True
    while cont:
        try:
            breakTime = int(input("Enter the number of cycles before re-evaluation: "))
            if breakTime <= 0:
                print("Please enter an integer value greater than 0")
            else:
                cont = False
        except:
            print("Please enter an integer value.")
    print("The simulation can be set to automatically pause and re-evaluate the progression even if the total number of compromised\n"
          "users falls below the breakpoint percentage. If automatic re-evaluation is set to false then it will only break if the\n"
          "total number of compromised users remains above the breakpoint percentage. (This can late be changed in the main menu)")
    cont = True
    while cont:
        choice = input("automatically re-evaluate after breakpoint reached? (y/n): ")
        if "y" in choice.lower():
            autoEvaluation = True
            cont = False
        elif "n" in choice.lower():
            autoEvaluation = False
            cont = False
        else:
            print("Please enter a valid option.")

    thisSim = simob.Simulation(thisID, cycleTotal, breakpoint, lifespan, breakTime, autoEvaluation)
    return(thisSim)

def buildSubjectPool():
    def questionLogic():
        cont = True
        while cont:
            try:
                userType = int(input("How many to include: "))
                if userType < 0:
                    print("Please enter an integer value of 0 or higher.")
                else:
                    cont = False
                    return(userType)
            except:
                print("Please enter an integer value.")

    print("The simulation requires a diversity of user types. Please designature how many of each user type to enter.")
    print("How many casual users should be included in this simulation? A casual user will check less of their timeline,\n"
          "but they will more likely share content they see. They will very rarely create new content.")
    casuals = questionLogic()

    print("How many habitual users should be included in this simulation? A habitual user will check more of their timeline,\n"
        "but they will not share content as often as casual users. They are more likely to create new content.")
    habituals = questionLogic()

    print("How many investigative users should be included in this simulation? An investigative user will check  far more\n"
        "of their timeline, but they will share far less content. They are far more likely to create new content. They will\n"
        "also follow more users than either casual users or habital users.")
    investigatives = questionLogic()

    print("How many performers should be included in this simulation? A performer will check far less of their timeline\n"
        "be less likely to share content, be less likely to follow other users but are the most likely to create new content.")
    performers = questionLogic()

    return(casuals, habituals, investigatives, performers)

def buildDisinfoScheme(thisSim):
    def cycleBlurb():
        print("Disinfo agents will behave as compromised accounts. This means the account will produce disinfo\n"
              "regardless of whether the user of the account is active or awake.\n"
              "How many cycles should there be between execution of the scheme? (recommended: 15)\n")
        cont = True
        while cont:
            try:
                cycleTotal = int(input("Enter the desired number of cycles: "))
                if cycleTotal <= 0:
                    print("Please enter an integer value greater than 0")
                else:
                    return(cycleTotal)
            except:
                print("Please enter an integer value.")
    def subMatterBlurb(thisSim):
        print("The subject matter of disinformation affects the likelihood of whether other users will share it.\n"
              "Subject matter can either be a fixed value, correspond to the agent's own interests, or be totally random.")
        while True:
            selection = input("""Please enter one of either "fixed", "interests" or "random": """)
            if selection == "fixed":
                thisSim.disinfoType = "fixed"
                print("For simplicity's sake the subject matter is for all content is abstracted as names of animals.")
                input("The following is a list of the animal names used as subject matter abstracts (press enter to continue)")
                for i, a in enumerate(simob.Simulation.submatter):
                    print(a, end=", ")
                    if i % 5 == 4:
                        print("\n")
                print("Note: If you do not use one of these names as subject matter it will count but won't be found in any subject interests!")
                subjectSelection = input("Enter the name of an animal to use as disinfo subject matter: ")
                thisSim.disinfoSubjectMatter = subjectSelection
                return
            elif selection == "interests":
                thisSim.disinfoType = "interests"
                return
            elif selection == "random":
                thisSim.disinfoType = "random"
                return
            else:
                print("Invalid selection!")


    print("The simulation requires a disinformation scheme to create false information for the users to share.\n"
          "This can be done in one of two ways, either a pool of dedicated users can be compromised\n"
          "to spread disinformation or an item of disinformation can be added to a user's\n"
          "timeline randomly.")
    cont = True
    while cont:
        selection = input("""Please enter either "pool" or "random" to determine the type of disinformation scheme:""")

        if selection.lower() == "random":
            thisSim.disinfoScheme = "random"
            disinfoCounter = cycleBlurb()
            thisSim.disinfoTimer = disinfoCounter
            thisSim.disinfoCount = disinfoCounter
            print("How many users should be randomly selected each time to produce disinformation? ")
            cont = True
            while cont:
                try:
                    totalUsers = int(input("Enter the desired number of users: "))
                    if totalUsers <= 0:
                        print("Please enter an integer value greater than 0")
                    else:
                        thisSim.disinfoRandomCount = totalUsers
                        cont = False
                except:
                    print("Please enter an integer value.")

            subMatterBlurb(thisSim)

            # cont = False



        elif selection.lower() == "pool":
            thisSim.disinfoScheme = "pool"
            disinfoCounter = cycleBlurb()
            thisSim.disinfoTimer = disinfoCounter
            thisSim.disinfoCount = disinfoCounter
            subjectTotal = thisSim.nodeframe[['Id', 'Label', 'Iteration']]
            subjectTotal = subjectTotal.loc[subjectTotal['Iteration'] == 0]
            print("The following is a list of all the subjects created for this simulation with their ID numbers.")
            print("""(Press enter to continue)""")
            print(subjectTotal)
            cont2 = True
            print("Any number of subjects can be added to the pool, simply enter their ID number.\n"
                  "Multiple entries of a single user will cause them to create disinfo for each entry.\n"
                  "To remove a subject from the pool enter their ID number with a hyphen (i.e. -25)\n"
                  "Once you have added all the users you would like simply press enter.")
            while cont2:
                print("Disinfo pool so far: ")
                for i in thisSim.disinfoAgents:
                    print(i.ID,": ",i.getName())
                try:
                    agent = input("who should be added to the pool?: ")
                    agent = int(agent)
                except:
                    if agent != "":
                        print("Invalid input! Please enter an integer, or press enter to stop filling the pool.")
                    else:
                        print("Finishing disinfo scheme construction...")
                        pass
                if isinstance(agent, int):
                    if agent < 0:
                        agent = agent * -1
                        for i in thisSim.disinfoAgents:
                            if i.ID == agent:
                                thisSim.disinfoAgents = [q for q in thisSim.disinfoAgents if q != i]
                    else:
                        for i in thisSim.subjects:
                            if i.ID == agent:
                                thisSim.disinfoAgents.append(i)
                elif agent == "":
                    cont2 = False
            subMatterBlurb(thisSim)
            cont = False
        else:
            print("Please enter one of the two valid options.")
    print("Disinfo scheme is complete! Simulation ready for execution. Reminder that the disinfo scheme can\n"
          "be rebuilt from the configuration option on the main menu.")


def saveLoad(thisSim = "none"):
    cont = True

    while cont:
        print("The following sim data is available:")
        file = open("simdata.txt", "r+")
        for line in file:
            print(line)
        file.close()

        print("""What would you like to do?:

            a: Save
            b: Load
            c: Return

            Enter a decision: """, end="")
        choice = input()
        choice = choice.lower()
        if choice == 'a':
            if thisSim == "none":
                print("No sim data available to save! Build a simulation first")
            else:
                userSaveData = input("Enter a name for the data or name one to overwrite: ")

                f = open("simdata.txt", "r")
                read = f.readlines()
                f.close()
                newfile = """"""
                for i in read:
                    if userSaveData in i:
                        pass
                    else:
                        newfile += i
                n = open("simdata.txt", 'w')
                one = str(newfile)
                n.write(one)
                n.close()

                file = open("simdata.txt", "a")
                file.write(userSaveData + "\n")
                file.close()

                savProper = open(userSaveData + ".dat", "wb")
                pickle.dump(thisSim, savProper)
                savProper.close()

        elif choice == 'b':
            try:
                userLoadData = input("Enter a save file to load: ")
                loadProper = open(userLoadData + ".dat", "rb")
                print("loading ",userLoadData + ".dat")
                thisSim = pickle.load(loadProper)
                print("This simulation has the following configuration: ")
                print("Simulation ID: ", thisSim.ID)
                print("Simulation length: ", thisSim.totalCycles)
                print("Remaining number of cycles: ", thisSim.remainingCycles)
                print("Breakpoint percentage: ", thisSim.breakpoint)
                print("Cycles between breakpoint re-evaluation: ", thisSim.breakTimeBetween)
                print("Auto-evaluation: ", thisSim.autoEvaluate)
                loadProper.close()
            except:
                print("LOAD ERROR. ", userLoadData, " not found!")

        elif choice == 'c':
            print("Returning to main menu...")
            return(thisSim)
        else:
            print("Invalid input...")

def configuration(thisSim):
    print("""From here the simulation can have various principle values altered or mitigations can be
    put in place to help control the spread of disinformation. There are also options to clear all current
    user timelines and create a new disinfo scheme without altering the simulation progression. (NOTE: It is advised
    you save your current simulation data before implementing any of these options!)
     
     Please select one of the following options:
     1. Configure simulation variables
     2. Implement mitigations
     3. Reset timelines
     4. Implement new disinfo scheme
     5. Return to main menu""")
    cont = True
    while cont:
        c = input("Selection: ")

        if c == "1":
            print("This simulation has the following configuration: ")
            print("Simulation ID: ",thisSim.ID)
            print("Simulation length: ", thisSim.totalCycles)
            print("Remaining number of cycles: ", thisSim.remainingCycles)
            print("Breakpoint percentage: ", thisSim.breakpoint)
            print("Cycles between breakpoint re-evaluation: ", thisSim.breakTimeBetween)
            print("Auto-evaluation: ", thisSim.autoEvaluate)

            print("To change a variable enter the desired value. Make sure to follow the directions\n"
                  "so as not to enter invalid data types. If you don't want to change the value,\n"
                  "simply press enter.")
            choice = input("What should the Simulation ID be changed to? (any string accepted): ")
            if choice == "":
                pass
            else:
                thisSim.ID = choice

            cont = True
            while cont:
                try:
                    choice = input("How many total cycles should the sim have?: ")
                    choice = int(choice)
                except:
                    if choice != "":
                        print("Invalid input! Please enter an integer or press enter to skip.")
                    else:
                        pass
                if isinstance(choice, int):
                    if choice <= 0:
                        print("Please enter an integer value greater than 0")
                    else:
                        cont = False
                        thisSim.totalCycles = choice
                elif choice == "":
                    cont = False

            cont = True
            while cont:
                try:
                    choice = input("How many remaining cycles should the sim have?: ")
                    choice = int(choice)
                except:
                    if choice != "":
                        print("Invalid input! Please enter an integer or press enter to skip.")
                    else:
                        pass
                if isinstance(choice, int):
                    if choice <= 0:
                        print("Please enter an integer value greater than 0")
                    elif choice > thisSim.totalCycles:
                        print("Please enter a value greater than the total number of cycles assigned to this simulation.")
                    else:
                        cont = False
                        thisSim.remainingCycles = choice
                elif choice == "":
                    if thisSim.remainingCycles > thisSim.totalCycles:
                        print("Newly assigned number of total cycles is now less than remaining number of cycles.\n"
                              "A new value must be assigned for remaining number of cycles.")
                    else:
                        cont = False


            cont = True
            while cont:
                try:
                    choice = input("What should the breakpoint percentage be?: ")
                    choice = int(choice)
                except:
                    if choice != "":
                        print("Invalid input! Please enter an integer or press enter to skip.")
                    else:
                        pass
                if isinstance(choice, int):
                    if choice <= 0:
                        print("Please enter an integer value greater than 0")
                    elif choice >= 100:
                        print("Please enter an integer value less than 100")
                    else:
                        cont = False
                        thisSim.breakpoint = choice
                elif choice == "":
                    cont = False

            cont = True
            while cont:
                try:
                    choice = input("How many cycles between re-evaluation should the simulation have?: ")
                    choice = int(choice)
                except:
                    if choice != "":
                        print("Invalid input! Please enter an integer or press enter to skip.")
                    else:
                        pass
                if isinstance(choice, int):
                    if choice <= 0:
                        print("Please enter an integer value greater than 0")
                    else:
                        cont = False
                        thisSim.breakTimeBetween = choice
                elif choice == "":
                    cont = False


            cont = True
            while cont:
                choice = input("automatically re-evaluate after breakpoint reached? (y/n): ")
                if "y" in choice.lower():
                    thisSim.autoEvaluate = True
                    cont = False
                elif "n" in choice.lower():
                    thisSim.autoEvaluate = False
                    thisSim.evaluationFlag = False
                    cont = False
                else:
                    print("Please enter a valid option.")

            print("Simulation successfully reconfigured! The new configuration is as follows: ")
            print("Simulation ID: ", thisSim.ID)
            print("Simulation length: ", thisSim.totalCycles)
            print("Remaining number of cycles: ", thisSim.remainingCycles)
            print("Breakpoint percentage: ", thisSim.breakpoint)
            print("Cycles between breakpoint re-evaluation: ", thisSim.breakTimeBetween)
            print("Auto-evaluation: ", thisSim.autoEvaluate)


        elif c == "2":
            print("Mitigations can be placed on individual users which will effectively serve as taking them out of the simulation.\n"
                  "Once a user has been flagged for mitigation a timer will countdown for each cycle of the simulation. Once the\n"
                  "the countdown completes the flag will be lifted. You can select which users will have a mitigation applied and\n"
                  "how long the mitigation will last for. ")
            subjectTotal = thisSim.nodeframe[['Id', 'Label']]
            print("The following is a list of all the subjects created for this simulation with their ID numbers.")
            print("""(Press enter to continue)""")
            subjectTotal = thisSim.nodeframe[['Id', 'Label', 'Iteration']]
            subjectTotal = subjectTotal.loc[subjectTotal['Iteration'] == 0]


            print(subjectTotal)
            print("Any number of subjects can have mitigations applied. A mitigation countdown must also.\n"
                  "be specified for each subject that receives a mitigation."
                  "To remove mitigations from a subject enter their ID number with a hyphen (i.e. -25)\n"
                  "Once you have applied all the mitigations you would like simply press enter.")
            while cont:
                print("Mitigated users so far: ")
                for i in thisSim.subjects:
                    if i.mitigationFlag == True:
                        print(i.ID, ": ", i.getName())

                try:
                    subject = input("who should have a mitigation placed upon them? (enter their ID number): ")
                    subject = int(subject)
                except:
                    if subject != "":
                        print("Invalid input! Please enter an ID number or press enter to stop placing mitigations.")
                    else:
                        print("Finishing mitigation applications...")
                        cont = False
                        pass
                if isinstance(subject, int) and not "":
                    if subject < 0:
                        subject = subject * -1
                        for i in thisSim.subjects:
                            if i.ID == subject:
                                i.mitigationFlag = False
                    elif subject > 0:
                        for i in thisSim.subjects:
                            if i.ID == subject:
                                i.mitigationFlag = True
                                cont2 = True
                                while cont2:
                                    mitigationCount = input("How many cycles until the mitigation is lifted?: ")
                                    mitigationCount = int(mitigationCount)
                                    if isinstance(mitigationCount, int):
                                        if mitigationCount <= 0:
                                            print("Please enter an integer value greater than 0")
                                        else:
                                            cont2 = False
                                            i.mitigationCount = mitigationCount
                                    else:
                                        print("Please enter an integer value.")
                    elif subject == "":
                        cont = False

        elif c == "3":
            for i in thisSim.subjects:
                i.timeline.clear()
            thisSim.contentlist.clear()
            thisSim.initialContent()
            thisSim.genTimelines()
            print("Timelines have been reset! Returning to main menu.")
            cont = False
        elif c == "4":
            buildDisinfoScheme(thisSim)
            cont = False
        elif c == "5":
            cont = False
        else:
            print("Invalid option. Make sure you enter the number of your selection with no spaces!")

def exportData(thisSim):
    if thisSim.remainingCycles == thisSim.totalCycles:
        print("Remaining cycle value for this simulation has been detected as equal to total number cycles.\n"
              "This indicates the simulation has not yet been run!")
        cont = True
        while cont:
            choice = input("Do you need the initial data to be exported again? (y/n): ")
            if "y" in choice.lower():
                initialNodeData = thisSim.nodeframe[['Id', 'Label', 'Gender', 'User Type', 'Active', 'Awake', 'Interests']]
                initialEdgeData = thisSim.edgeframe
                initialNodeData.to_csv('initialNodeData.csv', index=False)
                initialEdgeData.to_csv('initialEdgeData.csv', index=False)
                cont = False
            elif "n" in choice.lower():
                print("Returning to main menu...")
                cont = False
            else:
                print("Please enter a valid option.")
    elif thisSim.remainingCycles > thisSim.totalCycles:
        print("Remaining cycle value for this simulation reads as greater than the total number of cycles. \n"
              "This simulation has likely been misconfigured. Please see the configuration options from the \n"
              "configuration menu to rectify this!")
        print("Returning to main menu...")
    else:
        print("""There are two types of data to export from any given simulation. A total compromise count that
        will detail the total number of compromised accounts for each given iteration of the simulation. The other
        data to export will be the entire topology for a designated iteration, including details about each node
        within the topology at the time of the iteration. It is recommended that you use the compromise data to
        search for specific points within the simulation that from which to select an iteration to analyze. 
        For example if a breakpoint was hit and you were returned to the main menu, the last-most iteration
        would be the one to select for analysis. Any iteration can be exported for analysis however.
        
        Which data type would you like to export?
        1. compromise data
        2. specific iteration""")
        cont = True
        while cont:

            c = input("Selection: ")

            if c == "1":
                compcheck = thisSim.nodeframe[['Compromise Count', 'Iteration']]
                compcheck = compcheck.drop_duplicates()
                compcheck.to_csv('compcheck.csv', index=False)
                print("Data has been exported to compcheck.csv, please look for this in the parent directory\n"
                      "and analyse with excel!")
                cont = False
            elif c == "2":
                print("which iteration from the simulation would you like to extract data for?")
                cont2 = True
                while cont2:
                    try:
                        d = int(input("Enter an iteration number: "))
                        if d > thisSim.iteration:
                            print("Designated iteration value exceeds total number of documented iterations!\n"
                                  "Please enter an appropriate value.")
                        elif d < 0:
                            print("Designated iteration value is less than zero!\n"
                                  "Please enter an appropriate value.")
                        elif d > 0 and d < thisSim.iteration:
                            cont2 = False
                    except:
                        print("Please enter a valid iteration value!")

                nodeframe = thisSim.nodeframe.loc[thisSim.nodeframe['Iteration'] == d]
                edgeframe = thisSim.edgeframe
                nodeframe.to_csv('nodes.csv', index=False)
                edgeframe.to_csv('edges.csv', index=False)
                print("Data has been exported to nodes.csv and edges.csv, please look for this in the parent directory\n"
                      "and import them into the gephi data laboratory!")
                cont = False
            else:
                print("Please enter a valid selection from the options presented!")
        input("Press enter to continue... ")




    print("")
