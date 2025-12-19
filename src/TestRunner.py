from Deterministic import Deterministic
import pandas as pd

# Mapping of valid yes or no responses (in lower-case) to their corresponding boolean values
validYesOrNoResponses = {
    "Yes": True,
    "yes": True,
    "y": True,
    "No": True,
    "no": False,
    "n": False
}

# Valid responses for the specified tests
validTestSuiteResponses = {
    "1": True,
    "full": True,
    "0": False,
    "single": False, 
}

# Valid Mode of Operation responses
vaildModeResponses = {
    "ECB": True,
    "ecb": True,
    "CBC": False,
    "cbc": False
}

# Class to run command line interface that runs the deterministic tests
class TestRunner:
    def __init__(self) -> None:
        self.isSessionOn = False
    
        # Running runner class
        self.run()
    
    # Runs command line interface
    def run(self):
        print("Welcome to Isaiah Sinclair's CIS*4520 Term Project")
        
        # Enter a file input and read the file before starting the session
        # Only one file per session
        self.tester = self.getTester()
        
        self.isSessionOn = True
        yesOrNoPrompt = "Please enter your response as a yes/no (y/n) answer:"
        
        while self.isSessionOn:
            # Ask the user if they want to enter in a single input, or run the full test suite
            isFullTestSuite = self.getInput("Do you want to run a single test or the full test suite?", 
                                            "Please enter 'single' (or 0) if you want to run a single test, and 'full' (or 1) if you want to run the full test suite:", validTestSuiteResponses)
            
            # Run full test suite, save to a file
            if isFullTestSuite:
                print("***FULL TEST SUITE***")
                print("This runs the ECB and CBC modes of operation against different padding lengths (0-15 bytes) and outputs in a CSV file.")
                cpaAttackPos = self.getCPAAttackPos()
                results = self.tester.runTestSuite(cpaAttackPos)
                print("Test suite finished.")
                
                # Writes the results to a specified CSV file
                self.exportResultsToFile(results)
                print("Exported to file.")
                
            # Run single test (needs some user prompts to specify the specific test to run)
            else:
                print("***SINGLE TEST***")
                isECB = self.getInput("What mode of operation do you want to encrypt/decrypt your data with?", "Enter a mode of operation ('ECB' or 'CBC'):",
                                        vaildModeResponses)
                paddingLength = input("Enter a padding length: ")
                cpaAttackPos = self.getCPAAttackPos()
                
                result = self.tester.runTest(cpaAttackPos, int(paddingLength), isECB)
                print(result)
                
                if isECB:
                    modeStr = "ECB"
                else:
                    modeStr = "CBC" 
                
                print(f"Single test with the {modeStr} and a data length of {int(paddingLength) + 1} bytes finished.")
                print("See plaintext and ciphertext (represented as hex values) stored in plaintext.txt and ciphertext.txt, respectively.")
            
            # Ask user if they want to end the session
            self.isSessionOn = self.getInput("Do you want to run more tests against this data set?", yesOrNoPrompt, validYesOrNoResponses)
            
    def getTester(self):
        tester = None
        
        while tester == None:
            try:
                fileName = input("Enter a CSV file name: ")
                df = self.readFile(f"data/{fileName}")
                
                # Creating deterministic tester
                # Creating tester
                tester = Deterministic(df['Outcome'].astype(str))
                
                print(f"'{fileName}' read correctly. Tester created.")
            except FileNotFoundError:
                print("An exception occurred. Please make sure you entered the right file name/path.")
            
        return tester
    
    # Obtains the specific encrypted '1' (respresentation of a diabetic) that the person wants to use for the CPA attack
    # This is parameter is to help demonstrate how different ciphertexts given to an attacker provide different levels of effectiveness for querying data
    def getCPAAttackPos(self):
        pos = -1
        
        # Needs to get a position within the range of 1 to observedDiabetics (inclusive)
        while pos < 1:
            try:
                print(f"There are {self.tester.data.observedDiabetics} diabetics in this dataset. For experimental purposes, what diabetic ('1') do you want the corresponding ciphertext for?")
                pos = int(input(f"Please enter a number from 1-{self.tester.data.observedDiabetics}: "))
                
                if pos > self.tester.data.observedDiabetics or pos < 1:
                    pos = None
                    raise RuntimeError("Entered an invalid number")
            except RuntimeError:
                print("You entered an invalid number.")
            except Exception:
                print("You entered invalid value.")
                
        return pos
        
        
    # Takes a file name (needs full file path), and reads it and passes it into a deterministic tester structure
    # File path should be relative from the directory you ran the python TestRunner.py command
    def readFile(self, filePath):
        fp = open(filePath, 'r')
        df = pd.read_csv(fp)
        fp.close()
        
        return df
    
    # Writes results from the dataframe to a file
    def exportResultsToFile(self, df):
        writtenToFile = False
        
        while not writtenToFile:
            try:
                fileName = input("What file do you want to output the results too. Please enter a CSV file extension: ")
                df.to_csv(f"results/{fileName}", mode="w")
                print("Output to the results folder.")
                writtenToFile = True
            except:
                print("An error occurred while writing to the file.")
        
    # Gets user input for yes or no questions, validates
    def getInput(self, prompt, promptInstructions, mappedResponses):
        mappedAnswer = None
        
        # Loops until a valid response is mapped the mappedResponse variable
        while mappedAnswer == None:
            
            response = input(f"{prompt}\n{promptInstructions} ")
            
            # Check to see if response correspondings to mapping
            # If it does, assign an appropriate mapping
            # If it does not, re-prompt the user to enter again
            try:
                mappedAnswer = mappedResponses[response]
            except:
                print("Invalid entry.")
                
        return mappedAnswer
                    
        
if __name__ == "__main__":
    runner = TestRunner()