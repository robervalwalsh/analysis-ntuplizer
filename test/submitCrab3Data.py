#!/usr/bin/env python

import os.path
import urllib2

from WMCore.Configuration import Configuration

# ---
# Some parameter steering
PROCESS         = 'BTagCSV_2016H_03Feb2017'
RUN_RANGE       = ''
UNITS_PER_JOB   = 500
TYPE            = 'DATA'
PSET            = 'ntuplizer_data_80X_moriond17_H.py'
CAMPAIGN        = 'Run2016/80x_moriond17_reminiaod_03Feb2017_v1'
MYPATH          = '/store/user/%s/' % (getUsernameFromSiteDB())
BASEOUTDIR      = MYPATH+'Analysis/Ntuples/' + TYPE + '/' + CAMPAIGN

# from URL
# ---
#URL             = 'http://www.desy.de/~walsh/cms/analysis/samples/miniaod/Run2016'
#dataset_list    = URL + '/' + PROCESS + '.txt'
#datasets        = urllib2.urlopen(dataset_list)

dataset_list    = 'samples/data/' + PROCESS + '.txt'
f_datasets = open(dataset_list,'r')
datasets = f_datasets.readlines()


# _________________________________________________________________________

if __name__ == '__main__':

   from CRABAPI.RawCommand import crabCommand
   from CRABClient.ClientExceptions import ClientException
   from httplib import HTTPException
    
   from Analysis.Ntuplizer.crabConfig import crabConfig
   config = crabConfig()

# ====== GENERAL
   config.General.workArea += '_' + PROCESS


# ====== DATA   
   config.Data.splitting   = 'LumiBased'
   config.Data.unitsPerJob  = UNITS_PER_JOB
   config.Data.totalUnits   = -1
   config.Data.outLFNDirBase   = BASEOUTDIR + '/'
#   config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt'
#   config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader/'
#   config.Data.allowNonValidInputDataset = True    # If dataset not valid yet, will run over valid files only
   if RUN_RANGE != '':
      config.Data.runRange = RUN_RANGE


# ====== JOBTYPE
   config.JobType.psetName    = PSET
#   config.JobType.inputFiles = ['Fall15_25nsV2_DATA_PtResolution_AK4PFPuppi.txt','Fall15_25nsV2_DATA_PtResolution_AK4PFchs.txt','Fall15_25nsV2_DATA_SF_AK4PFPuppi.txt','Fall15_25nsV2_DATA_SF_AK4PFchs.txt']

   
   for dataset in datasets:
      dataset = dataset.split('\n')[0]
      dataset_name = dataset.split('/')[1]
      dataset_cond = dataset.split('/')[2]
      dataset_tier = dataset.split('/')[3]
#      
      config.Data.inputDataset    = dataset
      config.Data.outputDatasetTag = dataset_cond
#      
      config.General.requestName  = dataset_name
      config.General.requestName += '_'+dataset_cond
      if RUN_RANGE != '':
         config.General.requestName += '_'+RUN_RANGE
      
      print config.General.requestName
#      
      crabCommand('submit', config = config)

# _________________________________________________________________________
