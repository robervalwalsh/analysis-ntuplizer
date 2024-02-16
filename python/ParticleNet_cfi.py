import FWCore.ParameterSet.Config as cms

PNetAlgorithms = cms.PSet(
    PNetAlgorithms = cms.vstring   (
# DeepCSV        
                'pfDeepCSVJetTags:probudsg',
                'pfDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probcc',
                'pfDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probbb',
# DeepFlavour                
                'pfDeepFlavourJetTags:probuds',
                'pfDeepFlavourJetTags:probg',                
                'pfDeepFlavourJetTags:probc',
                'pfDeepFlavourJetTags:probb',
                'pfDeepFlavourJetTags:probbb',
                'pfDeepFlavourJetTags:problepb',
# ParticleNet AK4 Puppi Jets             
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probb',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probc',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probg',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probmu',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probele',                
                'pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll',
# ParticleNet b-regression AK4 Puppi Jets (Central)
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptcorr',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptnu',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreshigh',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreslow',
# ParticleNet b-regression AK4 Puppi Jets (Forward)
                'pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptcorr',
                'pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptnu',
                'pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreshigh',
                'pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreslow',
# ParticleNet QvsG AK4 Puppi Jets
                'pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:QvsG',
                'pfParticleNetFromMiniAODAK4PuppiForwardDiscriminatorsJetTags:QvsG',
    ),
    PNetAlgorithmsAliases = cms.vstring   (
# DeepCSV         
                'btag_deepcsv_light',
                'btag_deepcsv_c',
                'btag_deepcsv_cc',
                'btag_deepcsv_b',
                'btag_deepcsv_bb',
# DeepFlavour                
                'btag_deepjet_light',
                'btag_deepjet_g',
                'btag_deepjet_c',
                'btag_deepjet_b',
                'btag_deepjet_bb',
                'btag_deepjet_lepb',
# ParticleNet btag AK4 Puppi Jets 
                'btag_ak4pfpuppi_pnet_b',
                'btag_ak4pfpuppi_pnet_c',
                'btag_ak4pfpuppi_pnet_uds',
                'btag_ak4pfpuppi_pnet_g',
                'btag_ak4pfpuppi_pnet_mu',
                'btag_ak4pfpuppi_pnet_ele',                
                'btag_ak4pfpuppi_pnet_bvsall'
# ParticleNet b-regression AK4 Puppi Jets (Central)
                'breg_ak4pfpuppi_pnet_ptcorr',
                'breg_ak4pfpuppi_pnet_ptnu',
                'breg_ak4pfpuppi_pnet_ptreshigh',
                'breg_ak4pfpuppi_pnet_ptreslow',
# ParticleNet b-regression AK4 Puppi Jets (Forward)
                'breg_ak4pfpuppi_fw_pnet_ptcorr',
                'breg_ak4pfpuppi_fw_pnet_ptnu',
                'breg_ak4pfpuppi_fw_pnet_ptreshigh',
                'breg_ak4pfpuppi_fw_pnet_ptreslow',
# ParticleNet QvsG AK4 Puppi Jets
                'qvsg_ak4pfpuppi_pnet',
                'qvsg_ak4pfpuppi_fw_pnet',
    ),
)
