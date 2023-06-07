
# RI-based-CPSC : A chromatographic peak shift correction tool based on the N-acyl glycine retention index system for LC-MS data


### System requirements
The software is based on Python version 3.9

### Installation
The user can install the RI-based-CPSC program by cloning the code from this page，or using pipy to install.

    pip install Time_Corecctor

### Tutorial
The raw data obtaineded from the LC-MS instrument must be converted into .mzML format, by ProteoWizard MSConvert or other tools. 

#### Import the .mzML format raw data:

    Data_1 = MZDataProcess('.../Data_1.mzML')

#### Import the .xlsx format data of N-acyl glycine calibrants:
Before correction, import the .xlsx format file containing the m/z information of N-acyl glycine calibrants to the prrogram.

Calibrants data format:
| C   | m/z       |
|-----|-----------|
| 2   | 118.0499  |
| 3   | 132.0655  |
| ... | ...       |


    Data_1.set_RIIS('...\calibrants data.xlsx')

#### Chromatographic peak shift correction
Create a correction process, add data to be corrected, select a reference file and then perform correction.

    Data_Align = DataAlignment()
    Data_Align.add_Data(Data_1)
    Data_Align.add_Data(Data_2)
    ...
    Data_Align.RI_Correct(RefNumber=0)

#### Result
The corrected data will be saved in the original folder as .mzML format with the original data name + "_RI"
    












