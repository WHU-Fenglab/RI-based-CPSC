#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = "1.0.1"
DESCRIPTION = "An acquisition time correction tool based on the retention index system for LC-MS data"
LONG_DESCRIPTION = "In large-scale metabolomic analysis, it is crucial to preprocess and integrate the raw LC-MS data from run to run, determining the accuracy of follow-up statistical comparation and qualitative analysis. Currently, various peak alignment algorithms have been developed, such as the Joint aligner algorithm and the kernel estimation procedure based algorithm in XCMS. Above algorithms rely on the accurate m/z and RT of features to align chromatographic peaks, and can effectively correct random RT shifts caused by variations in column temperature and slight differences in biological samples. However, their ability to correct systematic RT shifts caused by variations in mobile phase composition, column, and instrumental conditions remains limited. Particularly in large-scale metabolomics analysis, severe systematic RT shifts can result in misalignment or cross-alignment of peaks, leading to reduced alignment accuracy and, in turn, affecting downstream statistical analysis and identification of metabolites. N-alkylglycine RI system can well correct the drift of RT. Based on this, we consider that RI technique can be used as a “time corrector” to adjust the acquisition time during the whole LC-MS analysis process."
    
# Setting up
setup(
      name="Time_Corrector",
      version=VERSION,
      author="Wuhan University, Laboratory of Separation Sciences and Bioanalytical Chemistry, Chen Yaoyu",
      author_email="<740318407@qq.com>",
      description=DESCRIPTION,
      long_description_content_type = "text/markdown",
      long_description = LONG_DESCRIPTION,
      packages=find_packages(),
      install_requires=['pyopenms','pandas','progress','matplotlib','numpy'],
      keywords=['LC-MS','RI system','RT Correct','MS Data'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows"
          ]     
      )