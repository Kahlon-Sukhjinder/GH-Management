# Python module containing facilities for Alberta Health Management System

from tabulate import tabulate

# Symbolic constants
docFormatInFile = 'id_name_specilist_timing_qualification_roomNb\n'
labFormatInFile = 'Lab_Cost\n'
patFormatInFile = 'id_Name_Disease_Gender_Age\n'
filenames = {"doctor": "files/doctors.txt", 
             "facility": "files/facilities.txt",
             "lab": "files/laboratories.txt",
             "patient": "files/patients.txt"}

class Doctor:
    """ A class for representing and managing medical doctors information """
    __ID:int
    __name:str
    __spec:str
    __wTime:str
    __qual:str
    __roomNo:int

    def __init__(self, ID:int, name:str, spec:str, wTime:str, qual:str, roomNo:int):
        assert (ID > 0 and roomNo > 0)
        self.__ID = ID
        self.__name = name
        self.__spec = spec
        self.__wTime = wTime
        self.__qual = qual
        self.__roomNo = roomNo

    def __str__(self):
        return self.formatDrInfo()

    def formatDrInfo(self):
        return f"{self.__ID}_{self.__name}_{self.__spec}_{self.__wTime}_{self.__qual}_{self.__roomNo}"

    @classmethod
    def enterDrInfo(cls):
        ID = int(input("Enter the doctor’s ID: "))
        name = input("\nEnter the doctor’s name: ")
        spec = input("\nEnter the doctor’s speciality: ")
        wTime = input("\nEnter the doctor’s timing (e.g., 7am-10pm): ")
        qual = input("\nEnter the doctor’s qualification: ")
        roomNo = int(input("\nEnter the doctor’s room number: "))
        return cls(ID, name, spec, wTime, qual, roomNo)

    @classmethod
    def readDoctorFile(cls, filename:str):
        docFile = open(filename, "r")
        doctors = []
        # Parse doc file according to 'id_name_specilist_timing_qualification_roomNb'
        assert (docFile.readline() == docFormatInFile)
        for doc in docFile:
            attributes = doc.strip().split("_")
            assert len(attributes) == 6
            doctors.append(cls(int(attributes[0]), attributes[1], attributes[2], attributes[3], 
                            attributes[4], int(attributes[5])))

        docFile.close()
        return doctors

    @staticmethod
    def searchDoctorById(ID:int, docList:list):
        """ Returns a Doctor object from docList with matching ID. If there's no match, then return
            None . """
        for doc in docList:
            if (doc.getID() == ID):
                return doc
        return None

    def searchDoctorByName(name:str, docList:list):
        """ Returns a Doctor object from docList with matching name. If there's no match, then return
            None . """
        for doc in docList:
            if (doc.getName().lower() == name.lower()):
                return doc
        return None

    def displayDoctorInfo(self):
        print(tabulate([self.formatDrInfo().split("_")], 
              ["ID", "Name", "Specialization", "Timing", "Qualification", "Room No."],
              tablefmt="grid"))

    @staticmethod
    def displayDoctorsList(docList:list):
        table = []
        for doc in docList:
            table.append(doc.formatDrInfo().split("_"))
        print(tabulate(table, 
                       ["ID", "Name", "Specialization", "Timing", "Qualification", "Room No."],
                       tablefmt="grid"))

    @classmethod
    def editDoctorInfo(cls, ID:int, docList:list):
        """ Edits attributes of Doctor object with matching ID in docList and returns the updated
            Doctor object. Returns None if no match is found. """
        for i in range(len(docList)):
            if (docList[i].getID() == ID):
                name = input("\nEnter new name: ")
                spec = input("\nEnter new speciality: ")
                wTime = input("\nEnter new timing (e.g., 7am-10pm): ")
                qual = input("\nEnter new qualification: ")
                roomNo = int(input("\nEnter new room number: "))
                docList[i] = cls(docList[i].getID(), name, spec, wTime, qual, roomNo)
                return docList[i]

        print("Can't find the doctor with the given ID in the system")
        return None

    def addDrToFile(self, filename:str):
        docFile = open(filename, "a")
        docFile.write(f"{self.formatDrInfo()}\n")
        docFile.close()

    @staticmethod
    def writeListOfDoctorsToFile(docList:list, filename:str):
        docFile = open(filename, "w")
        docFile.write(docFormatInFile)
        for doc in docList:
            docFile.write(f"{doc.formatDrInfo()}\n")
        docFile.close()

    def getID(self):
        return self.__ID
    def getName(self):
        return self.__name
    def getSpec(self):
        return self.__spec
    def getWTime(self):
        return self.__wTime
    def getQual(self):
        return self.__qual
    def roomNo(self):
        return self.__roomNo


class Facility:
    __name:str

    def __init__(self, name:str):
        self.__name = name

    def __str__(self):
        return self.__name

    @classmethod
    def enterFacilityInfo(cls):
        fac_name = input("Enter facility name: ")
        return cls(fac_name)

    def addFacility(self, filename:str):
        facFile = open(filename, "a")
        facFile.write(f"{str(self)}\n")
        facFile.close()

    @classmethod
    def readFacilitiesFile(cls, filename:str):
        facFile = open(filename, "r")
        facList = []
        facFile.readline() #discard first line
        
        for line in facFile:
            facList.append(cls(line.strip()))
        return facList

    @staticmethod
    def displayFacilities(facList:list):
        print("The Hospital Facilities are:\n")
        for fac in facList:
            print(fac)

    @staticmethod
    def writeListOfFacilitiesToFile(facList:list, filename:str):
        facFile = open(filename, "w")
        facFile.write("Hospital Facilities are:\n")
        for fac in facList:
            facFile.write(f"{str(fac)}\n")
        facFile.close()

    def getName(self):
        return self.__name


class Laboratory:
    __name:str
    __cost:float

    def __init__(self, name:str, cost:float):
        assert (cost >= 0)
        self.__name = name
        self.__cost = cost

    def __str__(self):
        return self.formatLabInfo()

    def formatLabInfo(self):
        return f"{self.__name}_{self.__cost:.2f}"

    @classmethod
    def enterLabInfo(cls):
        name = input("Enter Laboratory facility: ")
        cost = float(input("Enter Laboratory cost: "))
        return cls(name, cost)

    @classmethod
    def readLabFile(cls, filename:str):
        labList = []
        labFile = open(filename, "r")
        assert (labFile.readline() == labFormatInFile)
        for line in labFile:
            attribs = line.strip().split("_")
            assert (len(attribs) == 2)
            labList.append(cls(attribs[0], float(attribs[1])))
        labFile.close()
        return labList

    @staticmethod
    def displayLabsList(labList:list):
        table = []
        for lab in labList:
            table.append(lab.formatLabInfo().split("_"))
        print(tabulate(table, ["Lab", "Cost"], tablefmt="grid"))

    def addLabToFile(self, filename:str):
        labFile = open(filename, "a")
        labFile.write(f"{self.formatLabInfo()}\n")
        labFile.close()

    @staticmethod
    def writeListOfLabsToFile(labList:list, filename:str):
        labFile = open(filename, "w")
        labFile.write(labFormatInFile)
        for lab in labList:
            labFile.write(f"{lab.formatLabInfo()}\n")
        labFile.close()
        
    def getName(self):
        return self.__name
    def getCost(self):
        return self.__cost


class Patient:
    __pid:int
    __name:str
    __disease:str
    __gender:str
    __age:int

    def __init__(self, pid, name, disease, gender, age):
        assert (pid >= 0 and age >= 0)
        self.__pid = pid
        self.__name = name
        self.__disease = disease
        self.__gender = disease
        self.__age = age

    def __str__(self):
        return self.formatPatientInfo()

    def formatPatientInfo(self):
        return f"{self.__pid}_{self.__name}_{self.__disease}_{self.__gender}_{self.__age}"

    @classmethod
    def enterPatientInfo(cls):
        pid = int(input("Enter Patient id: "))
        name = input("Enter Patient name: ")
        disease = input("Enter Patient disease: ")
        gender = input("Enter Patient gender: ")
        age = int(input("Enter Patient age: "))
        return cls(pid, name, disease, gender, age)

    @classmethod
    def readPatientFile(cls, filename:str):
        patFile = open(filename, "r")
        patList = []
        assert (patFile.readline() == patFormatInFile)
        for line in patFile:
            attribs = line.strip().split("_")
            assert (len(attribs) == 5)
            patList.append(cls(int(attribs[0]), attribs[1], attribs[2], attribs[3], int(attribs[4])))
        patFile.close()
        return patList

    @staticmethod
    def searchPatientById(pid:int, patList:list):
        for pat in patList:
            if (pat.getPid() == pid):
                return pat
        return None

    def displayPatientInfo(self):
        print(tabulate([self.formatPatientInfo().split("_")], 
              ["ID", "Name", "Disease", "Gender", "Age"],
              tablefmt="grid"))

    @staticmethod
    def displayPatientsList(patList:list):
        table = []
        for pat in patList:
            table.append(pat.formatPatientInfo().split("_"))
        print(tabulate(table, ["ID", "Name", "Disease", "Gender", "Age"], tablefmt="grid"))

    @classmethod
    def editPatientInfo(cls, pid:int, patList:list):
        for i in range(len(patList)):
            if (patList[i].getPid() == pid):
                name = input("Enter new name: ")
                disease = input("Enter new disease: ")
                gender = input("Enter new gender: ")
                age = int(input("Enter new age: "))
                patList[i] = cls(patList[i].getPid(), name, disease, gender, age)
                return patList[i]
        print("Can't find the Patient with given ID in the system")
        return None

    def addPatientToFile(self, filename:str):
        patFile = open(filename, "a")
        patFile.write(f"{self.formatPatientInfo()}\n")
        patFile.close()

    @staticmethod
    def writePatientsListToFile(patList:list, filename:str):
        patFile = open(filename, "w")
        patFile.write(patFormatInFile)
        for pat in patList:
            patFile.write(f"{pat.formatPatientInfo()}\n")
        patFile.close()

    def getPid(self):
        return self.__pid
    def getName(self):
        return self.__name
    def getDisease(self):
        return self.__disease
    def getGender(self):
        return self.__gender
    def getAge(self):
        return self.__age


class Management:
    __lists = {"doctor": [], "facility": [], "lab": [], "patient": []}

    __filenames = {"doctor": [], "facility": [], "lab": [], "patient": []}

    def __init__(self, filenames:dict):
        for key in filenames:
            self.__filenames[key] = filenames[key]
            if (key == "doctor"):
                self.__lists[key] = Doctor.readDoctorFile(filenames[key])
            elif (key == "facility"):
                self.__lists[key] = Facility.readFacilitiesFile(filenames[key])
            elif (key == "lab"):
                self.__lists[key] = Laboratory.readLabFile(filenames[key])
            elif (key == "patient"):
                self.__lists[key] = Patient.readPatientFile(filenames[key])
            else:
                assert (False)

    def displayMenu(self):
        while (True):
            menu = int(input("\nWelcome to Alberta Hospital (AH) Managment system\n"
                             "Select from the following options, or select 0 to stop:\n"
                             "1 -   Doctors\n"
                             "2 -   Facilities\n"
                             "3 -   Laboratories\n"
                             "4 -   Patients\n"
                             "> "))
            if (menu == 1):
                self.docMenu()
            elif (menu == 2):
                self.facMenu()
            elif (menu == 3):
                self.labMenu()
            elif (menu == 4):
                self.patMenu()
            elif (menu == 0):
                break
            else:
                print("Sorry, invalid option selected. Try again...\n")

    def docMenu(self):
        while (True):
            menu = int(input("\nDoctors Menu:\n"
                               "1 - Display Doctors list\n"
                               "2 - Search for doctor by ID\n"
                               "3 - Search for doctor by name\n"
                               "4 - Add doctor\n"
                               "5 - Edit doctor info\n"
                               "6 - Back to the Main Menu\n"
                               "> "))
            print()
            if (menu == 1):
                Doctor.displayDoctorsList(self.__lists["doctor"])
            elif (menu == 2):
                ID = int(input("Enter the doctor id: "))
                doc = Doctor.searchDoctorById(ID, self.__lists["doctor"])
                if (doc == None):
                    print("Can't find the doctor with the given ID in the system")
                else:
                    doc.displayDoctorInfo()
            elif (menu == 3):
                name = input("Enter the doctor name: ")
                doc = Doctor.searchDoctorByName(name, self.__lists["doctor"])
                if (doc == None):
                    print("Can't find the doctor with the given name in the system")
                else:
                    doc.displayDoctorInfo()
            elif (menu == 4):
                new_doc = Doctor.enterDrInfo()
                self.__lists["doctor"].append(new_doc)
                new_doc.addDrToFile(self.__filenames["doctor"])
            elif (menu == 5):
                ID = int(input("Enter the id of the Doctor whose information you want to edit: "))
                Doctor.editDoctorInfo(ID, self.__lists["doctor"])
                Doctor.writeListOfDoctorsToFile(self.__lists["doctor"], self.__filenames["doctor"])
            elif(menu == 6):
                break
            else:
                print("Sorry, invalid option selected. Try again...")

            wait = input("\nPress return to continue...")
            print("Back to the previous menu\n")

    def facMenu(self):
        while (True):
            menu = int(input("\nFacilities Menu:\n"
                               "1 - Display Facilities list\n"
                               "2 - Add facility\n"
                               "3 - Back to the main menu\n"
                               "> "))
            print()
            if (menu == 1):
                Facility.displayFacilities(self.__lists["facility"])
            elif (menu == 2):
                new_fac = Facility.enterFacilityInfo()
                self.__lists["facility"].append(new_fac)
                new_fac.addFacility(self.__filenames["facility"])
            elif (menu == 3):
                break
            else:
                print("Sorry, invalid option selected. Try again...")

            wait = input("\nPress return to continue...")
            print("Back to the previous menu\n")


    def labMenu(self):
        while (True):
            menu = int(input("\nLaboratories Menu:\n"
                               "1 - Display laboratories list\n"
                               "2 - Add laboratory\n"
                               "3 - Back to the main menu\n"
                               "> "))
            print()
            if (menu == 1):
                Laboratory.displayLabsList(self.__lists["lab"])
            elif (menu == 2):
                new_lab = Laboratory.enterLabInfo()
                self.__lists["lab"].append(new_lab)
                new_lab.addLabToFile(self.__filenames["lab"])
            elif (menu == 3):
                break
            else:
                print("Sorry, invalid option selected. Try again...")

            wait = input("\nPress return to continue...")
            print("Back to the previous menu\n")


    def patMenu(self):
        while (True):
            menu = int(input("\nPatients Menu:\n"
                               "1 - Display patients list\n"
                               "2 - Search for patient by ID\n"
                               "3 - Add patient\n"
                               "4 - Edit patient info\n"
                               "5 - Back to the main menu\n"
                               "> "))
            print()
            if (menu == 1):
                Patient.displayPatientsList(self.__lists["patient"])
            elif (menu == 2):
                pid = int(input("Enter the Patient ID: "))
                pat = Patient.searchPatientById(pid, self.__lists["patient"])
                if (pat == None):
                    print("Can't find patient with the given ID in the system")
                else:
                    pat.displayPatientInfo()
            elif (menu == 3):
                new_pat = Patient.enterPatientInfo()
                self.__lists["patient"].append(new_pat)
                new_pat.addPatientToFile(self.__filenames["patient"])
            elif (menu == 4):
                pid = int(input("Enter the Id of patient whose info you want to edit: "))
                Patient.editPatientInfo(pid, self.__lists["patient"])
                Patient.writePatientsListToFile(self.__lists["patient"], self.__filenames["patient"])
            elif (menu == 5):
                break
            else:
                print("Sorry, invalid option selected. Try again...")

            wait = input("\nPress return to continue...")
            print("Back to the previous menu\n")


