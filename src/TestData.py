class TestData:
    # Takes in a passed dataframe and uses that as the test data
    def __init__(self, df) -> None:
        self.df = df
        self.len = len(self.df)
        self.observedDiabetics = self.countOccurrences("1")
        self.observedNonDiabetics = self.countOccurrences("0")
    
    # Converts Data to a String, with a Given Amount of Padding to Add a Magnitude of Determnistic Data
    def transformData(self, paddingLength):
        paddingString = ''
        
        # Adding Padding According to the Amount Specified
        for i in range(paddingLength):
            paddingString += ' '
            
        stringOutcomes = paddingString.join(self.df)
        
        return stringOutcomes
    
    # Counts the amount of occurrences of a given character within the data frame
    # Used for counting number of diabetics and non-diabetics
    def countOccurrences(self, char):
        count = 0
        
        for i in self.df:
            if i == char:
                count += 1
                
        return count
    
    # Locates the posth '1' in the Data Frame (starting at 1)
    def findDiabetic(self, pos):
        count = 0
        
        for i in range(len(self.df)):
            if self.df.iloc[i] == '1':
                count += 1
                
                if count == pos:
                    return i
            
        # Returns -1 if it cannot find the posth diabetic
        return -1
    
    def getRowValue(self, i):
        return self.df.iloc[i]