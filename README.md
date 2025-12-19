# block-cipher-mode-attacks
A research project in CIS*4520 where I analyzed the robustness of different block cipher modes of operation. Please see the report for more details on my research methodology.

## To Start the Program

*The user should install Python, pycryptodomex, pandas and the time module before attempting to run the code.*

1.  Ensure that there is a CSV file in the data folder corresponding to the format of the ’diabetes.csv’ file that I submitted.
2. Then, run the program from the root directory of the project
by entering: python src/TestRunner.py
3. Enter a CSV data file name when prompted, for example: diabetes.csv
4. Indicate whether you want to enter a single test (0), or the
full test suite (1).

### To Run a Single Test
1.  Enter a mode of operation to encrypt with (ECB or CBC).
2. Enter a padding length. Note that the data length for one single data value (a 1 or 0) will be equal to 1 byte + the provided padding length (amount of appended spaces).
3. Enter a specific diabetic to conduct the KPA with (to obtain the plaintext, ciphertext pair of).
4. Review the results.

### To Run the Test Suite.
1. Enter a specific diabetic to conduct the KPA with (to obtain
the plaintext, ciphertext pair of).
2. After the test suite has run, enter a CSV to save the results
to.
3. Review the results. The output CSV file will be in the ’results’ folder.