
# RI-based-CPSC : A chromatographic peak shift correction tool based on the N-acyl glycine retention index system for LC-MS data


### Research background
In large-scale metabolomics analysis, it is crucial to preprocess and integrate the raw LC-MS data from run to run, determining the accuracy of follow-up statistical comparation and qualitative analysis. In this respect, peak alignment is a necessary step to enable the comparison of LC-MS-based data across multiple samples. However, the negative effect of RT drift cannot be completely avoided, the data integration capability of currently commonly used peak alignment algorithms is limited, particularly in multi-batch analysis over long time intervals. N-acyl glycine RI system system can well correct the drift of RT. Based on this, we consider that RI technique can be used as a “time corrector” to adjust the time points during the whole LC-MS analysis process. 

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
    












