# For the ntuple production of prompt reco era Hv2

import FWCore.ParameterSet.Config as cms

process = cms.Process("MssmHbb")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016SeptRepro_v7')


## Options and Output Report
process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )

output_file = 'ntuple.root'
## TFileService
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(output_file)
)

## ============ TRIGGER FILTER =============== 
## Enable below at cms.Path if needed 
process.triggerSelection = cms.EDFilter( "TriggerResultsFilter",
    triggerConditions = cms.vstring(
                                      'HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v*',
                                      'HLT_DoubleJetsC100_DoubleBTagCSV_p026_DoublePFJetsC160_v*',
                                      'HLT_DoubleJetsC112_DoubleBTagCSV_p014_DoublePFJetsC112MaxDeta1p6_v*',
                                      'HLT_DoubleJetsC112_DoubleBTagCSV_p026_DoublePFJetsC172_v*',
# online b-tag triggers for efficiencies
                                      'HLT_DoubleJetsC100_SingleBTagCSV_p014_v*',
                                      'HLT_DoubleJetsC100_SingleBTagCSV_p014_SinglePFJetC350_v*',
                                      'HLT_DoubleJetsC100_SingleBTagCSV_p026_v*',
                                      'HLT_DoubleJetsC100_SingleBTagCSV_p014_SinglePFJetC350_v*',
# jet triggers for efficiencies
                                      'HLT_PFJet40_v*',
                                      'HLT_PFJet60_v*',
                                      'HLT_PFJet80_v*',
                                      'HLT_PFJet140_v*',
                                      'HLT_PFJet200_v*',
    ),
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
    l1tResults = cms.InputTag( "" ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)

#################################################
## Update PAT jets
#################################################

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

## b-tag discriminators
# no need to re-do existing algos, save CPU time
bTagDiscriminators = [
#     'pfTrackCountingHighEffBJetTags',
#     'pfTrackCountingHighPurBJetTags',
#     'pfJetProbabilityBJetTags',
#     'pfJetBProbabilityBJetTags',
#     'pfSimpleSecondaryVertexHighEffBJetTags',
#     'pfSimpleSecondaryVertexHighPurBJetTags',
#     'pfCombinedSecondaryVertexV2BJetTags',
#     'pfCombinedInclusiveSecondaryVertexV2BJetTags',
#     'pfCombinedMVAV2BJetTags',
    'deepFlavourJetTags:probudsg',
    'deepFlavourJetTags:probb',
    'deepFlavourJetTags:probc',
    'deepFlavourJetTags:probbb',
    'deepFlavourJetTags:probcc',
    'deepFlavourCMVAJetTags:probudsg',
    'deepFlavourCMVAJetTags:probb',
    'deepFlavourCMVAJetTags:probc',
    'deepFlavourCMVAJetTags:probbb',
    'deepFlavourCMVAJetTags:probcc'    
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
    btagDiscriminators = bTagDiscriminators
)
updateJetCollection(
    process,
    labelName = 'Puppi',
    jetSource = cms.InputTag('slimmedJetsPuppi'),
    jetCorrections = ('AK4PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
    btagDiscriminators = bTagDiscriminators
)


## ============ EVENT FILTER COUNTER ===============
## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer("EventCountProducer")
process.FilteredEvents = cms.EDProducer("EventCountProducer")

## ============ PRIMARY VERTEX FILTER ===============
process.primaryVertexFilter = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlineSlimmedPrimaryVertices"), # primary vertex collection name
   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"), # ndof>thr=4 corresponds to sum(track_weigths) > (thr+3)/2 = 3.5 so typically 4 good tracks
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)

## ============  THE NTUPLIZER!!!  ===============
process.MssmHbb     = cms.EDAnalyzer("Ntuplizer",
    MonteCarlo      = cms.bool(False),
    UseFullName     = cms.bool(False),
    ###################
    TotalEvents     = cms.InputTag("TotalEvents"),
    FilteredEvents  = cms.InputTag("FilteredEvents"),
    PatJets     = cms.VInputTag(  
                cms.InputTag("selectedUpdatedPatJets"),
                cms.InputTag("selectedUpdatedPatJetsPuppi"),
                ), 
    JECRecords      = cms.vstring  (           # for the JEC uncertainties
                "AK4PFchs",
                "AK4PFPuppi",
                ),
    # commented to use globaltag, uncomment if using text files                
#     JECUncertaintyFiles = cms.vstring  (
#                "",
#                "",
#                ),
    JERRecords      = cms.vstring  (           # for the JER
                "AK4PFchs",
                "AK4PFPuppi",
                ),
    # commented to use globaltag, uncomment if using text files                
#     JERResFiles     = cms.vstring  (
#                 "",
#                 "",
#                 ),
#     JERSfFiles      = cms.vstring  (
#                 "",
#                 "",
#                 ),
    FixedGridRhoAll = cms.InputTag("fixedGridRhoAll"),
    PatMETs     = cms.VInputTag(
                cms.InputTag("slimmedMETs"),
                cms.InputTag("slimmedMETsPuppi")
                ), 
    PatMuons    = cms.VInputTag(
                cms.InputTag("slimmedMuons")
                ), 
    PrimaryVertices = cms.VInputTag(
                cms.InputTag("offlineSlimmedPrimaryVertices")
                ), 
    BTagAlgorithms = cms.vstring   (
                                    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
                                    'pfJetProbabilityBJetTags',
                                    'pfCombinedMVAV2BJetTags',
                                    'deepFlavourJetTags:probudsg',
                                    'deepFlavourJetTags:probb',
                                    'deepFlavourJetTags:probc',
                                    'deepFlavourJetTags:probbb',
                                    'deepFlavourJetTags:probcc',
                                    'deepFlavourCMVAJetTags:probudsg',
                                    'deepFlavourCMVAJetTags:probb',
                                    'deepFlavourCMVAJetTags:probc',
                                    'deepFlavourCMVAJetTags:probbb',
                                    'deepFlavourCMVAJetTags:probcc'    
               ),
    BTagAlgorithmsAlias = cms.vstring   (
                                         'btag_csvivf',
                                         'btag_jetprob',
                                         'btag_csvmva',
                                         'btag_deeplight',
                                         'btag_deepb',
                                         'btag_deepc',
                                         'btag_deepbb',
                                         'btag_deepcc',
                                         'btag_deepmvalight',
                                         'btag_deepmvab',
                                         'btag_deepmvac',
                                         'btag_deepmvabb',
                                         'btag_deepmvacc',
                    ),
    TriggerResults  = cms.VInputTag(cms.InputTag("TriggerResults","","HLT")),
    TriggerPaths    = cms.vstring  (
    ## I recommend using the version number explicitly to be able to compare 
    ## however for production one has to be careful that all versions are included.
    ## Thinking of a better solution...
                                  'HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v',
                                  'HLT_DoubleJetsC100_DoubleBTagCSV_p026_DoublePFJetsC160_v',
                                  'HLT_DoubleJetsC112_DoubleBTagCSV_p014_DoublePFJetsC112MaxDeta1p6_v',
                                  'HLT_DoubleJetsC112_DoubleBTagCSV_p026_DoublePFJetsC172_v',
#
                                  'HLT_DoubleJetsC100_SingleBTagCSV_p014_v',
                                  'HLT_DoubleJetsC100_SingleBTagCSV_p014_SinglePFJetC350_v',
                                  'HLT_DoubleJetsC100_SingleBTagCSV_p026_v',
                                  'HLT_DoubleJetsC100_SingleBTagCSV_p014_SinglePFJetC350_v',
#
                                  'HLT_PFJet40_v',
                                  'HLT_PFJet60_v',
                                  'HLT_PFJet80_v',
                                  'HLT_PFJet140_v',
                                  'HLT_PFJet200_v',
               ),
    TriggerObjectStandAlone  = cms.VInputTag(
                     cms.InputTag("selectedPatTrigger"),
                     ),
    TriggerObjectLabels    = cms.vstring  (
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltBTagCaloCSVp014DoubleWithMatching',
                                       'hltDoublePFJetsC100',
                                       'hltDoublePFJetsC100MaxDeta1p6',
#                                       
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltBTagCaloCSVp026DoubleWithMatching',
                                       'hltDoublePFJetsC160',
#
                                       'hltL1sDoubleJetC112',
                                       'hltDoubleJetsC112',
                                       'hltBTagCaloCSVp014DoubleWithMatching',
                                       'hltDoublePFJetsC112',
                                       'hltDoublePFJetsC112MaxDeta1p6',
#
                                       'hltL1sDoubleJetC112',
                                       'hltDoubleJetsC112',
                                       'hltBTagCaloCSVp026DoubleWithMatching',
                                       'hltDoublePFJetsC172',
#
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltSingleBTagCSV0p84',
#
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltSingleBTagCSV0p84',
                                       'hltJetC350',
#                                       
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltSingleBTagCSV0p78',
#
                                       'hltL1sDoubleJetC100',
                                       'hltDoubleJetsC100',
                                       'hltSingleBTagCSV0p84',
                                       'hltJetC350',
#
                                       'hltL1sZeroBias',
                                       'hltSingleCaloJet10',
                                       'hltSinglePFJet40',
#
                                       'hltL1sSingleJet35',
                                       'hltSingleCaloJet40',
                                       'hltSinglePFJet60',
#
                                       'hltL1sSingleJet60',
                                       'hltSingleCaloJet50',
                                       'hltSinglePFJet80',
#
                                       'hltL1sSingleJet90',
                                       'hltSingleCaloJet110',
                                       'hltSinglePFJet140',
#
                                       'hltL1sSingleJet120',
                                       'hltSingleCaloJet170',
                                       'hltSinglePFJet200',
# belongs to JetHT triggers,
# added for backward compatibility,
# particularly on data                                       
                                       'hltPFJetsCorrectedMatchedToCaloJets10',
                                       'hltPFJetsCorrectedMatchedToCaloJets40',
                                       'hltPFJetsCorrectedMatchedToCaloJets50',
                                       'hltPFJetsCorrectedMatchedToCaloJets110',
                                       'hltPFJetsCorrectedMatchedToCaloJets170',
               ),
)

process.p = cms.Path(
          process.TotalEvents *
          process.triggerSelection *
          process.primaryVertexFilter *
          process.FilteredEvents *
          process.MssmHbb
            )


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
   '/store/data/Run2016G/BTagCSV/MINIAOD/03Feb2017-v1/100000/00609568-EAEC-E611-99AF-002590DE6E36.root',
] );


secFiles.extend( [
       ] )

## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
