
# RI-based-CPSC : A chromatographic peak shift correction tool based on the N-acyl glycine retention index system for LC-MS data


### System requirements
The software is based on Python version 3.9

### Installation
The user can install the RI-based-CPSC program by cloning the code from this page，or using pipy to install.

    pip install Time_Corecctor

### Chromatographic peak shift correction 
For data integration, the raw data obtained from the LC-MS instrument must be converted into .mzML format by ProteoWizard msConvert or other tools. 

#### Importation of the .mzML format data:

    Data_1 = MZDataProcess('.../Data_1.mzML')

#### Importation of the .xlsx format data of N-acyl glycine calibrants:
For retention time correction, the m/z information of N-acyl glycine calibrants is needed, import the .xlsx format file containing the m/z information of N-acyl glycine calibrants to the program. 

Calibrants data format:
| C   | m/z       |
|-----|-----------|
| 2   | 118.0499  |
| 3   | 132.0655  |
| ... | ...       |


    Data_1.set_RIIS('...\calibrants data.xlsx')

#### Correction process
For chromatographic peak shift correction, users can create a correction process by following these steps: adding the data to be corrected, selecting a reference file, and then performing the correction.

    Data_Align = DataAlignment()
    Data_Align.add_Data(Data_1)
    Data_Align.add_Data(Data_2)
    ...
    Data_Align.RI_Correct(RefNumber=0)

#### Result
The corrected data will be saved in the original folder as .mzML format, using the original data name followed by the suffix '_RI'.
    












