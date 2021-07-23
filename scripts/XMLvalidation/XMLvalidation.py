import ROOT
from array import array
from math import isnan
import sys

from MV2defaults import default_values

inputfileName            = sys.argv[1]
treeName                 = 'bTag_AntiKt4EMTopoJets'
variableToCompare        = sys.argv[2] #'jet_mv2c100'
xmlFile                  = sys.argv[3] #'TMVAClassification_BDTG.weights.xml'
mva_method               = 'BDTG'
maxNumberOfJetsToRunOver = -1
###################################################
###################################################
###################################################

# collect list of variables from XML file - they need to be declared in the reader in the same order
xml = ROOT.TXMLEngine()
xmldoc = xml.ParseFile(xmlFile)
mainnode = xml.DocGetRootElement(xmldoc)
child = xml.GetChild(mainnode)
while(xml.GetNodeName(child)!='Variables'):
	child = xml.GetNext(child)

attr = xml.GetFirstAttr(child)
nVars =  xml.GetAttrValue(attr)
print xml.GetAttrName(attr),' ', nVars

varList = []

varnode = xml.GetChild(child)
varList.append( xml.GetAttr(varnode,'Expression') )

for i in range(1,int(nVars)):
	varnode = xml.GetNext(varnode)
	varList.append( xml.GetAttr(varnode,'Expression') )

print varList

#dictionary from the name used in the XML file to the branch name in the ntuple
xmlNameToBranchName = {
"pt_uCalib" 			: "jet_pt_orig",
"eta_abs_uCalib" 		: "jet_eta_orig",
"ip2" 					: "jet_ip2" 	,
"ip2_c" 				: "jet_ip2_c" 	,
"ip2_cu" 				: "jet_ip2_cu" 	,
"ip3" 					: "jet_ip3" 	,
"ip3_c" 				: "jet_ip3_c" 	,
"ip3_cu" 				: "jet_ip3_cu" 	,
"sv1_ntkv" 				: "jet_sv1_ntrkv",
"sv1_mass" 				: "jet_sv1_m",
"sv1_efrc" 				: "jet_sv1_efc",
"sv1_n2t" 				: "jet_sv1_n2t",
"sv1_Lxy" 				: "jet_sv1_Lxy",
"sv1_L3d" 				: "jet_sv1_L3d",
"sv1_sig3" 				: "jet_sv1_sig3d",
"sv1_dR" 				: "jet_sv1_deltaR",
"jf_n2tv" 				: "jet_jf_n2t",
"jf_ntrkv" 				: "jet_jf_ntrkAtVx",
"jf_nvtx" 				: "jet_jf_nvtx",
"jf_nvtx1t" 			: "jet_jf_nvtx1t",
"jf_mass" 				: "jet_jf_m",
"jf_efrc" 				: "jet_jf_efc",
"jf_dR" 				: "jet_jf_dR",
"jf_sig3" 				: "jet_jf_sig3d",
"mass_first_vtx" 		: "mass_first_vtx",
"nTrk_vtx1" 			: "nTrk_vtx1",
"e_first_vtx" 			: "e_first_vtx",
"e_frac_vtx1" 			: "e_frac_vtx1",
"closestVtx_L3D" 		: "closestVtx_L3D",
"JF_Lxy1" 				: "JF_Lxy1",
"vtx1_MaxTrkRapidity" 	: "vtx1_MaxTrkRapidity",
"vtx1_AvgTrkRapidity" 	: "vtx1_AvgTrkRapidity",
"vtx1_MinTrkRapidity" 	: "vtx1_MinTrkRapidity",
"MaxTrkRapidity" 		: "MaxTrkRapidity",
"MinTrkRapidity" 		: "MinTrkRapidity",
"AvgTrkRapidity" 		: "AvgTrkRapidity",
"rnnip_pb" 				: "jet_rnnip_pb",
"rnnip_pc" 				: "jet_rnnip_pc",
"rnnip_pu" 				: "jet_rnnip_pu",
"rnnip_ptau" 			: "jet_rnnip_ptau",
}


reader = ROOT.TMVA.Reader()


varPointers = {}

for xmlName in varList:
	varname = xmlName

	varPointers[varname] = array('f',[-999])
	reader.AddVariable(varname,varPointers[varname])


reader.BookMVA(mva_method,xmlFile)

fin = ROOT.TFile(inputfileName, 'read')
tree = fin.Get(treeName)

fout = ROOT.TFile('validation_output.root','recreate')
outputtree = ROOT.TTree('outputtree','outputtree')
xmlResult = array('f',[-999])
resultsFromNtuple = array('f',[-999])

outputtree.Branch('xmlResult',xmlResult,'xmlResult/F')
outputtree.Branch(variableToCompare,resultsFromNtuple,variableToCompare+'/F')

nEntries = tree.GetEntries()
nJetsProccessed = 0

for i in range(nEntries):
	tree.GetEntry(i)

	njets = tree.jet_pt_orig.size()

	varToCompareVector = getattr(tree, variableToCompare)

	for jetI in range(njets):

		for xmlName in varList:

			varvector = getattr(tree, xmlNameToBranchName[xmlName])
			varValue = varvector.at(jetI)

			if xmlNameToBranchName[xmlName] == 'jet_eta_orig': #eta is special, we need its abs value but its not stored in the ntuple
				varValue = abs(varValue)


			if isnan(varValue):
				varValue = default_values[xmlName]

			varPointers[xmlName][0] = varValue
			#print xmlName, ' ',varPointers[xmlName][0], ' ',varvector.at(jetI)


		resultsFromNtuple[0] = varToCompareVector.at(jetI)

		xmlResult[0] = reader.EvaluateMVA(mva_method)

		outputtree.Fill()
		nJetsProccessed+=1
	if (nJetsProccessed > maxNumberOfJetsToRunOver) and maxNumberOfJetsToRunOver > 0:
		break


c = ROOT.TCanvas('c','c',600,600)


outputtree.Draw(variableToCompare+' : xmlResult')

c.Print(variableToCompare+'_validation.png')



outputtree.Write()
fout.Close()


