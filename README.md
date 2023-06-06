---
attachments: [Clipboard_2023-05-19-19-56-21.png, Clipboard_2023-05-19-19-56-31.png, Clipboard_2023-05-19-20-26-51.png, Clipboard_2023-05-19-20-39-07.png]
tags: [Import-780d]
title: 'RI Corrector : A retention time drift correction tool in liquid chromatography - mass spectrometry data'
created: '2023-05-19T11:34:26.749Z'
modified: '2023-05-19T12:50:23.793Z'
---

# RI Corrector : A retention time drift correction tool in liquid chromatography - mass spectrometry data


### Research background
$~~~~~$In large-scale metabolomics analysis, it is crucial to preprocess and integrate the raw LC-MS data from run to run, determining the accuracy of follow-up statistical comparation and qualitative analysis. In this respect, peak alignment is a necessary step to enable the comparison of LC-MS-based data across multiple samples. Up date, the peak alignment algorithms used by most MS-based metabolomics software, such as MS-DIAL, XCMS online and MZmine 2, are implemented based on accurate m/z and RT. However, since the negative effect of RT drift cannot be completely avoided, the data integration capability of currently commonly used peak alignment algorithms is inadequate, particularly in multi-batch analysis over long periods of time. As mentioned above, N-alkylglycine RI system system can well correct the drift of RT. Based on this, we consider that RI technique can be used as a “time corrector” to adjust the acquisition time during the whole LC-MS analysis process. 
### System requirements
$~~~$The software is based on Python version 3.9
### Installation
Clone the code from this page，or use pipy to installation.

    pip install RI_Corecctor

### Tutorial
Firstly,The data collected by the instrument must be converted into mzML format, by ProteoWizard MSConvert or other tools. 

#### Import mzML format data:

    Data_1 = EazyMZDataProcess('.../Data_1.mzML')

#### Set the calibrants data:
Calibrants data format ( without RT ) :
| C   | m/z       |
|-----|-----------|
| 3   | 132.0655  |
| 4   | 146.0812  |
| ... | ...       |
Calibrants data format ( with RT (second)  ) :
| C   | m/z       | RT |
|-----|-----------|----|
| 3   | 132.0655  |    |
| 4   | 146.0812  |    |
| ... | ...       |    |

    Data_1.set_RIIS('...\calibrants data.xlsx')

#### Time correction process
Create an time correction process, add data to be corrected, and perform Alignment.

    Data_Align = DataAlignment()
    Data_Align.add_Data(Data_1)
    Data_Align.add_Data(Data_2)
    ...
    Data_Align.RI_Correct(RefNumber=0)

#### Processing Result
The processed data is saved in the original folder as a file with the original data name + _RI
    












