from AES import CBC, ECB
from TestData import TestData
from Cryptodome.Random import get_random_bytes
import pandas as pd
from TestResult import TestResult
import time

# Tests to Show how More Deterministic Plaintext Makes it Easier to Query Information From The Ciphertext
class Deterministic:
    def __init__(self, fp) -> None:
        self.data = TestData(fp)
    
    # Compares Actual Data with Predicted Data and Returns the Results
    def comparePredictions(self, result, predictions):
        # Storing Postions Data Points that Relevant Predictions About Them
        
        for i in range(self.data.len):
            # See if Current Row was Predicted as Diabetic, by Attempting to Find it in the Predictions List Passed
            try:
                predictions.index(i)
                predictedDiabetic = True
            except:
                predictedDiabetic = False
                
            isDiabetic = self.data.getRowValue(i) == '1'
                
            # Boolean expression to see if the two values are the same (XNOR -- evaluates to false if both are different)
            correct = not (isDiabetic ^ predictedDiabetic)
                
            result.addComparisonResult(i, correct, isDiabetic)
        
        # Calculates results 
        result.computeResults(self.data.observedDiabetics, self.data.observedNonDiabetics)
        
        return result
    
    # String Searches for the Specified Ciphertext, Returns Locations of Predicted Diabetics Corresponding to Row Numbers in the Original DF
    def getPredictedDiabetics(self, strData, ciphertext, hexLength):
        # Source: https://www.geeksforgeeks.org/python-all-occurrences-of-substring-in-string/
        # Gets Position of All Occurrences of Substring within the Hex Data String
        # Modfies the Resulting Value to an Index that Corresponds to the Original Data Row Numbers 
        diabetics = [(int(i / hexLength)) for i in range(len(strData)) if strData.startswith(ciphertext, i)]
        
        return diabetics
    
    # Runs a single test, with a given padding amount
    # Test CPA with a known '1', meaning that there is a corresponding encrypted '1' and '0'
    def runTest(self, ithDiabetic, paddingLength, isECB):
        singleDataLength = 1 + paddingLength
        
        hexLength = 2 * singleDataLength
        strData = self.data.transformData(paddingLength)
        
        # Finds position of diabetic within the data to conduct the chosen-plaintext attack
        cpaDiabetic = self.data.findDiabetic(ithDiabetic)
        
        sk = get_random_bytes(16)
        
        encodedData = strData.encode('utf-8')
        
        # Testing and Timing Modes
        iv = get_random_bytes(16)
        
        encryptionTime = time.time()
        
        if isECB:
            c = ECB(sk, encodedData, True)
        # Testing CBC Mode
        else:
            c = CBC(sk, iv, encodedData, True)
            
        encryptionTime = time.time() - encryptionTime
        
        # Decrypting the Ciphertext to Get Decryption Time Statistics
        decryptionTime = time.time()
        
        if isECB:
            p = ECB(sk, encodedData, False)
        # Testing CBC Mode
        else:
            p = CBC(sk, iv, encodedData, False)
            
        decryptionTime = time.time() - decryptionTime
                
        # Store Ciphertext Representation of First 1 as a String
        cipherTextHex = str(c.hex())
        plainTextHex = str(p.hex())
        diabeticEncrypted = cipherTextHex[cpaDiabetic * hexLength:cpaDiabetic * hexLength + hexLength]
        
        predictedDiabetics = self.getPredictedDiabetics(cipherTextHex, diabeticEncrypted, hexLength)
        
        # Creating result object, gets modified in self.comparePredictions as it is passed by reference
        result = TestResult(paddingLength, isECB, plainTextHex, cipherTextHex)
        result.encTime = encryptionTime
        result.decTime = decryptionTime
        
        self.comparePredictions(result, predictedDiabetics)
        
        # Write plaintext and hex to a file for reference
        try:
            self.writeHexToFile("results/plaintext.txt", plainTextHex)
            self.writeHexToFile("results/ciphertext.txt", cipherTextHex)
        except:
            print("Could not export plaintext and ciphertext to text files for this test. You're probably not running the program in the project's root directory. Re-runt the program with: python src/testRunner.py")
        
        return result
    
    # Runs a Series of Tests with Different Padding Lengths
    # Records Results in a DataFrame
    def runTestSuite(self, attackPos):
        # We construct a DataFrame first
        deterministicResults = pd.DataFrame()
        
        ecbStates = [True, False]
        
        # Storing Results in Arrays Before Adding them as a Column in the DataFrame
        dataBytes = []
        ecbCorrect1s = []
        ecbCorrect0s = []
        ecbEncryptionTime = []
        ecbDecryptionTime = []
        cbcCorrect1s = []
        cbcCorrect0s = []
        cbcEncryptionTime = []
        cbcDecryptionTime = []
        
        # Test Implemented Modes (first ECB, then CBC)
        for isECB in ecbStates:
            # Padd data from 0-15 bytes (inclusive), and record results
            for padLength in range(16):
                result = self.runTest(attackPos, padLength, isECB)
                
                print(result)
                
                # Append Results to Data Frame
                if isECB:
                    ecbCorrect1s.append(round(result.diabeticsCorrectness / 100, 3))
                    ecbCorrect0s.append(round(result.nonDiabeticsCorrectness / 100, 3))
                    ecbEncryptionTime.append(round(result.encTime, 3))
                    ecbDecryptionTime.append(round(result.decTime, 3))
                else:
                    cbcCorrect1s.append(round(result.diabeticsCorrectness / 100, 3))
                    cbcCorrect0s.append(round(result.nonDiabeticsCorrectness / 100, 3))
                    cbcEncryptionTime.append(round(result.encTime, 3))
                    cbcDecryptionTime.append(round(result.decTime, 3))
                    
        # Creating column for byte length of one diabetic data value ('1' or '0' and the padding)
        # Length of the data is the current padding length + 1 byte (for the actual byte of data)
        for i in range(16):
            dataBytes.append(i + 1)
                               
        # Append Column Values to Data Frame at Once
        deterministicResults['Total Bytes for Each Data Value'] = dataBytes
        deterministicResults['ECB Correct Diabetics Proportion'] = ecbCorrect1s
        deterministicResults['ECB Correct Non-diabetics Proportion'] = ecbCorrect0s
        deterministicResults['ECB Encryption Time'] = ecbEncryptionTime
        deterministicResults['ECB Decryption Time'] = ecbDecryptionTime
        deterministicResults['CBC Correct Diabetics Proportion'] = cbcCorrect1s
        deterministicResults['CBC Correct Non-diabetics Proportion'] = cbcCorrect0s
        deterministicResults['CBC Encryption Time'] = cbcEncryptionTime
        deterministicResults['CBC Decryption Time'] = cbcDecryptionTime
        
        return deterministicResults
    
    # Exports hex data to a file
    def writeHexToFile(self, filePath, data):
        fp = open(filePath, "w")
        fp.write(str(data))
        fp.close()