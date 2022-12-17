# Main Alberta Health(AH) Management console program.

import ah

# Database Filenames
d_files = {"doctor": "files/doctors.txt", 
             "facility": "files/facilities.txt",
             "lab": "files/laboratories.txt",
             "patient": "files/patients.txt"}

if __name__ == "__main__":
    ah_Manager = ah.Management(d_files)
    ah_Manager.displayMenu()
