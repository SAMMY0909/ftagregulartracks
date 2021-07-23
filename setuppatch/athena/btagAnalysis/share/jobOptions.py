##########################################################################################################################################################
##########################################################################################################################################################
from AthenaConfiguration.ComponentAccumulator import ComponentAccumulator
from AthenaConfiguration.ComponentFactory import CompFactory

doRetag = True

from MV2defaults import default_values

JetCollections = [
  #'AntiKtVR30Rmax4Rmin02TrackJets',
  #'AntiKtVR30Rmax4Rmin02TrackJets_BTagging201903',
  #'AntiKt4EMPFlowJets_BTagging201903',
  #'AntiKt4EMPFlowJets_BTagging201810',
  'AntiKt4EMTopoJets'
  ]

#########################################################################################################################################################
#########################################################################################################################################################
### Define input xAOD and output ntuple file name
import glob
from AthenaCommon.AthenaCommonFlags import jobproperties as jp
#jp.AthenaCommonFlags.EvtMax.set_Value_and_Lock( vars().get('EVTMAX', -1) )
#jp.AthenaCommonFlags.SkipEvents.set_Value_and_Lock(16400)
jp.AthenaCommonFlags.EvtMax.set_Value_and_Lock(-1)

inputfiles = [
  #'/afs/cern.ch/work/k/khanov/public/valid1.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.recon.AOD.e4993_s3227_r12581/AOD.25384333._000688.pool.root.1'
  '/afs/cern.ch/work/k/khanov/public/combineTracks/data/DAOD_TEST1.test.pool.root'
   #'AOD.pool.root'
]

# New-style config to fix https://its.cern.ch/jira/browse/ATR-22504
jp.AthenaCommonFlags.FilesInput = inputfiles
jp.AthenaCommonFlags.PoolAODInput.set_Value_and_Lock( inputfiles )
from AthenaConfiguration.AllConfigFlags import ConfigFlags
ConfigFlags.Input.Files = jp.AthenaCommonFlags.FilesInput.get_Value()

# from PyUtils import AthFile
# af = AthFile.fopen( jp.AthenaCommonFlags.FilesInput()[0] )

evtPrintoutInterval = vars().get('EVTPRINT', 5000)
svcMgr += CfgMgr.AthenaEventLoopMgr( EventPrintoutInterval=evtPrintoutInterval )
svcMgr += CfgMgr.THistSvc()
svcMgr.AuditorSvc += CfgMgr.FPEAuditor()
svcMgr.AuditorSvc.FPEAuditor.NStacktracesOnFPE=1

for jet in JetCollections:
  shortJetName=jet.replace("AntiKt","Akt").replace("TopoJets","To").replace("TrackJets","Tr").replace("PFlowJets","Pf")
  svcMgr.THistSvc.Output += [ shortJetName+" DATAFILE='flav_"+shortJetName+".root' OPT='RECREATE'"]

##########################################################################################################################################################
##########################################################################################################################################################

from RecExConfig.RecFlags import rec
print (rec)
rec.doESD.set_Value_and_Lock        (False)
rec.doWriteESD.set_Value_and_Lock   (False)
rec.doAOD.set_Value_and_Lock        (False)
rec.doWriteAOD.set_Value_and_Lock   (False)
rec.doWriteTAG.set_Value_and_Lock   (False)
rec.doDPD.set_Value_and_Lock        (False)
rec.doTruth.set_Value_and_Lock      (False)
rec.doApplyAODFix.set_Value_and_Lock(False)

rec.doCalo.set_Value_and_Lock        (False)
rec.doCaloRinger.set_Value_and_Lock  (False)
rec.doForwardDet.set_Value_and_Lock  (False)
rec.doJetMissingETTag.set_Value_and_Lock(False)
rec.doLArg.set_Value_and_Lock        (False)
rec.doLucid.set_Value_and_Lock       (False)
rec.doTau.set_Value_and_Lock         (False)
rec.doTile.set_Value_and_Lock        (False)
rec.doZdc.set_Value_and_Lock         (False)

include ("RecExCommon/RecExCommon_topOptions.py")

from AthenaCommon.AlgSequence import AlgSequence
algSeq = AlgSequence()

##########################################################################################################################################################
##########################################################################################################################################################
### GEO Business
# from AthenaCommon.GlobalFlags import globalflags
# print "detDescr from global flags= "+str(globalflags.DetDescrVersion)
# from AtlasGeoModel.InDetGMJobProperties import GeometryFlags as geoFlags
# print "geoFlags.Run()   = "+geoFlags.Run()
# print "geoFlags.isIBL() = "+str(  geoFlags.isIBL() )


##########################################################################################################################################################
##########################################################################################################################################################
### this is if you want to re-tag with another calibration file
from BTagging.BTaggingFlags import BTaggingFlags

#BTaggingFlags.ForceMV2CalibrationAlias = False
#BTaggingFlags.CalibrationChannelAliases += ["AntiKt2PV0Track->AntiKt2Track"]
#BTaggingFlags.OutputLevel = DEBUG
#### if the new file is already in the datatbase: simple edit the name
#BTaggingFlags.CalibrationTag = 'BTagCalibRUN12-08-42'
#### if you want to use your own calibration file use this part below
######BTaggingFlags.CalibrationFromLocalReplica = True
######BTaggingFlags.CalibrationFolderRoot = '/GLOBAL/BTagCalib/'
######BTaggingFlags.CalibrationTag = "antonello"
######BTaggingFlags.JetVertexCharge=False

include("RetagFragment.py")

# A.X. how come this doesn't work??
####BTaggingFlags.Print()

##########################################################################################################################################################
### Tools

jvt = CfgMgr.JetVertexTaggerTool('JVT')
#ToolSvc += jvt

ToolSvc += CfgMgr.CP__PileupReweightingTool("prw",
                                            OutputLevel = INFO,
                                            UsePeriodConfig= "MC15"
                                            )


from TrkVertexFitterUtils.TrkVertexFitterUtilsConf import Trk__TrackToVertexIPEstimator
ToolSvc+=Trk__TrackToVertexIPEstimator("trkIPEstimator")


# For running on xAODs without truth jets, un-comment these 2 lines:
#from DerivationFrameworkMCTruth.MCTruthCommon import addStandardTruthContents
#addStandardTruthContents()

##########################################################################################################################################################

algSeq += CfgMgr.BTagVertexAugmenter()

### Main Ntuple Dumper Algorithm
for JetCollection in JetCollections:
  shortJetName=JetCollection.replace("AntiKt","Akt").replace("TopoJets","To").replace("TrackJets","Tr").replace("PFlowJets","Pf")
  alg = CfgMgr.btagAnalysisAlg("BTagDumpAlg_"+JetCollection,
                               OutputLevel=INFO, #DEBUG
                               Stream=shortJetName,
                               # TrackClassTool=ToolSvc.InDetTrkInJetType
                               # JVTtool=ToolSvc.JVT,
                             )

  alg.JetCollectionName = JetCollection
  alg.doJVT = False #if this is false JVT is NAN, if true an attempt is made to update JVT after calibration
  alg.CleanJets = False
  alg.CalibrateJets = False

  alg.DefaultValDictionary = default_values
  alg.ReplaceNanDefaults = True

  if "TrackJets" in JetCollection or "Truth" in JetCollection:
    alg.CleanJets     = False
    alg.CalibrateJets = False
    alg.doJVT = False

  alg.JetCleaningTool.CutLevel= "LooseBad"
  alg.JetCleaningTool.DoUgly  = True

  ## what to include in ntuple ####
  #example
  #alg.exampleBranchInfo = False

  alg.EventInfo = True
  alg.retriveTruthJets = False
  # Flag for truth jet collection to save
  alg.TruthJetCollection = "AntiKt4TruthJets" #(default)
  #alg.TruthJetCollection = "AntiKt4TruthWZJets" # only works on AOD, for use with b-jet energy regression
  alg.JetProperties = True
  ##taggers (MV2, DL1)
  alg.TaggerScores = True
  ##IPxD+RNNIP
  alg.ImpactParameterInfo = True
  ##SV1
  alg.SVInfo = True
  alg.svxCollections = {'jet_sv1_': 'SV1'}
  ##JetFitter
  alg.JetFitterInfo = True
  ###SoftMuonTagger
  alg.SoftMuoninfo = False
  ## b and c hadron truth info
  alg.bHadInfo = False
  alg.bHadExtraInfo = False #include all b and c decay products, and trk_origin
  ## kshort
  alg.kshortInfo = False

  #show debug info for branches
  alg.branchDebug = False

  #track information
  alg.TrackInfo = True
  alg.nRequiredSiHits = 2 #number of hits required to save a track
  alg.TrackCovariance = True

  #you can disable the track augmenter if youre not filling the track branches
  # if alg.TrackInfo and not doRetag:
  algSeq += CfgMgr.Analysis__BTagTrackAugmenterAlg(
    "BTagTrackAugmenter_" + JetCollection,
    OutputLevel = INFO,
  )

  alg.AccessBtagObject = True # for fatjets, turn this to False

  algSeq += alg

  from btagAnalysis.configHelpers import get_calibration_tool
  ToolSvc += get_calibration_tool(CfgMgr, JetCollection, False)

  # from btagAnalysis.configHelpers import get_calibration_tool_2016_calib
  # ToolSvc += get_calibration_tool_2016_calib(CfgMgr, JetCollection, False)


from PerfMonComps.PerfMonFlags import jobproperties as PerfMon_jp
PerfMon_jp.PerfMonFlags.doMonitoring = False
PerfMon_jp.PerfMonFlags.doFastMon = False
