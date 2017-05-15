#!/usr/bin/env python

import os
import os.path
import urllib2
import importlib
import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

# colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple


ARGSN = len(sys.argv)
if ARGSN < 3:
   print (R+"You need to provide the CMSSW python config and the samples file in this order"+W)
   sys.exit()

# ---
# Some parameter steering
UNITS_PER_JOB   = 5 
TYPE            = 'MC'
CAMPAIGN        = 'Trigger17/91x_triggerstudies17_phasei_fall16_flatpu28to62_userv39'

ARGS = sys.argv
PSET = ARGS[1]
SAMPLE = ARGS[2]

psetname, pset_ext = os.path.splitext(PSET)
samplename, sample_ext = os.path.splitext(SAMPLE)

if not ( os.path.isfile(PSET) and pset_ext == '.py' ):
   print (R+"The given python config does not exist or it is not a python file"+W)
   sys.exit()

if not ( os.path.isfile(SAMPLE) and sample_ext == '.txt' ):
   print (R+"The given sample list file does not exist or it is not a txt file"+W)
   sys.exit()

# ---
# Some parameter steering
PROCESS         = samplename.split('/')[-1]
MYPATH          = '/store/user/%s/' % (getUsernameFromSiteDB())
BASEOUTDIR      = MYPATH+'Analysis/Ntuples/' + TYPE + '/' + CAMPAIGN

dataset_list    = 'samples/mc/' + PROCESS + '.txt'
f_datasets = open(dataset_list,'r')
datasets = f_datasets.readlines()

import FWCore.ParameterSet.Config as cms
#from ntuplizer_mc_765_summer_conferences_2016_v1 import process
pset = PSET.split('.')[0]
process = __import__(pset).process #(see why it does not work!)

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
   config.Data.splitting   = 'FileBased'
   config.Data.unitsPerJob  = UNITS_PER_JOB
   config.Data.totalUnits   = -1
   config.Data.outLFNDirBase   = BASEOUTDIR + '/'
#   config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader/'
#   config.Data.allowNonValidInputDataset = True    # If dataset not valid yet, will run over valid files only

# ====== JOBTYPE
#   config.JobType.inputFiles = ['Fall15_25nsV2_MC_PtResolution_AK4PFPuppi.txt','Fall15_25nsV2_MC_PtResolution_AK4PFchs.txt','Fall15_25nsV2_MC_SF_AK4PFPuppi.txt','Fall15_25nsV2_MC_SF_AK4PFchs.txt']
   config.JobType.numCores    = 4

   for dataset in datasets:
      dataset=dataset.replace(" ", "")
      cross_section = 1.
      if len(dataset.split(',')) > 1:
         cross_section = dataset.split(',')[1].split('\n')[0]
         dataset = dataset.split(',')[0]
      else:
         dataset = dataset.split('\n')[0]
         
      dataset_name = dataset.split('/')[1]
      dataset_cond = dataset.split('/')[2]
      dataset_tier = dataset.split('/')[3]
       
       
      
#      
      config.Data.inputDataset     = dataset
      config.Data.outputDatasetTag = dataset_cond
#      
      config.General.requestName  = dataset_name
# use if needed in private productions (modify accordingly)
#      processname = dataset_cond.split('_')
#      config.General.requestName  += '_'+processname[0]+'-'+processname[1]+'_oldGT'
#      print config.General.requestName 
#     
      process.MssmHbbTrigger.CrossSection = cms.double(cross_section)
      psettmp = pset+'_tmp.py'
      f = open(psettmp, 'w')
      f.write(process.dumpPython())
      f.close()
#      
      config.JobType.psetName    = psettmp
#
      outtext = "Submitting dataset " + dataset + "..."
      print (O+str(outtext)+W) 
      crabCommand('submit', config = config)
      print (O+"--------------------------------"+W)
      print
#
      os.remove(psettmp)

# _________________________________________________________________________
