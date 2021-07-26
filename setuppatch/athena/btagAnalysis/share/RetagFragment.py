##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
### THIS is the full retagging configuration
if doRetag:
  suffix = 'retag'

  def RenameInputContainerCfgExample(suffix, JetCollectionShort, tracksKey = 'InDetTrackParticles'):
    acc=ComponentAccumulator()
    # Delete BTagging container read from input ESD
    AddressRemappingSvc, ProxyProviderSvc=CompFactory.getComps("AddressRemappingSvc","ProxyProviderSvc",)
    AddressRemappingSvc = AddressRemappingSvc("AddressRemappingSvc")
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::JetAuxContainer#' + JetCollectionShort + 'Jets.BTagTrackToJetAssociator->' + JetCollectionShort + 'Jets.BTagTrackToJetAssociator_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::JetAuxContainer#' + JetCollectionShort + 'Jets.JFVtx->' + JetCollectionShort + 'Jets.JFVtx_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::JetAuxContainer#' + JetCollectionShort + 'Jets.SecVtx->' + JetCollectionShort + 'Jets.SecVtx_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::JetAuxContainer#' + JetCollectionShort + 'Jets.btaggingLink->' + JetCollectionShort + 'Jets.btaggingLink_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::BTaggingContainer#BTagging_' + JetCollectionShort + '->BTagging_' + JetCollectionShort + '_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::BTaggingAuxContainer#BTagging_' + JetCollectionShort + 'Aux.->BTagging_' + JetCollectionShort + '_' + suffix+"Aux."]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::VertexContainer#BTagging_' + JetCollectionShort + 'SecVtx->BTagging_' + JetCollectionShort + 'SecVtx_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::VertexAuxContainer#BTagging_' + JetCollectionShort + 'SecVtxAux.->BTagging_' + JetCollectionShort + 'SecVtx_' + suffix+"Aux."]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::BTagVertexContainer#BTagging_' + JetCollectionShort + 'JFVtx->BTagging_' + JetCollectionShort + 'JFVtx_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::BTagVertexAuxContainer#BTagging_' + JetCollectionShort + 'JFVtxAux.->BTagging_' + JetCollectionShort + 'JFVtx_' + suffix+"Aux."]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.TrackCompatibility->' + tracksKey + '.TrackCompatibility_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_d0->' + tracksKey + '.btagIp_d0_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_z0SinTheta->' + tracksKey + '.btagIp_z0SinTheta_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_d0Uncertainty->' + tracksKey + '.btagIp_d0Uncertainty_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_z0SinThetaUncertainty->' + tracksKey + '.btagIp_z0SinThetaUncertainty_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_trackMomentum->' + tracksKey + '.btagIp_trackMomentum_' + suffix]
    AddressRemappingSvc.TypeKeyRenameMaps += ['xAOD::TrackParticleAuxContainer#' + tracksKey + '.btagIp_trackDisplacement->' + tracksKey + '.btagIp_trackDisplacement_' + suffix]
    acc.addService(AddressRemappingSvc)
    acc.addService(ProxyProviderSvc(ProviderNames = [ "AddressRemappingSvc" ]))
    return acc

# Based off of https://gitlab.cern.ch/atlas/athena/-/blob/master/PhysicsAnalysis/JetTagging/JetTagAlgs/BTagging/python/BTagRun3Config.py#L152
  def myBTagRecoSplitCfg(inputFlags, JetCollectionShort = 'AntiKt4EMTopo', **kwargs):
    from AthenaConfiguration.ComponentAccumulator import ComponentAccumulator
    from JetTagCalibration.JetTagCalibConfig import JetTagCalibCfg
    from BTagging.BTagRun3Config import JetBTaggerSplitAlgsCfg
    from BTagging.BTagRun3Config import RenameInputContainerCfg
    result=ComponentAccumulator()
    # Can only configure b-tagging for collisions; not cosmics, etc.
    if inputFlags.Beam.Type != 'collisions':
      return result

    result.merge(RenameInputContainerCfgExample(suffix, JetCollectionShort))

    taggerList = inputFlags.BTagging.run2TaggersList
    result.merge(JetTagCalibCfg(inputFlags, TaggerList = taggerList, **kwargs))

    secVertexingAndAssociators = {'SV1':'BTagTrackToJetAssociator','JetFitter':'BTagTrackToJetAssociator'}
    result.merge(JetBTaggerSplitAlgsCfg(inputFlags,
                                        JetCollection = JetCollectionShort,
                                        TaggerList = taggerList,
                                        SecVertexingAndAssociators = secVertexingAndAssociators,
                                        **kwargs))

    from AthenaCommon.ConcurrencyFlags import jobproperties
    if jobproperties.ConcurrencyFlags.NumThreads() == 0 :
      for el in result._allSequences:
        el.name = "TopAlg"

    return result

  # Component accumulator implementation
  # TODO: loop over jet collections
  JetCollectionShort = JetCollections[0].split('Jets')[0]
  from AthenaCommon.Configurable import Configurable
  Configurable.configurableRun3Behavior=1
  ConfigFlags.loadAllDynamicFlags()
  #ConfigFlags.Btagging.dump()
  # Translate all needed flags from old jobProperties to a new AthConfigFlag Container
  ConfigFlags.IOVDb.GlobalTag=globalflags.ConditionsTag()
  ConfigFlags.GeoModel.AtlasVersion = jp.Global.DetDescrVersion()
  # Additional b-tagging related flags
  ##ConfigFlags.BTagging.SaveSV1Probabilities = True
  ##ConfigFlags.BTagging.RunJetFitterNN = True
  ConfigFlags.BTagging.run2TaggersList = ['IP2D','IP3D', 'SV1', 'SoftMu', 'JetFitterNN']
  ConfigFlags.dump()
  # Configure BTagging algorithm
  if not callable(myBTagRecoSplitCfg):
    raise TypeError("CAtoGlobalWrapper must be called with a configuration-function as parameter")
  result = myBTagRecoSplitCfg(ConfigFlags, JetCollectionShort)
  if isinstance(result, tuple):
    ca = result[0]
  else:
    ca = result

  #################################################
    #################################################
  # Configuration examples and debugging printouts
  # See tool_info.txt for examples of printouts
  #################################################

  # List available algorithms:
  print('Available algorithms:')
  for alg in ca.getEventAlgos():
    print('\t'+alg.getName())

  # List available sequences:
  print('Available sequences:')
  for alg in ca.getSequence().Members:
    print('\t'+alg.getName())

  # Get event algorithm
  algoA=ca.getEventAlgo("btagging_"+JetCollectionShort.lower())
  # Print algorithm
  print(algoA)
  # Print TagToolList associated to algorithm
  print(algoA.BTagTool.TagToolList)
  # Print IP3DTag of TagToolList
  print(algoA.BTagTool.TagToolList["IP3DTag"])
  # Get trackSelectorTool from IP3DTag
  toolA=algoA.BTagTool.TagToolList["IP3DTag"].trackSelectorTool
  # Print trackSelectorTool
  print (toolA)
  # Optionally modify the tool parameters for testing
  # toolA.nHitBLayer=3
  # print (toolA)

  #### A.X. what is this??

  # Get another event algorithm
  ## algoB=ca.getEventAlgo(JetCollectionShort.lower()+"_sv1_secvtxfinding")
  # Get secondary vertex finder tool from algorithm
  ##toolB=algoB.SecVtxFinder
  # Optionally modify the tool parameters for testing
  # toolB.CutPixelHits = 5
  # print(toolB)

  # Get another event algorithm
  ##algoC=ca.getEventAlgo("btagging_201903_dl1_antikt4empflow")
  # Get jet decorator tool
  ###toolC = algoC.JetDecorator
  # Optionally modify the algorithm parameters for testing
  # toolC.nnFile = 'BTagging/201903/dl1r/antikt4empflow/network.json'
  # print(toolC)

  ca.printConfig(printDefaults=True,printComponentsOnly=False)

  Configurable.configurableRun3Behavior=0
  from AthenaConfiguration.ComponentAccumulator import appendCAtoAthena
  appendCAtoAthena(ca)

  print (algSeq)
