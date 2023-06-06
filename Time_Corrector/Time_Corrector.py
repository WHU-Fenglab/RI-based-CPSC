#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from progress.bar import Bar
from matplotlib import pyplot as plt
import pyopenms
import numpy as np
import bisect

class MSDataProcess(object):   
    def __init__(self,DataPath):
        self.OriginData = pyopenms.MSExperiment()
        self.file_path = DataPath
        ''' 储存文件pyopenms.MzMLFile().store("filtered.mzML", exp) '''
        if self.file_path.endswith('mzML'):
            pyopenms.MzMLFile().load(self.file_path,self.OriginData)
        elif self.file_path.endswith('mzXML'):
            pyopenms.MzXMLFile().load(self.file_path,self.OriginData)
        self.OriginData.sortSpectra(True)
        self.__param = {'MS1_Tor':0.000005,'RT_Tor':5,'min_Int':10000,'min_RT':6,'max_Noise':3000,
                        'Deconvolution':False,'FeatureDetectPlot':2,'MergeRule':'Intersection',
                        'UpDown_gap':10,'saveAutoList':False}
        self.Origin_RT_List = np.array([])
        self.Origin_MZ_List = []
        self.Origin_Int_List = []
        self.MS2_Pre = []
        self.MS2_RT_List = []
        self.MS2_MZ_List = []
        self.MS2_Int_List = []
        self.MS2_RelInt=[]
        for i in self.OriginData:
            if i.getMSLevel()==1:
                MZ_temp, Int_temp = i.get_peaks()
                self.Origin_MZ_List.append(np.around(MZ_temp,5))
                self.Origin_Int_List.append(np.around(Int_temp,0))
                self.Origin_RT_List = np.append(self.Origin_RT_List,i.getRT())
            if i.getMSLevel()==2:
                Pre_temp = i.getPrecursors()[0].getMZ() 
                MZ_temp,Int_temp=i.get_peaks()
                temp_range = list(filter(lambda x:MZ_temp[x]<=Pre_temp,range(len(MZ_temp)))) # and Int_temp[x]>1000
                temp_range = list(filter(lambda x:len(np.where(abs(MZ_temp[temp_range]-MZ_temp[x])/MZ_temp[x]<self.__param['MS1_Tor']))==1 or
                                         Int_temp[x]==max(Int_temp[np.where(abs(MZ_temp[temp_range]-MZ_temp[x])/MZ_temp[x]<self.__param['MS1_Tor'])]),temp_range))
                if len(temp_range)>0:
                    MZ_temp = MZ_temp[temp_range]
                    Int_temp = Int_temp[temp_range]
                    self.MS2_Pre.append(Pre_temp)
                    self.MS2_RT_List.append(i.getRT())
                    self.MS2_MZ_List.append(np.around(MZ_temp,5))
                    self.MS2_Int_List.append(np.around(Int_temp,0))
                    self.MS2_RelInt.append(max(Int_temp[temp_range]))
        self.Origin_RT_List = np.around(self.Origin_RT_List,3)
        self.MS2_RT_List = np.around(self.MS2_RT_List,3)
        self.MS1_Data = {'Scan_Time':self.Origin_RT_List,'MZ_List':self.Origin_MZ_List,'Int_List':self.Origin_Int_List}
        self.MS1_Data = pd.DataFrame(self.MS1_Data)
        self.MS2_Data = {'Scan_Time':self.MS2_RT_List,'Pre_MZ':self.MS2_Pre,'MZ_List':self.MS2_MZ_List,'Int_List':self.MS2_Int_List,'Rel_Int':self.MS2_RelInt}
        self.MS2_Data = pd.DataFrame(self.MS2_Data)
        self.__param['Flow_RT'] = int(self.__param['min_RT']/(2*np.mean(np.diff(self.Origin_RT_List))))+1
        if self.OriginData[0].getInstrumentSettings().getPolarity() == 1:
            self.__param['Polarity'] = 'Positive'
        elif self.OriginData[0].getInstrumentSettings().getPolarity() == 2:
            self.__param['Polarity'] = 'Negtive'
        else:
            self.__param['Polarity'] = 'Not give'
            print('Uncertain Polarity')
    def ClosestPosition(TargetNumber, List):
        if TargetNumber >= List[-1]:
            #print("Close error +")
            return len(List)-1
        elif TargetNumber <= List[0]:
            #print("Close error -")
            return 0
        position = bisect.bisect_left(List, TargetNumber)
        before = List[position-1]
        after = List[position]
        if after - TargetNumber < TargetNumber - before:
            return position
        else:
            return position-1
    def ExtractDataPoint(self,MZ, RTR, RTL,s_min=False, plt_for_test=False, smooth_index=5):
        smooth_index =(smooth_index-1)//2
        if s_min == True:
            RTR = RTR * 60          # min -> s
            RTL = RTL * 60
        RTR_place = MSDataProcess.ClosestPosition(RTR,self.Origin_RT_List)
        RTL_place = MSDataProcess.ClosestPosition(RTL,self.Origin_RT_List)
        RT_List = self.Origin_RT_List[RTL_place:RTR_place]
        Int_List = []
        #MZ_List=[]
        for i in range(RTL_place, RTR_place):
            MZ_place = MSDataProcess.ClosestPosition(MZ,self.Origin_MZ_List[i])
            if MZ_place > len(self.Origin_MZ_List[i])-3:
                MZ_place = len(self.Origin_MZ_List[i])-3
            elif MZ_place < 2:
                MZ_place = 2
            temp_int = []
            #temp_MZ = []
            for ii in range(MZ_place-2, MZ_place+2):
                if MZ*(1-self.__param['MS1_Tor']) < self.Origin_MZ_List[i][ii] < MZ*(1+self.__param['MS1_Tor']):
                    temp_int.append(self.Origin_Int_List[i][ii])
                    #temp_MZ.append(Origin_MZ_List[i][ii])
            if not temp_int:
                Int_List.append(0)
                #MZ_List.append(0)
            else:
                temp_int = np.array(temp_int)
                Int_List.append(temp_int.max())
                #MZ_List.append()
        # smooth
        def GaussSmooth(x):
            if len(x)==5:
                op = x[0]*0.07+x[1]*0.23+x[2]*0.4+x[3]*0.23+x[4]*0.07
            elif len(x)==3:
                op = x[0]*0.17 +x[1]*0.66 +x[2]*0.17
            else:
                op = np.mean(x)
            return op
        smooth_Int_List = list(map(lambda x:GaussSmooth(Int_List[x-smooth_index:x+smooth_index+1]) if x in range(smooth_index,len(Int_List)-smooth_index) else Int_List[x],range(len(Int_List))))
        #smooth_Int_List = list(map(lambda x:np.mean(Int_List[x-smooth_index:x+smooth_index+1]) if x in range(smooth_index,len(Int_List)-smooth_index) else Int_List[x],range(len(Int_List))))
        # plt test
        if plt_for_test == True:
            plt.figure()
            #RT_List = RT_List/60
            #smooth_Int_List = np.array(smooth_Int_List) 
            plt.title(str(MZ))
            plt.plot(RT_List, smooth_Int_List)
            plt.figure()
            plt.title('Raw'+str(MZ))
            plt.plot(RT_List,Int_List)
        # reture
        return RT_List, Int_List
    def set_RIIS(self,RIIS):
        self.RIIS = pd.read_excel(RIIS)
    def Draw_TIC(self,OutputPath=''):
        TIC_Int_List = []
        for i in range(len(self.Origin_Int_List)):
            TIC_Int_List.append(sum(self.Origin_Int_List[i]))
        plt.plot(self.Origin_RT_List,TIC_Int_List)
        plt.show()
        if OutputPath=='':
            pass
        else:
            TIC_Table = {'ScanTime':self.Origin_RT_List,'Intensity':TIC_Int_List}
            TIC_Table = pd.DataFrame(TIC_Table)
            TIC_Table.to_excel(OutputPath)
                                                
class DataAlignment(object):
    def __init__(self):
        self.DataBase = pd.DataFrame(columns=['Data','Data_Name','Tag'])
        self.AlignmentParam = {'MZ_Tor':0.000005,'RT_Tor':0.05,'A':0.5,
                               'Miss_Filter':0.8,'Threshold':5,'RI_Alignment':False}
        self.RefList=pd.DataFrame(columns=['m/z','Int','RT','MS_List','RT_List','MS2_Int','MS2_MZ'])
        self.RefList['m/z'] = self.RefList['m/z'].map(lambda x:'%.4f'%x)
    def add_Data(self,Data,Tag='Sample'):
        # 添加数据
        if Tag == 'Sample' or Tag == 'Blank':
            def namestr(obj, namespace):
                return [name for name in namespace if namespace[name] is obj]
            self.DataBase.at[len(self.DataBase)]=[Data,namestr(Data,globals())[0],Tag]
            self.DataBase.sort_values(by='Tag',ascending=False,inplace=True)
            self.DataBase.reset_index(drop=True,inplace=True)
        else:
            print('Data Tag should be Sample or Blank')
    def show_Data(self):
        # 显示数据
        print(self.DataBase.iloc[:,[1,2]])
    def get_param(self):
        # 获取参数
        print(self.AlignmentParam)
    def set_param(self,Name,Value):
        # 更改参数
        self.AlignmentParam[Name] = Value
        print('set '+Name+' '+str(Value))
    def RI_Correct(self,RIIS_Path='',RefNumber=0):
        def RTO_to_RTC(RTO,t_n_S,t_n1_S,t_n_R,t_n1_R):
            RTC = (RTO-t_n_S)/(t_n1_S-t_n_S)*(t_n1_R-t_n_R)+t_n_R
            return RTC
        if hasattr(self.DataBase.at[RefNumber,'Data'],'RIIS') == False:
            self.RIIS = pd.read_excel(RIIS_Path)
        else:
            self.RIIS = self.DataBase.at[RefNumber,'Data'].RIIS.copy()
        bar = Bar('Calculate RI',max = len(self.DataBase))
        for i in range(len(self.DataBase)):
            bar.next()
            if hasattr(self.DataBase.at[i,'Data'],'RIIS') == False:
                self.DataBase.at[i,'Data'].RIIS = self.RIIS.copy()
                self.DataBase.at[i,'Data'].RIIS['RT']=0.00
                RTL = self.DataBase.at[i,'Data'].Origin_RT_List[0]
                RTR = self.DataBase.at[i,'Data'].Origin_RT_List[-1]
                for ii in range(len(self.DataBase.at[i,'Data'].RIIS)):                
                    MZ = self.DataBase.at[i,'Data'].RIIS['m/z'][ii]
                    [RT_List, Int_List]=self.DataBase.at[i,'Data'].ExtractDataPoint(MZ,RTR,RTL)
                    RT_place = np.where(Int_List==max(Int_List))[0]
                    self.DataBase.at[i,'Data'].RIIS['RT'][ii] = RT_List[RT_place[0]]
        bar.finish()
        self.RIIS = self.DataBase.at[RefNumber,'Data'].RIIS.copy()
        bar = Bar('Calculate RI',max = len(self.DataBase))
        for i in range(len(self.DataBase)):
            bar.next()
            if i != RefNumber:
                exp = pyopenms.MSExperiment()
                for ii in range(len(self.DataBase.at[i,'Data'].Origin_RT_List)):   
                    spectrum = self.DataBase.at[i,'Data'].OriginData[ii]
                    RTO = self.DataBase.at[i,'Data'].Origin_RT_List[ii]
                    n_place = np.where(self.DataBase.at[i,'Data'].RIIS['RT']<=RTO)[0]
                    n1_place = np.where(self.DataBase.at[i,'Data'].RIIS['RT']>RTO)[0]
                    if len(n_place)==0:
                        n_place = n1_place[0]
                        n1_place = n1_place[1]
                    elif len(n1_place)==0:
                        n1_place = n_place[-1]
                        n_place = n_place[-2] 
                    else:
                        n_place = n_place[-1]
                        n1_place = n1_place[0]
                    t_n_S = self.DataBase.at[i,'Data'].RIIS['RT'][n_place]
                    t_n1_S = self.DataBase.at[i,'Data'].RIIS['RT'][n1_place]
                    t_n_R = self.RIIS['RT'][n_place]
                    t_n1_R = self.RIIS['RT'][n1_place]
                    RTC = RTO_to_RTC(RTO,t_n_S,t_n1_S,t_n_R,t_n1_R)
                    spectrum.setRT(RTC)
                    exp.addSpectrum(spectrum)
                dot_place = self.DataBase.at[i,'Data'].file_path.rfind('.')
                OutputPath = self.DataBase.at[i,'Data'].file_path[0:dot_place]
                pyopenms.MzMLFile().store(OutputPath+'_RI.mzML',exp)
        bar.finish()
        
if __name__ == '__main__':
    RI_Origin_1 = MSDataProcess('/Users/lacter/Downloads/HJD_P/1-QC-FS-P-1.mzML')
    RI_Origin_1.set_RIIS('/Users/lacter/Downloads/HJD_P/QC-P-1.xlsx')
    RI_Origin_2 = MSDataProcess('/Users/lacter/Downloads/HJD_P/2-QC-FS-P-2_RI.mzML')
    RI_Origin_2.set_RIIS('/Users/lacter/Downloads/HJD_P/QC-P-2.xlsx')
    RI_Origin_3 = MSDataProcess('/Users/lacter/Downloads/HJD_P/3-QC-FS-P-3_RI.mzML')
    RI_Origin_3.set_RIIS('/Users/lacter/Downloads/HJD_P/QC-P-3.xlsx')
    RI_Origin_4 = MSDataProcess('/Users/lacter/Downloads/HJD_P/4-QC-FS-P-4_RI.mzML')        
    RI_Origin_4.set_RIIS('/Users/lacter/Downloads/HJD_P/QC-P-4.xlsx')
    RI_Origin_Align = DataAlignment()
    RI_Origin_Align.add_Data(RI_Origin_1,Tag='Sample')
    RI_Origin_Align.add_Data(RI_Origin_2,Tag='Sample')
    RI_Origin_Align.add_Data(RI_Origin_3,Tag='Sample')
    RI_Origin_Align.add_Data(RI_Origin_4,Tag='Sample')
    RI_Origin_Align.RI_Correct(RefNumber=0)
    
    RI_Origin_1.Draw_TIC('/Users/lacter/Downloads/HJD_P/TIC-P-1.xlsx')
 

        
        
        
        