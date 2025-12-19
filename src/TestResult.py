class TestResult:
    def __init__(self, padLen, isECB, plaintext, ciphertext) -> None:
        self.diabeticsNotIdentified = []
        self.diabeticsIdentified = []
        self.nonDiabeticsIdentified = []
        self.nonDiabeticsNotIdentified = []
        self.diabeticsNotIdentifiedCount = 0
        self.diabeticsIdentifiedCount = 0
        self.nonDiabeticsIdentifiedCount = 0
        self.nonDiabeticsNotIdentifiedCount = 0
        
        # Time attributes
        self.encTime = 0
        self.decTime = 0
        
        # Test parameters (to retain information about the test parameters themselves for analysis)
        self.padLen = padLen
        
        if isECB:
            self.mode = "ECB"
        else:
            self.mode = "CBC"    
            
        # Data attributes
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        
    # Adds result to the appropriate array, based on its classification
    # Two boolean parameters
    def addComparisonResult(self, index, correct, diabetic):
        if correct:
            # Diabetics should be identified
            if diabetic:
                self.diabeticsIdentified.append(index)
            # Non-diabetics should not be identified
            else:
                self.nonDiabeticsNotIdentified.append(index)
        else:
            if diabetic:
                self.diabeticsNotIdentified.append(index)
            else:
                self.nonDiabeticsIdentified.append(index)
        
    # Calculates results, which include the counts and then the ratios
    def computeResults(self, observedDiabetics, observedNonDiabetics):
        self.computeCounts()
        self.computeCorrectness(observedDiabetics, observedNonDiabetics)
      
    # Takes the 4 Arrays and Computes Their Relative Counts
    def computeCounts(self):        
        self.diabeticsNotIdentifiedCount = len(self.diabeticsNotIdentified)
        self.diabeticsIdentifiedCount = len(self.diabeticsIdentified)
        self.nonDiabeticsIdentifiedCount = len(self.nonDiabeticsIdentified)
        self.nonDiabeticsNotIdentifiedCount = len(self.nonDiabeticsNotIdentified)
        
    # Calculates the ratios of correctness
    def computeCorrectness(self, observedDiabetics, observedNonDiabetics):
        # For diabetics, the classification is correct if it identifies a diabetic as a diabetic
        self.diabeticsCorrectness = self.diabeticsIdentifiedCount / observedDiabetics * 100
        
        # For non-diabetics, the classification is correct if it does not identify a non-diabetic as a diabetic
        self.nonDiabeticsCorrectness = self.nonDiabeticsNotIdentifiedCount / observedNonDiabetics * 100
        
    # Returns a string of all the relevant computed statistics
    def __str__(self) -> str:
        outputString = f"Results for Test (mode: {self.mode}, value length (including padding): {self.padLen + 1}):\n"
        
        # Time Statistics
        outputString += "Time Statistics\n"
        outputString += f"  Encryption Time: {self.encTime:.4f} seconds\n"
        outputString += f"  Decryption Time: {self.decTime:.4f} seconds\n"
        
        # Classification Statistics
        outputString += "Classification Statistics\n"
        outputString += f"  Diabetics Identified: {self.diabeticsIdentifiedCount}\n"
        outputString += f"  Diabetics Not Identified {self.diabeticsNotIdentifiedCount}\n"
        outputString += f"  Non-Diabetics Identified: {self.nonDiabeticsIdentifiedCount}\n"
        outputString += f"  Non-Diabetics Not Identified: {self.nonDiabeticsNotIdentifiedCount}\n"
        
        # Adding Correctness Statistics
        outputString += "Correctness Statistics\n"
        outputString += f"  Diabetics Correctness: {self.diabeticsCorrectness:.2f}%\n"
        outputString += f"  Non-Diabetics Correctness: {self.nonDiabeticsCorrectness:.2f}%\n"
        
        return outputString