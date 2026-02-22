---
title: "Some 'Learning' in Cheminformatics, QSAR and Generative AI"
author: Hao Lan
date: 2026-02-06
permalink: /posts/2026-02-06/
tags:
  - Virtual Screening
  - Machine Learning 
  - Graph Neural Network
  - Generative Chemistry
---

## Introduction
<p style="text-align: justify;">
In 2025, I have written 2 posts about molecular modelling with AI co-folding and physical simulation approaches for SBDD based on my background in physical organic chemistry and biophysics. However, there are several other important aspects of modern computational chemistry for drug discovery, including <b>cheminformatics</b> and <b>machine learning</b>, which have not been touched in my blog yet. During these years in industry, those fields are actually where I have learnt and progressed most deeply and rapidly. In this blog, I would like to share some experience in my journey adapt to multiple positions as both cheminformatician and machine learning engineer in the biotech environment. To demonstrate how data science is applied to the real-world drug discovery, <b>a virtual screening (VS) example of covalent drug discovery in the popular Cereblon (CRBN) chemical space would be presented in this post (Figure 1)</b>. I would go through a deliberate workflow starting from chemical database search to idea enumuration, docking test as well as QSAR study and AI generation under rational supervisions from the perspective of organic and medicinal chemistry.   
</p>
<img src="photos_and_videos/figure_1.png" alt="figure1" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/><br>
<font size="2"><b>Figure 1</b>. The co-crystal structures of CRBN in complex with IMiD glue ligands (left - binary from PDB 4TZ4) and 2 targeted proteins to be degraded (mid - <b>IKZF</b> from PDB 7U8F; right - <b>WIZ</b> from PDB 8TZX), with opportunities in developing covalent drugs.</font><br>

## Study Outlines

1. <b>Data Inspection</b> - Check the chemical space of CRBN-based binder/degrader with commerical and open-source database.

2. <b>Chemical Enrichment</b> - Use traditonal cheminformatics and QM approach to generate synthetic data in the domain of insufficient chemical space.

3. <b>Physical Validation</b> - Apply shape-constrained molecular docking for the virtial screening of large cheminformatic library, to refine the chemical space more realistically.

4. <b>QSAR Modelling</b> - Build classic ML and graph-based deep learning models to classify and identify the prior chemical space of interest (i.e., covalent modulator based on CRBN)

5. <b>Generative AI</b> - Test mature chemical generation models (including smilesRNN module from MorganCThomas/Nxera team and the latest RL-based Reinvent4 platform developped by AZ) for exploring the desired chemical space as well as necessary post-processing including alerts filtration, drug-like rewarding and selection with transferred QSAR model.

## Chemical Database Search and Processing
<p style="text-align: justify;">
There are a lot of chemical database in the public domain, including <i>PubChem, ChEMBL, ZINC, Enamine</i> etc. They are suitable for different purposes and cheminformaticians usually have different preference in choosing those open resources. As a computational medicinal chemist closely supporting pipeline projects all day every day in the TPD field, I found <i>bindingDB</i> and <i>molecularglueDB</i> are useful in covering general dataset published from academia. For people working in the industry, we also quite value those latest data which are less disclosed in the patent especially from our competitors. These documented data often requires extra efforts to extract, annotate and structuralise (thankfully now we have several AI tools such as <i>DECIMER</i> which is used later in this post). Meanwhile, efficient drug design usually needs specific dataset based on synthetically feasible building blocks, and chemical supplier such as <i>Enamine</i> could provide corresponding catagorties to match our critira depending on the task.
</p>
<p style="text-align: justify;">
Those are the database I found very valuable in my daily work but the approach to engineer and utilise them could be even more critical if we want to maximise their benefits. To process data professionally in cheminformatics, I prefer to use KNIME pipeline which is a powerful GUI toolkit developped from JavaScript in manipulating and visualising tubular data (as in csv file) in sequential steps. It has also saved me tons of time from foundamental data engnieering by Python coding with rdkit, pandas and numpy... and I am not yet confident with fully automatic LLM/AI agents nowadays for such processing tasks which would require intensive human expertise in chemistry as well as instant monitoring/debugging capabilities.                          
</p>

### Open-source Database with Activity Labels and Potential Issues
<p style="text-align: justify;">
The <b>figure 2</b> is a KNIME workflow I used to process and merge the data of CRBN chemical space loaded from <i>bindingDB</i> and <i>molecularglueDB</i> respectively. Apart from building the final dataset in sdf format, I also checked all available PDB structure information (for later steps) and inspect the distribution of chemical space through plotting t-distributed Stochastic Neighbour Embedding (t-SNE) - a dimensionality reduction technique to simplify chemical space based on molecular fingerprints and <i>Tanimoto</i> similarity. Since most PROTACs with high molecular weight had been removed and remaining CRBN binders/glues were small molecules and they comprise a dataset with only few hundreds of record, I set the default 1024 Morgan bits (stereo-ignored) based on 2 radius of atom neigbour without worrying about the issue of bits clash. Notably, the most time-consuming step is to classify active/inactive sets from diverse resources, cellular/biophysical assays and detailed conditions etc., which I have to divide and test these labels manually and cautiously.
</p>
<img src="photos_and_videos/figure_2.png" alt="figure2" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 2</b>. The KNIME pipeline to integrate two chemical database, check specific labelled information and visualise the chemical space on t-SNE plot.</font>
<br><br>

<p style="text-align: justify;">
As shown in the <b>figure 3</b>, my major concern is the overwhelming active set compared to insufficicent data with inactive labels. This is a common problem from public database where academic nerds prefer to publish and collect positive results of their research. Based on my experience so far in industry where investment is not a problem, things are completely different: <b>We always collect much more negative data than those positives from our colleagues/collaborators/CROs in the DMTA cycle...</b> Hence I do not think these limited and imbalanced dataset are suitable for ML-based QSAR modelling on any purpose. It is better to seek opportunity and breakthrough from other database even without any activity label.             
</p>
<img src="photos_and_videos/figure_3.png" alt="figure3" width="360px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 3</b>. The t-SNE plot showing imbalanced data distribution between active and inactive CRBN chemical sets that against the need for ML/QSAR analysis properly.</font><br>

### Commerical Database with Cheminformatics Analysis
<p style="text-align: justify;">
There are some libraries of CRBN-focused molecular glues recently released by <i>Enamine</i> and I found they are quite informative and diverse containing scaffolds from <b>classic IMiDs</b> to those latest Phenyl Amino Glutarimide (<b>PAG</b>), Phenyl Dihydrouracil (<b>PD</b>), Phenyl Glutarimide (<b>PG</b>), Acylated Amino Glutarimide (<b>AAG</b>), avadomide and so on. Using KNIME workflow (<b>Figure 4a</b>), I analysed the overall chemical space at different levels. The molecular level is the most obvious representation (over 3000 canonical smiles string uniquely after stripping stereo tokens like '@' for simplicity) and most molecules contain <b> at least 1 imide substructure in ring as the necessary pharamacophore (Figure 4b)</b>. However such comprehensive t-SNE plot looks a bit fuzzy with too many similar or even duplicate scaffolds concentrated together (alternative plotting with UMAP did not help either). For sparse and clustered visualisation, I degenerated the level represented with Murcko scaffolds (basically it only includes the union of ring systems and linkers in a molecule) as well as decomposed MCS (maximum common substructure) cores. Following this focused map, most classes of core scaffold were found belong to IMiDs but the merged dataset still contain some latest scaffolds like PAG/PG as shown in core 10 or 21 for example.
</p>
<img src="photos_and_videos/figure_4a.png" alt="figure4a" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/><br>
<img src="photos_and_videos/figure_4b.png" alt="figure4b" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 4</b>. The KNIME workflow to analyse CRBN-related databases integrated from <i>Enamine</i>, showing major distributions of chemical space represented at diverse levels based on Bemis-Murcko, MCS and R-group decomposition.</font>
<br><br>

### Insufficient Chemical Space for Covalent Modalities based on CRBN
<p style="text-align: justify;">
Then I merged two database together and obviously the <i>Enamine</i> set complement and enrich the chemical space from the public efficiently (<b>Figure 5</b>). There are few overlap but not too much, I guess this is because chemical supplier CROs tend to invent and sell novel hits with better synthetic feasibility rather than just replicate active substances which have been made and reported already. However, the space for covalent CRBN binders and corresponding protein degraders remain inadequate - there are only around 150 entries within 4500 records in the final library.
</p>
<img src="photos_and_videos/figure_5.png" alt="figure5" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 5</b>. Two t-SNE maps showing the limited chemical space of covalent CRBN binders available from public databases.</font>
<br><br>
<p style="text-align: justify;">
To enrich corresponding chemical space, I digged into some papers (DOIs in reference) published by Lyn Jones group in Dana-Farber as well as the latest patent (WO2025/096856A1) released from C4 Therapeutics. There are around 30 more covalent CRBN binders which have not been covered in the previous databases (<b>Figure 6</b>). I think most of them are just CRBN binders with the addtional covalency on HIS-353 (as shown in <b>Figure 1 left</b>) based on the mechanism as far as I know, all containing the fragment of Sulfonyl Fluorides for the desired reactivity. As an experienced drug designer in TPD industry, I realised there could be much more covalent modalities to be developed for CRBN-dependent binders/degraders based on the pipelines and structures recently reported from AZ, BMS, MonteRosa and Novartis... For example, IKZF2 target has an residue HIS-6 on its beta-sheet near G-loop (<b>Figure 1 mid</b>) while WIZ target contain the CYS-11 (<b>Figure 1 right</b>) which is also not far away from the IMiD-binding pocket on CRBN. <b>The question then becomes how to invent chemical space on those targets <i>in silico</i>.</b>     
</p>
<img src="photos_and_videos/figure_6.png" alt="figure6" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 6</b>. The structure of some novel CRBN binders based on the covalency with HIS-353, extracted from recent journals and patents by AI tool <i>DECIMER</i>.</font>

## Synthetic Data Generation by Classic Cheminformatics
<p style="text-align: justify;">
In cheminformatics, one of the most robust way to enumurate chemicals is based on virtual reactions from/between/among different building blocks. We have seen so many examples of using synthons for creating real drug-like molecules which are ready to be made by wet-lab chemists. Meanwhile, most IMiD and Glutarimide derivatives in current datase bear phenyl and other armoatic functionalities. Given limited experience of organic synthesis in my mind, the C-H activation for adding covalent warheads could be a applicable strategy herein. For quick and dirty enrichment, I defined a two-component reaction smarts using rdkit in order to functionalise each sp2-hybridised [c&H1] on each candidate in the dataset (<b>Figure 7</b>). There are around 10-15 warheads I think commonly used for covalent drug discovery where cysteine or histidine is available around the active site. They are supposed to provide enough covalent chemical space built on the CRBN database filled with non-covalent precursors as mentioned (<b>Figure 5</b>).
</p>
<img src="photos_and_videos/figure_7.png" alt="figure7" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 7</b>. The example of two-component reaction to enumurate one IMiD candidate with covalent handles using aromatic C-H functionalisation virtually.</font>
<br><br>
Since the organic database is originally from commercial source, I also managed to perform few extra steps below for the robustness of generation:<br>
<b>1. Remove most protecting groups using defined smarts reactions</b> (carbamate to amine, ester hydrolysis, hydroxyl deprotections etc...)<br>
<b>2. Before the covalent transformation, degenerate diverse structures into Murcko scaffolds for the simplicity as hit library</b> (downsized approximately from 4000 to 2500)<br>
<b>3. After the covalent transformation, ensure imide substructure still exist but not undesired substructures</b> (using 'pains' list except phthalimide and reactive warheads' smarts)<br><br>
<p style="text-align: justify;">
By the way, I prompted AI agents <i>Gemini 3 Pro</i> and <i>Claudex 4</i> using my <i>Copilot Pro</i> account for above tasks. Each individual rdkit function was coded almost perfectly I have to say, but these LLMs failed to have thoughtful consideration when no progressive direction (chatbox command instructions + markdown file protocols) is given by myself as a human cheminformatician to deal with such complex chemical database. The agent itself either forgot to clean protective fragments or just generate invalid/unmatched smarts variables against processing... It seems that we still need to develop chemistry-specialised language models and agents if people want to further unleash productivity.
</p>
<p style="text-align: justify;">
Getting back to the topic, the cheminformatic workflow afforded the amount of 137673 potential covalent CRBN candidates (all MW below 600Da) where a subset of 19678 entries contain the Sulfonyl Fluoride or Fluorosulfate targeting histidine while others could be reactive with cysteine. <b>I think the chemical space become redundent now and it is the time to refine and enrich positives confidently using physics.</b>  
</p>

## Covalent Docking with Structural Constraints
<p style="text-align: justify;">
For virtual screening over 10000 candidates from the previous enumeration, the standard method is molecular docking based on available structure information. According to the quary search from RCSB, most PDB structures in the database are actually holo CRBN co-crystals in closed state (i.e., active for target degradation), either with isoform 4 sequence (uniport A4TVL0) or with human sequence (uniport Q96SW2). Some of these structures would be used to prioritise the chemical space for developing covalent CRBN modulators, molecular glus and PROTACs.  
</p>

### Techniques for Reliable Models in Docking Test
<p style="text-align: justify;">
To test the ensemble docking with reported covalent binders at the beginning, I selected 4TZ4, 5V3O and 8OJH, three high-resolution crystallography of human CRBN closed binary complex (<b>Figure 8</b>), all preserved IMiD ligand scaffolds and conserved binding site under alignment. I believe these consistent structual constraints are suitable to embrace and lock the chemical space as what pursued.
</p>
<img src="photos_and_videos/figure_8.png" alt="figure8" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 8</b>. The aligned crystal structures of CRBN-IMiD complex used for ensemble docking with enumurated datebase in order to enrich covalent binding hits engaging HIS-353.</font>
<br><br>
<p style="text-align: justify;">
Herein, the flexible sidechain mode of AutoDock4 (AD4) was used to process covalent docking based on my experience. It blurs the targeted covalent residue atomtypes and charges in pdbqt grid map, but requires the ligand conjugate anchored on the backbone CA position as expected. To perpare the conjugate, a smarts reaction was defined to create the modality including sidechain. I also did a quick free conformational search/min (ETKDG/MMFF) as well as cyclic imide pharacophore shape alignment (bestRMS < 2A to bioactive Glutarimide as MCS) for picking up the initial 3D rotamer bearing a proper structure of such ring fragment (<b>Figure 9</b>) - so only those freely rotatable torsions are manipulated and searched by AD4 genetic MC algorithm under translational+rotational transformations in the fixed pocket grid.
</p>
<img src="photos_and_videos/figure_9.png" alt="figure9" width="360px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 9</b>. The smarts reaction for preparing histidine covalent ligand adducts used in flexible sidechain docking, followed by Glutarimide (MCS) pharacophore shape alignment to select the initial conformer of each ligand.</font>
<br><br>
<p style="text-align: justify;">
One common chanllenge in molecular docking is to ensure ligands fitting into the right position. Even though the Cartesian location of grid box (20-30 A depending on ligands' size in library) provide some spatial contraints, we could still see some docking conformations shift to cavities that are not normally occupied by the reference ligand. For instance, a covalent CRBN binder explored sites (4 of 5 from AD4 docking clusters) apart from the IMiD pocket (<b>Video 10</b>). Certainly it does not mean those novel poses are completely non-sense, these scenario are rarely seen during the lead optimisation especially when we are confident with the SAR based on the core scaffold with pharamacophores. Some commercial softwares (e.g., Schrodinger Glide) are able to perform core/shape-constrained docking provided with a bioactive ligand conformation and its smarts pattern for reference. Herein, I instructed AI to write an alternative rdkit function for the pose selection with reference containing cyclic imide (<b>Text 11</b>). Because we are dealing with post-docking structures, no re-alignment is needed for calculating RMS to the reference based on their MCS of Glutarimide.
</p>
<video controls>
  <source src="photos_and_videos/video_10.mp4" type="video/mp4">
</video>
<font size="2"><b>Vedio 10</b>. The covalent CRBN docking example showing diverse binding modes generated from AD4 algorithm and scoring functions, which requires further filtration and selection.</font>
<br><br>

```python
def get_mcs_rmsd(query_sdf_path, ref_sdf_path, aligned_sdf_path, aligned=False, cutoff=2.0):

    confs = []
    with Chem.SDMolSupplier(query_sdf_path, removeHs=True, sanitize=True) as suppl_query:
        for conf in suppl_query:
            if conf is None: continue
            confs.append(conf)

    with Chem.SDMolSupplier(ref_sdf_path, removeHs=True, sanitize=True) as suppl_ref:
        ref_mol = suppl_ref[0]
        
    mcs = rdFMCS.FindMCS([confs[0], ref_mol], completeRingsOnly=True, ringMatchesRingOnly=False)
    patt = Chem.MolFromSmarts(mcs.smartsString)

    #check patt contains imide
    imide_smarts = "[!#1]1(-[#6]-[#6]-[#6](-[#7]-[#6]-1=[#8])=[#8])-[!#1]"
    imide_mol = Chem.MolFromSmarts(imide_smarts)
    if not patt.HasSubstructMatch(imide_mol):
        print("Warning: auto MCS does not contain a cyclic imide group, use defined cyclic imide as MCS instead")
        patt = imide_mol
    refMatch = ref_mol.GetSubstructMatch(patt)

    rms_min = None
    best_conf_id = None
    for i, conf in enumerate(confs):
        mv = conf.GetSubstructMatch(patt)
        if aligned == False:
            rms = AllChem.CalcRMS(conf, ref_mol, map=[list(zip(mv, refMatch))])
        else:
            rms = AllChem.AlignMol(conf, ref_mol, atomMap=list(zip(mv, refMatch)))
        if (rms_min is None) or (rms < rms_min):
            rms_min = rms
            best_conf_id = i

    if rms_min <= cutoff:
        with Chem.SDWriter(aligned_sdf_path) as writer:
            conf_with_hs = Chem.AddHs(confs[best_conf_id], addCoords=True)
            conf_with_hs.SetProp("_RMSD_MCS_to_ref", str(rms_min))
            writer.write(conf_with_hs)
        print(f"{aligned_sdf_path} is best valid conformation ID: {best_conf_id} with MCS RMSD: {rms_min} to {ref_sdf_path}")
        return best_conf_id, rms_min
    else:
        print(f"No valid conformation found with MCS RMSD <= {cutoff} A for {query_sdf_path} against {ref_sdf_path}")

        return None, None
```
<font size="2"><b>Text 11.</b> The Python code to get RMSD values of MCS (cyclic imide) from query conformations to a reference in sdf format, and to get the best matched pose for docking selection.</font><br>

### Virtual Screening Results
<p style="text-align: justify;">
Following several days of computational time in my PC using above docking tricks, I managed to refine the chemical space in silico for covalent CRBN binders and degraders targeting IKZF2 and WIZ. The VS for covalent MG ligands in binary and IKZF2 ternary complex are easier becasue their histidines are already in proximity to the binding site near G-loop (<b>2nd & 3rd rows in Figure 12</b>). Meanwhile the CYS-11 from WIZ is a bit distant from the Glutarimide according to structures (<b>1st row in Figure 12</b>), which would require PROTAC-like scaffolds to bridge such gap for the proximity. Apart from these, we need some empirial critira to ensure the drug-likeness from positive docking poses especially when docked candidates are still too much.
</p>
<img src="photos_and_videos/figure_12.png" alt="figure12" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 12</b>. Some packing states in available ternary complex co-crystal structures for WIZ (1st row, 8TZX/9DJX) and IKZF2 (2nd & 3rd rows, 7U8F/7LPS), showing different proximities needed for developing covalent modalities to stabilise coresponding complexes. 
</font>

#### Covalent CRBN Binders and IKZF2 Degraders
<p style="text-align: justify;">
For the covalent CRBN binder excluding target protein, 36554 valid poses were afforded from docking selection (<b>Video 13</b>). Since all stereochemistry were ennumurated before conformational preparations and docking, I converted these 3D objects back to 2D canonical smiles without any stereo-label which is to streamline later QSAR and generative AI studies. Also the principle chiral centre at the C3 position of Glutarimide racemise quickly <i>in vivo</i>... The resulting 14042 unique molecules were filtrated by 3 criteria:<br>
<b>1. Binding score (AD4 covalent mode) < -10 kcal/mol</b><br>
<b>2. Molecular weight < 500 Da</b><br>
<b>3. Rotatable bond count < 7</b><br>
The logics was to find proximate ligand but not overwhelmed by the size (a common bias in docking algorithm where larger molecule tends to scored with lower binding energy). The limited number of rotatable bonds also ensured the drug-likeness without too much entropic penality or strain energy against binding. These criteria eliminate 14000 redundent candidates to around 1500 reasonably (<b>Figure 14</b>). 
</p>
<video controls>
  <source src="photos_and_videos/video_13.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 13</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from binary co-crystallography (4TZ4/5V3O/8OJH).</font>
<br><br>
<img src="photos_and_videos/figure_14.png" alt="figure14" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 14</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 defined criteria for covalent CRBN binders.</font>
<br><br>
<p style="text-align: justify;">
For the covalent IKZF2 degrader, I loose the criteria of MW and nRotB (< 550 Da & < 8) but tighten the cutoff for binding score (< -11 kcal) after docking. This garentee the complementarity towards degrading target and its histidine residue in ternary complex based on my experience (<b>Video 15 & Figure 16</b>). Overall, around 1000 entries were prioritised from over 10000 valid docking poses. There are some candidates even having their scaffolds overlaied with the exposed pharmacophore of aromaticity in shape, which built the confidence for further drug design based on such VS if anyone else want to try (I am no more synthetic chemist unfortunately...)
</p>
<video controls>
  <source src="photos_and_videos/video_15.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 15</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from IKZF2 ternary complexes (7U8F/7LPS).</font>
<br><br>
<img src="photos_and_videos/figure_16.png" alt="figure16" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 16</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 tailored criteria for IKZF2 covalent MGs.</font>

#### Covalent WIZ Degraders
<p style="text-align: justify;">
Targeting CYS-11 in CRBN-WIZ ternary complex is more challenging, not only because cysteine favours diverse warheads that are usually different from histidine but also its position is away from the binding interface as mentioned before. To prepare ligands for covalent docking, I checked the shortest bonding pathlength (SBP) on 2D graph structure from imide nitrogen to electrophilic carbon (thanks to Gemini for the tip of such rdkit function) and then defined 9 suitable reactions with the cysteine sidechain in order to reduce the size of library containing over 100000 precursors from previous enumuration (<b>Figure 17</b>).
</p>
<img src="photos_and_videos/figure_17.png" alt="figure17" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 17</b>. The pre-docking process to focus the library on cys-dependent PROTAC-like WIZ covalent degraders. Those candidates with 13 SBP at least were chosen for subsquent covalent additions and ligand preparations.</font>
<br><br>
<p style="text-align: justify;">
The covalent docking with WIZ afforded many satifactory poses and drug-like hits from my perspective (<b>Video 18</b>). This time I tighten both critira of docking score (< -12.5 kcal/mol) and nRotB (< 7) for the desired cooperativity in PROTAC development (<b>Figure 19</b>). The majority of winners bear cyanamide warhead while only few poses are based on the Michael addition. There are many L-shape scaffolds observed to complement the interface between CRBN and WIZ. Again these VS structures are attached in my github repository for any researcher interested in further development potentially.
</p>
<video controls>
  <source src="photos_and_videos/video_18.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 18</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from WIZ ternary complexes (8TZX/9DJX).</font>
<br><br>
<img src="photos_and_videos/figure_19.png" alt="figure19" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 19</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 tailored criteria for WIZ covalent PROTACs.</font>

## QSAR Modelling
<p style="text-align: justify;">
Following above VS screening results, both covalent and non-covalent CRBN binders were merged together to enrich the original CRBN chemical database with diverse covalent modalities. I used the QED score over 0.5 (a druglikeness index balance Lipinski's rules etc.) to further filter all covalent docking candidates already passing my criterias, which made corresponding library size shrink to around 2500 - a fairly reasonable amount regarding the non-covalent CRBN candidate pool (size just over 4000) from open and enamine databases (<b>Figure 20</b>). For the QSAR modelling, I decided to start with a classification task which is commonly used for binary decision-making in industry when the early-stage data is high-throughput but noisy. This prior would also guide later regression model and generative AI to have more confidence for the desired predictions.
</p>         
<img src="photos_and_videos/figure_20.png" alt="figure20" width="480px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 20</b>. The distribution of chemical space between covalent and non-covlant classes for CRBN.</font>

### Classification Task to Identify Covalent CRBN Ligand
<p style="text-align: justify;">
The chemical identification is a common task especially in toxicity study. Rather than determining whether a substance is hazard or not, here it was applied to identify covalent CRBN candidate with ML approaches. Since I have annotated most common covalent warheads somehow in a previous step (please check <b>Figure 7</b>), the purpose was to build a model that try to learn my experience as a chemist so such modality could be classified automatically.
</p>
<p style="text-align: justify;">
<b>For practical ML in chemistry as indiviual researcher, a key point is to focus on the specific domain.</b> When the data was prepared as shown in <b>Figure 20</b>, I also tried to include some covalent modalities from other enamine library even though they are not from the CRBN chemical space at all. However I realised those noise (i.e., positive for covalency but negative for CRBN covalency) actually confuse the machine to learn effective patterns, either through embedded fingerprints or node/edge/graph-level matrix, that are responsible for the covalency in CRBN space... Unless for transferred learning (in that case one also need to enrich the universe of non-crbn & non-covalent space), it is better to build a small model straightforwardly that is suitable for specific task in the field of each drug discovery project.        
</p>

#### Classic Machine Learning with SVM and Tree Classifiers (RF and XGBoost)
<p style="text-align: justify;">
Based on my experience, some classic ML approaches could provide robust performance and generalisation on the QSAR classification task given the limited datasize of chemical space here below 10000. To start with, I tested support vector machine (SVM) based on a proper string of Morgan fingerprints (set size 8192 with radius 2 according to the occupancy screening in advance). The majority of on-bits come from the imide pharacophore as shown in <b>Figure 21</b>, which is not a concern for me since SVM could decide boundaries based on sparse but critical features in hyperplane.
</p>
<img src="photos_and_videos/figure_21.png" alt="figure21" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 21</b>. The most common structures of on-bit from CRBN chemical space embedding with Morgan fingerprints (size 8192 with radius 2).</font>
<br><br>
<p style="text-align: justify;">
To ensure the generalisation capability of ML model, different Murcko scaffolds were distributed into training (80%) and testing (20%) sets. After the grid search of hyperparameters in scikit-learn (e.g., cost, gamma and kernal for SVM classifier) based on cross-validation within training set, the model performed so well that the prediction on testset almost reach 1.0 accuracy as well as 1.0 MCC (Matthews correlation coefficient - a statistical index balancing both precision and recall qualities in binary classification). To double check reasoning (one advantage of most classic ML models), I plotted the importance of top 25 fingerprint features in SVM (<b>Figure 22 top</b>). The interpretation is clear - the model did learn and make decisions from those most likely warheads including bits which are relevent to Sulfonyl Fluorides and Acrylamides.
</p>
<p style="text-align: justify;">
Two common tree models, Random Forest (RF) and extreme gradient boosting (XGBoost), were tried next. Following similar CV grid search (max branch depth, number of estimators, sub-sample/features etc.) for model training and tuning, all testing performaces are perfect as expected. The XGBoost model demonstrated most steady classification and reasonable interpretation after several runs, where more weights/bias were built on Cyanamide-relevent bits in complex decision trees (<b>Figure 22 down</b>).
</p>
<img src="photos_and_videos/figure_22.png" alt="figure22" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 22</b>. The top-feature importance plot based on Morgan fingerprints respectively for tuned SVM, RF and XGBoost models, to classify the covalent modality from others in CRBN chemical space.</font>
<br><br>
<p style="text-align: justify;">
Noteworthy, tuning the hyperparameter with grid search is a time-consuming step to establish a model properly in days. With the help from Claude, Bayesian optimisation using optuna module was coded and tried to search for a best set of hyperparameters (<b>Test 23</b>). Under 100 iterations in just few hours, the algorithm found a XGBoost model which is competible to classify all testset correctly based on similar feature importances. This reminded me with MCMC (Markov Chain Monte Carlo - also a type of Bayesian/Gaussian process if I am correct) for searching low-energy molecular conformations efficiently as I mentioned in the previous blog. <b>To find global optimum/minimum in a distribution or an energy landscape for example, we might not always need all trials based on <i>ab initio</i> physics. The sufficient high-quality data, empirical paradigms (e.g., DFT, force-field potential or even just model architecture) and approperate statistical methods together could lead us to the ground truth faster despite the approximation in anyway (i.e., the ideology of engineering).</b> This is my simple understanding so far in data science as physical chemist doing interdisciplinary studies...                      
</p>

```python
#Tuning hyperparameters of XGBoost using Optuna based on Bayesian optimization
import optuna

def objective(trial):
    # 1. Define the search space
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 2, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 1.0),
    }
    # 2. Initialize model with suggested params
    model = XGBClassifier(**param, random_state=42, eval_metric='logloss')
    
    # 3. Use train data to get a score (using MCC as our metric)
    score = cross_val_score(model, 
                            X_train,
                            y_train,
                            cv=5,
                            scoring='matthews_corrcoef').mean()
    
    return score

# 4. Create a "study" and optimize
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
print(f"Best Params: {study.best_params}")

#Testing best XGBoost from Optuna
best_xgb_optuna = XGBClassifier(**study.best_params,
                                random_state=42,
                                eval_metric='logloss')
best_xgb_optuna.fit(X_train, y_train)
y_pred = best_xgb_optuna.predict(X_test)
acc_optuna = accuracy_score(y_test, y_pred)
mcc_optuna = matthews_corrcoef(y_test, y_pred)
print(f"Optimised XGBoost - Test MCC: {mcc_optuna:.4f} | Test ACC: {acc_optuna:.4f}")
```
<font size="2"><b>Text 23.</b> The Python code to tune hyperparameters of XGBoost classifier with Bayesian optimisation.</font><br>

#### Classification by Deep Learning with Graph Neural Networks (GCN, GAT and GIN)
<p style="text-align: justify;">
The classification model was also built with graph neural network. Following some tutorials from DeepChem, TeachOpenCADD and blogger MaximeLabonne as well as advise from AI agent, each CRBN molecule in my dataset was embeded into graph data at first. For example with Thalidomide (<b>Figure 24</b>), the adjacent matrix was created to show bonding connectivities (edge) among all atoms (node) - a simplied version of graph. In DeepChem modules, I found its graph featuriser convert the chemical structure into 3 sub-matrices: <b>node features, edge index and edge features</b>. The first and second matrix are compulsory to construct a graph while the edge features (e.g., bond types) might be redundent since node features already contain such information implicitly. Moreover, the massage passing algorithm and mean/max/sum aggregate for pooling update in most classic GNN architectures are not very sensitive to edge type as far as I have learnt from LLMs, and we are not predicting chemical properties that are closely associated with bond. Hence, the matrix of edge features was dropped for simplicity as suggested by workshop.                  
</p>
<img src="photos_and_videos/figure_24.png" alt="figure24" width="480px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 24</b>. The adjacent matrix of Thalidomide as a simply encoded graph in 2D, and the actual object featurised by DeepChem module for this study.</font>
<br><br>
<p style="text-align: justify;">
To be honest, deep learning (DL) is seldom used for my daily QSAR work as computational chemist in biotech, neither am I software engineer nor mathematician by professional training. There was no knowledge of Linear Algrebra or Matrix Transformation in my mind. During the xmas holiday before I wrote this blog, I took a certain amount of time to get familiar with PyTorch and modularise each DL step in the workflow below based on my coding experience and AI proficiency:
<br><br>
<b>1. Graph Featurisation, Collate, Scaffold-based Splitting and Dataloader Preparation</b><br>
<b>2. Epoch Training with backward propagation together with Adam Optimisation on BCE loss function</b><br>
<b>3. Some Regularisations to avoid over-fitting as well as The Evaluation using MCC for binary classification</b><br> 
<b>4. Tunning Hyperparameters - batch size, learning rate and hidden dimensions in each GNN architecture</b><br>
see the notebook of pytorch_GNN_classification.ipynb for more details...
</p>
<p style="text-align: justify;">
For the forward architecture, I tried Graph Convolutional Network (GCN), Graph Isomorphism Network (GIN) as well as Graph Attention Network (GAT). Both GCN and GIN were inspired from TeachOpenCADD tutorial while GAT was proposed by my Gemini agent (<b>Text 25</b>). There might be inappropriate layers and readout functions from professional perspective of data science, however a recent research from cheminformaticians in GSK suggested: <b>The GNN architecture is less important than hyperparamter optimisation and feature engineering for QSAR study</b> (DOIs in reference). With the deepchem graph featurised from rdkit canonical smiles string (stereo-ignored), I decided to focus on tuning hyperparameters in order to maximise GNN performances on the classification of covalent CRBN ligand modalities. 
</p>

```python
import torch
import torch.nn as nn
import torch.nn.functional as Fun
from torch.nn import Linear, Sequential, BatchNorm1d, ReLU
from torch_geometric.nn import GCNConv, GINConv, GATConv, global_mean_pool, global_add_pool

# Set device to GPU RTX5070 in Hao's laptop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Common hyperparameters to be tuned later
HIDDEN_DIM = 32
BATCH_SIZE = 64
LEARNING_RATE = 0.001
EPOCHS = 100
EARLY_STOP_PATIENCE = 5
# Some regularisation parameters to prevent overfitting issue given limited crbn data < 10000
DROPOUT_P = 0.5
WEIGHT_DECAY = 1e-4
# Initial random seed which will be varied 2 more times (21, 0) for robustness testing
RANDOM_SEED = 42

# Define GNN architectures: GCN, GIN, and GAT
class GCN(torch.nn.Module):
    def __init__(self, in_features, dim_h):
        super().__init__()
        # GCNConv layers for graph convolutional operations
        self.conv1 = GCNConv(in_features, dim_h)
        self.conv2 = GCNConv(dim_h, dim_h)
        self.conv3 = GCNConv(dim_h, dim_h)
        self.lin = torch.nn.Linear(dim_h, 1)
    def forward(self, graphs_in):
        # Normalize input to a list of graph objects
        graphs_list = list(graphs_in)
        x_list = []
        edge_list = []
        batch = []
        node_offset = 0
        # Build concatenated Tensors (x, edge_index, batch vector)
        for i, g in enumerate(graphs_list):
            # Convert node features and edge index to 2 tensors and move them to device (GPU/CUDA)
            nf = torch.tensor(g.node_features, dtype=torch.float32).to(device)
            ei = torch.tensor(g.edge_index, dtype=torch.long).to(device)            
            # Shift edge indices by the current node offset
            edge_list.append(ei + node_offset)
            x_list.append(nf)
            # Create batch vector for this graph (all nodes get the same graph index)
            n_nodes = nf.shape[0]
            batch.append(torch.full((n_nodes,), i, dtype=torch.long, device=device))
            node_offset += n_nodes
        # Concatenate all features, edges, and batch vectors
        x = torch.cat(x_list, dim=0)
        e = torch.cat(edge_list, dim=1)
        batch = torch.cat(batch, dim=0)
        # GCN layers with ReLU activations
        x = self.conv1(x, e)
        x = x.relu()
        x = self.conv2(x, e)
        x = x.relu()
        x = self.conv3(x, e)
        # Global Pooling with mean aggregation for GCN graph-level prediction
        x = global_mean_pool(x, batch)
        # Readout layer
        x = Fun.dropout(x, p=DROPOUT_P, training=self.training)
        x = self.lin(x) # Output logits (unscaled)
        return x.squeeze(-1) # Squeeze to shape [batch_size]    

class GIN(torch.nn.Module):
    def __init__(self, in_features, dim_h):
        super(GIN, self).__init__()
        # Add BatchNorm for GIN stability
        self.conv1 = GINConv(
            Sequential(Linear(in_features, dim_h), BatchNorm1d(dim_h), ReLU(), 
                      Linear(dim_h, dim_h), BatchNorm1d(dim_h), ReLU())
        )
        self.conv2 = GINConv(
            Sequential(Linear(dim_h, dim_h), BatchNorm1d(dim_h), ReLU(), 
                      Linear(dim_h, dim_h), BatchNorm1d(dim_h), ReLU())
        )
        self.conv3 = GINConv(
            Sequential(Linear(dim_h, dim_h), BatchNorm1d(dim_h), ReLU(), 
                      Linear(dim_h, dim_h), BatchNorm1d(dim_h), ReLU())
        )
        self.lin = Linear(dim_h, 1)
    def forward(self, graphs_in):
        graphs_list = list(graphs_in)
        x_list = []
        edge_list = []
        batch = []
        node_offset = 0
        for i, g in enumerate(graphs_list):
            nf = torch.tensor(g.node_features, dtype=torch.float32).to(device)
            ei = torch.tensor(g.edge_index, dtype=torch.long).to(device)
            edge_list.append(ei + node_offset)
            x_list.append(nf)
            n_nodes = nf.shape[0]
            batch.append(torch.full((n_nodes,), i, dtype=torch.long, device=device))
            node_offset += n_nodes
        x = torch.cat(x_list, dim=0)
        e = torch.cat(edge_list, dim=1)
        batch = torch.cat(batch, dim=0)
        # GIN layers with MLPs and BatchNorm
        x = self.conv1(x, e)
        x = self.conv2(x, e)
        x = self.conv3(x, e)
        # Global Pooling with sum aggregation for GIN graph-level prediction
        x = global_add_pool(x, batch)
        x = Fun.dropout(x, p=DROPOUT_P, training=self.training)
        x = self.lin(x)
        return x.squeeze(-1)  

class GAT(torch.nn.Module):
    def __init__(self, in_features, dim_h, heads=3):
        super(GAT, self).__init__()
        # GATConv layers for graph attention operations
        self.conv1 = GATConv(in_features, dim_h, heads=heads, concat=True)
        self.conv2 = GATConv(dim_h * heads, dim_h, heads=heads, concat=True)
        self.conv3 = GATConv(dim_h * heads, dim_h, heads=1, concat=False)
        self.lin = Linear(dim_h, 1)
    def forward(self, graphs_in):
        graphs_list = list(graphs_in)
        x_list = []
        edge_list = []
        batch = []
        node_offset = 0
        for i, g in enumerate(graphs_list):
            nf = torch.tensor(g.node_features, dtype=torch.float32).to(device)
            ei = torch.tensor(g.edge_index, dtype=torch.long).to(device)
            edge_list.append(ei + node_offset)
            x_list.append(nf)
            n_nodes = nf.shape[0]
            batch.append(torch.full((n_nodes,), i, dtype=torch.long, device=device))
            node_offset += n_nodes
        x = torch.cat(x_list, dim=0)
        e = torch.cat(edge_list, dim=1)
        batch = torch.cat(batch, dim=0)
        # GAT layers with attention mechanism
        x = self.conv1(x, e)
        x = x.relu()
        x = self.conv2(x, e)
        x = x.relu()
        x = self.conv3(x, e)
        # Global Pooling with mean aggregation for GAT graph-level prediction
        x = global_mean_pool(x, batch)
        x = Fun.dropout(x, p=DROPOUT_P, training=self.training) 
        x = self.lin(x)
        return x.squeeze(-1)
```
<font size="2"><b>Text 25.</b> The Python code for 3 common GNN architectures in PyTorch used for chemical classification based on DeepChem GraphData.</font><br>
<p style="text-align: justify;">
Following the grid search (<b>Figure 26</b>), all GNN models are able to identify those covalent molecules in CRBN chemical space with perfect precision, recall and accuarcy (> 0.95). Compared to GCN and GAT, the GIN model demonstrated most robust mcc stabilities regardless of hyperparameters. Similarly with Bayesian optimisation, a well-tuned graph model (GIN with hidden_dim=16, batch_size=256 and learning_rate=0.001) was rapidly obtained for nearly all correct classifications (mcc up to 0.98). <b>It seems that both classic ML and GNN approaches are able to deal with the chemical classification task in this study... Then how about regression modelling?</b>
</p>
<img src="photos_and_videos/figure_26.png" alt="figure26" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 26</b>. The hyperparameter screening result for all graph models trained to make binary classification between covalent and non-covalent CRBN binders.</font><br>

### Regression Task on Electrophilicity
<p style="text-align: justify;">
In covalent drug discovery, the estimation of reactivity is a common task for medicinal chemists. With complex biophysical assays, we are able to measure indicators like Kd/ki for binding kinetics in covalent mechanism. Alternatively, the glutathione (GSH) reactivity assay could provide high throughput screening on chemicals targeting a cysteine residue in approximation. For computational chemistry, the reactivity might be even evaluated roughly from ligand electrophilicity through calculating HOMO, LUMO energies and their gaps based on QM approach. Since I have annotated classes of covalent and non-covalent compounds in CRBN chemical space empirically, it would be sensible to check if such label could be characterised and quantified through numerical numbers based on the scientific computation.                   
</p>

#### Quantum Chemical Calculations
<p style="text-align: justify;">
To calculate molecualr electronic properties reliably within the CRBN chemical space, I instructed my agent for a workflow starting from ETKDG(MMFF) conformational search, xTB geometry optimisations to single-point energy calculations with UMA model as well as Boltzmann averaging on ensembles in vaccum (<b>Figure 27</b>). This is a compromised approach to screen over 10000 hit candidates, considering slow computation speed with MD simulations and DFT calculations but acceptable accuracy with atomic NNP energies and semi-empirical xTB properties based on my previous experience.  
</p>
<img src="photos_and_videos/figure_27.png" alt="figure27" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 27</b>. The example to calculate eletrophilic properties (conformationally dependent) for 2 distinct CRBN ligand modalities respectively based on a quick & dirty statistical quantum mechanical workflow.</font>
<br><br>
<p style="text-align: justify;">
Comparing HOMO, LUMO and gap energies between the covalent and the non-covalent class of my CRBN chemical space (<b>Figure 28</b>), some statistically significant differences (p < 0.05 in MWU and t-test) could be observed: All covalent species tend to have lower LUMO, higher HOMO and smaller gap values than others. The distribution of xTB-based electrophilicity index is also more significant for the covalent class. 
</p>
<img src="photos_and_videos/figure_28.png" alt="figure28" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 28</b>. The distribution of HOMO, LUMO, gap energies and electrophilicty index (&omega;) in covalent and non-covalent classes of CRBN chemical space.</font><br>

$$\omega = \frac{(E_{H} + E_{L})^2}{4(E_{L} - E_{H})}$$

<p style="text-align: justify;">
Nevertheless, these molecular-level QM features are insufficient to classify the covalency confidently in desired chemical space. This was also confirmed by researches from Bayer and Boehringer Ingelheim (DOIs in reference). We might need some further physical calculations associated with the warhead fragment (e.g., atom attribute of Fukui indices in FMO, reaction activation energy with nucleophilic residue etc.) in order to convince ourself of actual covalency for CRBN-based binder or degrader... Given that LUMO value is more relevant to electrophilicity (i.e., the orbital which accept electrons) and its distribution approach Gaussian in our chemical space (<b>Figure 28 second</b>), I decided to test some regression models on it.               
</p>

#### Benchmarking Models for LUMO Prediction
