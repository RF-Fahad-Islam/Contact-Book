import datetime
import json
import os
import pickle

class ContactBook:
    """
    A ContactBook class which saved and managed the contact inforamation
    by name and phonenumber
    """

    def __init__(self, contactBookDict):
        self.dataSavePath = "contacts.json"
        self.contactBookDict = self.generateSkeleton()
        self.contactsDict = self.getContacts()
        self.retrieveContacts()
        self.assignKeysContacts()
        self.counter = max(self.keys)+1

    def assignNames(self):
        self.names = [key.lower() for key in self.contactsDict.keys()]

    def assignKeysContacts(self):
         self.keys = [int(key) for key in self.contactsDict.keys()]
    
    def generateSkeleton(self):
        """
        Generate the skeleton of the contact book dictionary if contactBookDict
        is Undefined or None
        """
        skeleton = {"name":"####","last-modified": f"{datetime.datetime.now()}","contacts": [{'1':"{}"}]}
        return skeleton

    def showContacts(self):
        """
        Show the contacts name and number to console
        """
        for dicts in self.contactBookDict.get("contacts"):
            for key, contacts in dicts.items():
                for name, number in contacts.items():
                    print(f"{key}. {name} => {number}")

    def getContacts(self):
        """
        Get the contacts dictionary

        Returns:
            list: self.contactBookDict.get("contacts")
            dict: self.contactBookDict.get("contacts")[0]
        """
        return self.contactBookDict.get("contacts")[0]

    def addContacts(self, contactBookName,name, number):
        """
        Add contacts to contactBookDict with serial number using name and Phone Number
        """
        self.contactBookDict["name"] = contactBookName
        self.contactBookDict["last updated"] = str(datetime.datetime.now())
        newContacts = {
            name: number
        }
        self.assignNames()
        if name.lower() not in self.names:
            self.contactsDict[self.counter] = newContacts
            self.counter += 1
            print(f"Successfully assign :\nName: {name}]\nNumber: {number}")
            self.saveContacts()
        else:
            print(f"The name already exists in the saved data : {name}")

    def saveContacts(self):
        """
        Save the contact Dictionary in JSON foramt in the "contacts.json" file
        """
        with open(self.dataSavePath, "w") as f:
            json.dump(self.contactBookDict, f, indent=3)
        with open("backup.pkl", "wb") as f:
            pickle.dump(self.contactBookDict, f)
            
    def retrieveContacts(self):
        """
        Read the saved JSON data from "contacts.json" and convert the JSON to
        Python dictionary object.
        """
        if os.path.exists(self.dataSavePath):
            with open(self.dataSavePath) as f:
                self.contactBookDict = json.load(f)
        else:
            User().getInformatonForNewContact()

    def updateContact(self):
        self.contactBookDict["last updated"] = str(datetime.datetime.now())
        print("Overview : ")
        self.showContacts()
        self.assignNames()
        givenName = input("Enter the name for updating : ")
        for key, contact in self.contactsDict.items():
            for name, number in contact.items():
                if name.lower() == givenName.lower():
                    typeof = input("Choose the value for updating\n1.name\n2.number\n3.both\nType the text or index : ")
                    if typeof == "name" or typeof == "1":
                        updateDict = {input("Enter the new name : "):number}
                    elif typeof == "number" or typeof == "2":
                        updateDict = {name:input("Enter the update number => ")}
                    elif typeof == "both" or typeof == "3":
                        updateDict = {input("Enter the new name : "):input("Enter the update number => ")}
                        
                    self.contactsDict.update(updateDict)
                    self.saveContacts()
                    print(f"Successfully updated the number of {givenName}")
                else:
                    print(f"The {givenName} is not present in the saved data.")
                
    def removeContact(self, key):
        """
        Remove a contact information from the dictionary

        Args:
            name (str): Takes the name from the user for removing

        Returns:
            str: The deleted contactinfo
        """
        self.assignKeysContacts()
        deleted = self.contactsDict.pop(key)
        self.saveContacts()
        return deleted

    def removeAll(self):
        self.contactsDict = {}
        self.saveContacts()

    def searchContact(self, givenname):
        for key, contact in self.contactsDict.items():
            for name, number in contact.keys():
                if name.lower() == givenname.lower():
                    print(f"\t\t\tSearch Results : ")
                    print(f"{name}'s number => {number}")


class User:
    def takeCommand(self):
        """
        Take command from the user

        Returns:
            str: command take from the user
        """
        command = input("Enter the command : ")
        return command

    def getInformatonForNewContact(self):
        """
        Take the new contact name and phone number
        """
        ContactBookName = input("Enter the name of contact book : ")
        print("Enter \"q\" to stop")
        while True:
            newContactName = input("Enter the name => ")
            if newContactName == "q":
                break
            newContactNumber = input(f"Enter the number of \"{newContactName}\" => ")
            ContactBook().addContacts(ContactBookName, newContactName, newContactNumber)

    def removeContactKey(self):
        """
        Take the key of contact to delete

        Returns:
            str : User input

        """
        key = input("Enter the no. for delete contact : ")
        return key

    def askname(self):
        """
        Take the name from the user

        Returns:
            str: The given name to use it in the contactBook
        """
        name = input("Enter the name => ")
        return name


if __name__ == "__main__":
    contactBookDict = {
        "name": "My-Contact",
        "last updated": "01/12/2020",
        "contacts":
            [
                {
                    "1": {
                        "Fahad": "01905600574"
                    },
                    "2": {
                        "Harry": "019176720518"
                    }
                }
            ] 
        }
    newContact = ContactBook(contactBookDict)
    user = User()
    while True:
        command = user.takeCommand()
        if command == "1":
            newContact.showContacts()
        elif command == "2":
            user.getInformatonForNewContact()
        elif command == "3":
            newContact.showContacts()
            key = user.removeContactKey()
            confirm = input(
                "Do you really want the delete the contact (y/n) : ")
            if confirm == "y":
                a = newContact.removeContact(key)
                print(f"Successfully deleted {a.items()}")   
        elif command == "4":
            newContact.updateContact()
                
        elif command == "6":
            confirm = input(
                "Do you really want the delete the contact (y/n) : ")
            if confirm == "y":
                newContact.removeAll()
                print(f"Successfully deleted All contacts!")

        elif command == "q":
            exit()
