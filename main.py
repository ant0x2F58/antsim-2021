import pandas as pd
import simob
import random
import simfun

#These are options for the Pandas module that were initially used to display the visual output
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_rows', None)



print("Welcome to AntSim! A social networking and disinformation simulator.\n")
simExist = False
while True:
    if simExist:
        print("Current sim loaded:")
        thisSim.displaySim()
    print("""
Welcome to the main menu. Please select an option:
1. Build Sim
2. Load/Save Sim""")
    if simExist:
        print("""3. Run Sim
4. Configure Sim
5. Export Data""")
    print("""6. Quit""")
    c = input("Selection: ")

    if c == "1":
        thisSim = simfun.buildSim()
        thisSim.initialContent()
        subjectTuple = simfun.buildSubjectPool()
        thisSim.genSubjects(subjectTuple[0],subjectTuple[1],subjectTuple[2],subjectTuple[3])
        thisSim.genTimelines()
        simExist = True
        thisSim.networking()
        thisSim.initialDataGet()
        initialNodeData = thisSim.nodeframe[['Id', 'Label', 'Gender', 'User Type', 'Active', 'Awake', 'Interests']]
        initialEdgeData = thisSim.edgeframe
        initialNodeData.to_csv('initialNodeData.csv', index=False)
        initialEdgeData.to_csv('initialEdgeData.csv', index=False)
        print("The social network has been computed and the data has been exported for viewing in gephi.")
        print("Please search for the files initialNodeData.csv and initialEdgeData.csv in the parent directory\n"
              "for this software and load them into the datalab in gephi to visualize the network.")
        input("Once you have the data loaded and are satisfied with the visualization press enter to continue.")
        simfun.buildDisinfoScheme(thisSim)
        print("Simulation successfully built and ready to run! Returning to main menu.")
    elif c == "2":
        if simExist:
            thisSim = simfun.saveLoad(thisSim)
        else:
            try:
                thisSim = simfun.saveLoad()
                print("This simulation has the following configuration: ")
                print("Simulation ID: ", thisSim.ID)
                print("Simulation length: ", thisSim.totalCycles)
                print("Remaining number of cycles: ", thisSim.remainingCycles)
                print("Breakpoint percentage: ", thisSim.breakpoint)
                print("Cycles between breakpoint re-evaluation: ", thisSim.breakTimeBetween)
                print("Auto-evaluation: ", thisSim.autoEvaluate)
                simExist = True

            except:
                print("No simulation data loaded! Make sure to build one in the main menu!")

    elif c == "3" and simExist:
        thisSim.simActual()
    elif c == "4" and simExist:
        simfun.configuration(thisSim)
    elif c == "5" and simExist:
        simfun.exportData(thisSim)
    elif c == "6":
        print("Thank you for using AntSim! Have a wonderful day :)")
        break
    else:
        print("Invalid option. Make sure you enter the number of your selection with no spaces!")





