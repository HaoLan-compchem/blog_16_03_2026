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
In 2025, I published two posts exploring molecular modeling through AI co-folding and physics-based simulations for Structure-Based Drug Discovery (SBDD), drawing on my background in physical organic chemistry and biophysics. However, some pillars of modern computational drug discovery - <b>cheminformatics</b> and <b>machine learning (ML)</b> - have yet to be discussed here. During my time in the industry, these are the fields where I have experienced the most significant professional growth.
</p>
<p style="text-align: justify;">
In this post, I will share insights from my journey transitioning between the roles of a cheminformatician and an ML engineer within the biotech ecosystem. To demonstrate the real-world application of data science in drug discovery, I will present <b>a virtual screening (VS) workflow targeting the Cereblon (CRBN) chemical space for covalent drug discovery (Figure 1).</b> We will walk through a rigorous pipeline: from chemical database mining and library enumeration to molecular docking, QSAR modelling, and AI-driven generation - all guided by the rational constraints of organic and medicinal chemistry.  
</p>
<img src="photos_and_videos/figure_1.png" alt="figure1" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/><br>
<font size="2"><b>Figure 1.</b> Co-crystal structures of CRBN in complex with IMiD molecular glues. <b>Left:</b> Binary complex (PDB 4TZ4). <b>Center/Right:</b> Ternary complexes with neosubstrates <b>IKZF2</b> (PDB 7U8F) and <b>WIZ</b> (PDB 8TZX), highlighting the structural basis for covalent ligand design with potential warheads.</font><br>

## Study Outlines

1. <b>Data Inspection & Curation</b> - Analysing the chemical space of CRBN-based binders and degraders using both open-source and commercial databases.

2. <b>Chemical Library Enrichment</b> - Utilising traditional cheminformatics and Quantum Mechanics (QM) approaches to generate synthetic data, specifically addressing regions of insufficient chemical space coverage.

3. <b>Physical Validation via VS</b> - Implementing shape-constrained molecular docking to screen large-scale chemical libraries, refining the candidate space based on realistic binding poses and steric complementarity.

4. <b>QSAR Modelling & Hit Identification</b> - Developing classical ML (e.g., SVM, tree models) and Graph Neural Networks (GNNs) to classify, regress and prioritise chemical spaces of interest (specifically CRBN-based covalent modulators).

5. <b>Generative AI & Rational Optimisation</b> - Evaluating industry-standard generative models, including the smilesRNN module from the MorganCThomas/Nxera team and the REINVENT4 Reinforcement Learning (RL) platform developed by AstraZeneca, together with post-processing by alert filtering, descriptor scoring, and transferred QSAR models for the final selection.

## Chemical Database Search and Processing
<p style="text-align: justify;">
The public domain offers a vast array of chemical databases — including <b>PubChem</b>, <b>ChEMBL</b>, <b>ZINC</b>, and <b>Enamine</b> — each serving distinct research purposes. As a computational medicinal chemist supporting Targeted Protein Degradation (TPD) pipelines actively, I have found <b>BindingDB</b> and <b>MolecularGlueDB</b> particularly effective for capturing academic datasets.
</p>
<p style="text-align: justify;">
In an industrial setting, we also place a high premium on the latest competitive intelligence, often found in patent literature. Extracting, annotating, and structuralising this "dark data" requires significant effort... Fortunately, AI-powered tools like <b>DECIMER</b> (used later in this workflow) have streamlined the translation of chemical images into machine-readable formats. Furthermore, efficient drug design necessitates libraries built upon synthetically feasible building blocks. Suppliers like Enamine provide categorised catalogs that allow us to tailor our search criteria to the specific synthetic constraints of a project.
</p>
<p style="text-align: justify;">
While sourcing data is foundational, the engineering approach used to process it is often the differentiator in a project's success. For professional cheminformatics workflows, I prefer <b>KNIME</b> as learnt during the work. This GUI-based platform is exceptionally powerful for manipulating and visualising tabular data (such as CSV or SD files) through sequential nodes. Honestly KNIME has saved me countless hours typically spent on boilerplate data engineering with Python (using RDKit, Pandas, and NumPy modules). While LLM-driven AI agents are evolving, I remain cautious about fully delegating these tasks to them. I believe data processing in chemistry still requires deep domain expertise and the ability to perform real-time monitoring and debugging to ensure structural integrity.
</p>

### Open-Source Curation and Data Imbalance
<p style="text-align: justify;">
<b>Figure 2</b> illustrates the KNIME workflow I developed to aggregate and process CRBN chemical space data from BindingDB and MolecularGlueDB. Beyond generating the final dataset in SDF format, the pipeline extracts available PDB structural metadata for downstream structural analysis. To assess the chemical diversity, I employed <b>t-distributed Stochastic Neighbor Embedding (t-SNE)</b>, a dimensionality reduction technique used here to project the chemical space based on molecular fingerprints and <b>Tanimoto similarity</b>.
</p>
<img src="photos_and_videos/figure_2.png" alt="figure2" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 2</b>. The KNIME pipeline to integrate two chemical database, check specific labelled information and visualise the chemical space on t-SNE plot.</font>
<br><br>
<p style="text-align: justify;">
Since high-molecular-weight PROTACs were filtered out, the remaining dataset consists of a few hundred small-molecule CRBN binders and glues. Given this relatively small scale, I utilised 1024-bit <b>Morgan fingerprints</b> (radius = 2, chirality ignored) without significant concern for bit collisions. The most labor-intensive phase, however, remains the manual classification of "active" versus "inactive" sets. This requires a detailed review of diverse data sources, varying biophysical or cellular assay conditions, and thresholding — all of which demand cautious, expert-led curation. As shown in <b>Figure 3</b>, a major challenge emerged: an overwhelming prevalence of "active" compounds relative to "inactive" labels. This reflects a pervasive <b>publication bias</b> in open databases, where academic research naturally prioritises and reports successful positive results.
</p>
<img src="photos_and_videos/figure_3.png" alt="figure3" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 3</b>. The t-SNE plot showing imbalanced data distribution between active and inactive CRBN chemical sets that against the need for ML/QSAR analysis properly.</font>
<br><br>
<p style="text-align: justify;">
In an industrial setting, the situation is usually opposed. In the <b>Design-Make-Test-Analyze (DMTA)</b> cycle, we typically generate far more negative data than positive hits. Relying solely on these limited and imbalanced public datasets for QSAR modeling is often not productive. To build a robust predictive model, we must look beyond these biased activity labels and seek opportunities in broader, unlabelled chemical libraries or through data augmentation.
</p>

### Commercial Database & Cheminformatics Analysis 
<p style="text-align: justify;">
Recently, Enamine released several targeted libraries focused on CRBN molecular glues. These datasets are highly informative and chemically diverse, spanning a range of scaffolds from <b>classic IMiDs</b> to newer derivatives such as Phenyl Amino Glutarimides (<b>PAG</b>), Phenyl Dihydrouracils (<b>PD</b>), Phenyl Glutarimides (<b>PG</b>), Acylated Amino Glutarimides (<b>AAG</b>), and Avadomide.
</p>
<p style="text-align: justify;">
Using a custom KNIME workflow (<b>Figure 4, upper</b>), I analysed this chemical space at multiple levels. At the molecular level, the dataset contains over 3,000 unique canonical SMILES strings (processed by stripping stereochemical tokens like '@' for simplified initial analysis). As expected, the vast majority of these molecules contain <b>at least one cyclic imide substructure</b>, acting as the essential pharmacophore for CRBN binding (<b>Figure 4, lower</b>).
</p>
<p style="text-align: justify;">
However, raw t-SNE visualisations at the molecular level can appear "fuzzy" due to the high density of similar or near-duplicate analogs — a problem that alternative algorithms like UMAP also struggled to resolve. To achieve a more distinct and interpretable visualisation, I abstracted the molecules to their <b>Bemis-Murcko scaffolds</b> (retaining only the union of ring systems and linkers) and performed <b>Maximum Common Substructure (MCS)</b> decomposition.
</p>
<p style="text-align: justify;">
This hierarchical mapping revealed that while the majority of core scaffolds are rooted in the IMiD class, the merged dataset successfully captures modern chemical matter. For instance, cores 10 and 21 respectively represent the more recently developed PAG and PG scaffolds. This structural decomposition allows us to better navigate the diversity of the library and identify gaps for potential expansion.
</p>
<img src="photos_and_videos/figure_4a.png" alt="figure4a" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/><br>
<img src="photos_and_videos/figure_4b.png" alt="figure4b" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 4</b>. The KNIME workflow to analyse CRBN-related databases integrated from <i>Enamine</i> catalog, showing major distributions of chemical space represented at diverse levels based on Bemis-Murcko, MCS and R-group decomposition.</font><br>

### Addressing the Covalent Modality Gap
<p style="text-align: justify;">
By merging the curated public data with the Enamine dataset, I was able to significantly enrich the available chemical space (<b>Figure 5</b>). There is minimal overlap between the two: This is likely because commercial suppliers prioritise novel, synthetically accessible analogs rather than simply replicating previously reported active substances. Despite this expansion, a critical gap remains: <b>Covalent CRBN binders and their corresponding degraders are still under-represented, accounting for only ~150 entries out of the 4500 records in the final library.</b>
</p>
<img src="photos_and_videos/figure_5.png" alt="figure5" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 5</b>. Two t-SNE maps showing the limited chemical space of covalent CRBN binders available from public and Enamine databases.</font>
<br><br>
<p style="text-align: justify;">
To address this sparsity, I conducted a targeted literature and patent search, focusing on recent works from the <b>Lyn Jones group</b> in Dana-Farber (DOIs in reference) and a recent <b>C4 Therapeutics</b> patent (<b>WO2025/096856A1</b>). This yielded approximately 30 additional covalent CRBN binders not present in the initial databases (<b>Figure 6</b>). Based on the reported mechanism, most of these ligands function as reversible-covalent binders that target <b>HIS-353</b> through a <b>sulfonyl fluoride</b> warhead (as shown in left, <b>Figure 1</b>).
</p>
<img src="photos_and_videos/figure_6.png" alt="figure6" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 6</b>. The structure of some novel CRBN binders based on the covalency with HIS-353, extracted from recent journals and patents by AI tool <i>DECIMER</i>.</font>
<br><br>
<p style="text-align: justify;">
From my perspective as an industrial drug designer, the potential for covalent modalities in CRBN-dependent degradation is far broader than what is currently documented. Recent structural data and pipelines from <b>AstraZeneca, BMS, MonteRosa, and Novartis</b> suggest several untapped opportunities. For instance:

1. The <b>IKZF2</b> neosubstrate features a <b>HIS-6</b> residue on its $\beta$-sheet near the G-loop (middle, <b>Figure 1</b>).
2. The <b>WIZ</b> neosubstrate also contains a <b>CYS-11</b> residue positioned near the IMiD-binding pocket on CRBN (right, <b>Figure 1</b>).

Both residues present strategic handles for covalent engagement. <b>The challenge now lies in how to "invent" and explore this hypothetical chemical space <i>in silico</i> to target these specific residues.</b>
</p>

## Synthetic Data Generation via Classic Cheminformatics 
<p style="text-align: justify;">
In cheminformatics, one of the most robust methods for library enumeration is the use of <b>virtual reactions</b> between building blocks (synthons). This approach ensures that the resulting "drug-like" molecules are synthetically accessible for wet-lab validation. Given that most IMiD and glutarimide derivatives in my current dataset feature phenyl or other aromatic systems, I utilised a <b>C-H activation strategy</b> to append covalent warheads virtually.
</p>
<p style="text-align: justify;">
For this rapid enrichment, I defined a two-component <b>Reaction SMARTS</b> using RDKit to functionalize sp2-hybridised [c;H1] atoms on each candidate in the dataset (<b>Figure 7</b>). I curated a suite of 10–15 warheads commonly employed in covalent drug discovery for targeting proximal cysteine or histidine residues. This strategy successfully transformed non-covalent precursors into a vast, covalent-focused chemical space.
</p>
<img src="photos_and_videos/figure_7.png" alt="figure7" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 7</b>. The example of two-component reaction based on rdkit module to enumurate one IMiD candidate with covalent handles using aromatic C-H functionalisation virtually.</font>
<br><br>
<p style="text-align: justify;">
To ensure the robustness and quality of the generated library, I implemented several critical post-processing steps:

1. <b>Deprotection</b>: Before the aromatic C-H activation, I applied other SMARTS-based transformations to remove common protecting groups (e.g., converting carbamates to amines, ester hydrolysis, and hydroxyl deprotections).

2. <b>Scaffold Simplification</b>: Prior to covalent transformation, I also abstracted the diverse structures into their Bemis-Murcko scaffolds to simplify the hit library, reducing the starting pool from approximately 4000 to 2500 unique frameworks.

3. <b>Quality Control</b>: After enumeration, I verified the presence of the essential imide pharmacophore and filtered out undesired substructures using a modified PAINS list - carefully excluding the phthalimide core and the intended reactive warheads from the 'bad' SMARTS filter.
</P>
<p style="text-align: justify;">
During this process, I leveraged AI agents like <b>Gemini</b> and <b>Claude</b> via my <b>Copilot Pro</b> account to assist with coding. While these LLMs generated individual RDKit functions with high precision, they struggled with the "big picture" logic required for complex database workflows. Without iterative, human-led direction (through structured markdown protocols and specific prompts), the agents sometimes failed to clean protective groups or generated invalid SMARTS variables. This underscores a current truth for industry-level applications: <b>While LLMs are powerful coding assistants, we still require chemistry-specialised language models to fully automate the digital stage of drug discovery with scientific logic</b>.
</p>
<p style="text-align: justify;">
Anyway, this cheminformatics workflow yielded <b>137673 potential covalent CRBN candidates</b> (all with MW < 600 Da). Within this set, 19678 entries contain sulfonyl fluoride or fluorosulfate groups for targeting histidine, while the remainder are designed for cysteine reactivity. <b>With a redundant chemical space at the moment, the next stage is to utilise physics-based refinement to confidently identify high-priority hits.</b>
</p>

## Covalent Docking with Structural Constraints
<p style="text-align: justify;">
To screen the ~140000 candidates generated from our enumeration, I employed molecular docking guided by high-resolution structural data. A query of the <b>RCSB PDB</b> reveals that most available structures represent the <b>"closed" (active) state of CRBN, which is the conformation required for neosubstrate degradation</b>. These include both the isoform 4 (UniProt <b>A4TVL0</b>) and standard human (UniProt <b>Q96SW2</b>) sequences. These structures are essential for prioritising chemical space for covalent modulators, molecular glues, and PROTACs.
</p>

### Ensuring Reliability in Docking Models
<p style="text-align: justify;">
For the initial ensemble docking validation, I selected three high-resolution crystal structures of human CRBN in the closed binary state: <b>4TZ4, 5V3O, and 8OJH (Figure 8)</b>. These structures show highly conserved IMiD-binding sites. By aligning these models, I established a consistent set of structural constraints to "lock" the chemical space and ensure our virtual screening remains biologically relevant.
</p>
<img src="photos_and_videos/figure_8.png" alt="figure8" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 8</b>. The aligned crystal structures of CRBN-IMiD complex (4TZ4, 5V3O, and 8OJH) used for ensemble docking with enumurated datebase, which is to enrich covalent binding hits engaging HIS-353.</font><br>

#### Preparing Ligand before Docking
<p style="text-align: justify;">
I utilised the flexible sidechain mode of AutoDock4 (AD4) for the covalent docking workflow. This method involves masking the target covalent residue's atom types and charges in the PDBQT grid map, while the ligand-adduct is "anchored" to the protein backbone at the Ca position. To prepare these conjugates, I defined a SMARTS-based transformation to create the object of ligand-sidechain adduct in 2D (<b>Figure 9</b>).
</p>
<p style="text-align: justify;">
Furthermore, I performed a two-step conformer preparation:

1. Conformational Sampling: Initial 3D rotamers were generated using the ETKDG method followed by MMFF minimisation.
2. Pharmacophore Alignment: I applied a shape-alignment filter, selecting only those conformers where the cyclic imide pharmacophore maintained an $RMSD < 2$ Å relative to the bioactive glutarimide pose.
</p>
<img src="photos_and_videos/figure_9.png" alt="figure9" width="360px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 9</b>. The SMARTS reaction for preparing histidine covalent ligand adducts used in flexible sidechain docking, followed by Glutarimide MCS pharmacophore shape alignment to select the initial conformer of each ligand.</font>
<br><br>
<p style="text-align: justify;">
Through providing a pre-aligned "bioactive-like" starting conformation, the AD4 Genetic Algorithm only needs to explore the remaining freely rotatable torsions under translational and rotational transformations, significantly improving the efficiency of the search within the fixed grid.
</p>

#### Overcoming Docking Pose Drift with Custom Constraints
<p style="text-align: justify;">
A common challenge in virtual screening is <b>"pose drift"</b>, where ligands dock into peripheral cavities rather than the intended pocket. Even with a defined grid box (20-30 Å), we often observe clusters where the ligand deviates from the reference IMiD coordinates. For example, in one test case below, 4 out of 5 docking clusters occupied sites distal to the IMiD pocket (<b>Video 10</b>).
</P>
<video controls>
  <source src="photos_and_videos/video_10.mp4" type="video/mp4">
</video>
<font size="2"><b>Vedio 10</b>. A covalent CRBN docking example showing diverse binding modes generated from AD4 algorithm and scoring functions, which must require further filtration and selection.</font>
<br><br>
<p style="text-align: justify;">
While commercial software like <b>Schrödinger Glide</b> offers built-in constrained docking by core or/and shape, I developed a custom solution by instructing my AI agent to write an RDKit-based post-docking filter (<b>Text 11</b>). This function calculates the MCS-based RMSD of the glutarimide core against the reference crystal pose. Since the docking was performed in a fixed coordinate system, no further alignment is required - We can simply filter for poses that maintain the essential binding geometry of the imide headgroup.

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
<font size="2"><b>Text 11.</b> The Python function to get RMSD values of MCS (cyclic imide herein) from query conformations (e.g., docked) to a reference in SDF format, in order to get the best matched pose for final selection.</font><br>

### Virtual Screening Results
<p style="text-align: justify;">
Following several days of intensive computation locally using the docking strategies described above, I successfully refined the <i>in silico</i> chemical space for covalent CRBN binders and degraders targeting <b>IKZF2</b> and <b>WIZ</b>. The virtual screening for covalent ligands in the binary and <b>IKZF2</b> ternary complexes was relatively straightforward, as two target histidines are in close proximity to the IMiD binding site near the G-loop (rows 2 & 3, <b>Figure 12</b>). In contrast, CYS-11 in the <b>WIZ</b> neosubstrate is more distal from the glutarimide-binding pocket (row 1, <b>Figure 12</b>). This structural gap necessitates "PROTAC-like" bifunctional scaffolds to bridge the distance and ensure effective proximity for covalent engagement.
</p>
<img src="photos_and_videos/figure_12.png" alt="figure12" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 12</b>. Some packing states in ternary complex co-crystal structures available for <b>WIZ</b> (upper row, 8TZX/9DJX) and <b>IKZF2</b> (middle and lower rows, 7U8F/7LPS), showing different proximities needed for developing covalent modalities to stabilise coresponding complexes.</font><br>

#### Covalent CRBN Binders and IKZF2 Degraders
<p style="text-align: justify;">
For the covalent CRBN binders (binary system), 36554 valid poses passed the initial docking and pharmacophore filter (<b>Video 13</b>). To streamline downstream QSAR and generative AI studies, these 3D poses were converted back to 2D canonical SMILES. I decided to remove stereochemical labels at this stage, as the chiral center at the C3 position of the glutarimide ring is known to racemise rapidly <i>in vivo</i>.
</p>
<video controls>
  <source src="photos_and_videos/video_13.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 13</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from binary co-crystallography (4TZ4/5V3O/8OJH).</font>
<br><br>
<p style="text-align: justify;">
The resulting 14042 unique molecules were filtered using three empirical criteria to ensure drug-likeness and minimise docking artifacts:

1. <b>Binding Score (AD4 covalent mode):</b> $< -10$ kcal/mol (to ensure the basic proximity needed).
2. <b>Molecular Weight (MW):</b> $< 500$ Da (to mitigate the inherent bias of docking algorithms toward larger molecules).
3. <b>Rotatable Bond Count (nRotB):</b> $< 7$ (to keep conformational stability while limit entropic penalties).

These rigorous filters refined the library from over 14000 candidates to a high-priority set of approximately 1500 compounds (<b>Figure 14</b>).
<img src="photos_and_videos/figure_14.png" alt="figure14" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 14</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 defined criteria for covalent CRBN binders.</font>
<br><br>
<p style="text-align: justify;">
For the IKZF2 covalent MG degraders, I adjusted the thresholds to reflect the increased complexity of the ternary interface: I loosened the MW and nRotB limits (< 550 Da and < 8) but tightened the binding score cutoff (< -11 kcal/mol). This ensured high complementarity within the ternary complex (<b>Video 15</b> & <b>Figure 16</b>). Approximately 1000 entries were prioritised, with several candidates showing excellent shape complementarity to the aromatic pharmacophores in reference, providing strong structural hypotheses for further medicinal chemistry optimisation.
</p>
<video controls>
  <source src="photos_and_videos/video_15.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 15</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from IKZF2 ternary complexes (7U8F/7LPS).</font>
<br><br>
<img src="photos_and_videos/figure_16.png" alt="figure16" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 16</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 tailored criteria for IKZF2 covalent MGs.</font><br>

#### Covalent WIZ Degraders
<p style="text-align: justify;">
Targeting CYS-11 in the CRBN-WIZ complex presented a greater challenge - Cysteine residues typically require different warheads than histidine, and as noted, the residue is located further from the binding interface. To focus the library as suggested by Gemini, I calculated the <b>Shortest Bonding Pathlength (SBP)</b>, the number of bonds on the 2D graph from the imide nitrogen to the electrophilic carbon, using a custom RDKit function. I restricted the library to precursors with a SBP >= 13 to ensure the linker was long enough to reach the target residue (<b>Figure 17</b>).
</p>
<img src="photos_and_videos/figure_17.png" alt="figure17" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 17</b>. For WIZ covalent degraders, a pre-docking process to focus the library with cysteine dependency. Those candidates with at least 13 SBP were chosen for subsequent covalent additions and ligand preparations.</font>
<br><br>
<p style="text-align: justify;">
Covalent docking against <b>WIZ</b> yielded several promising drug-like hits (<b>Video 18</b>). For this set, I tightened both the docking score (< -12.5 kcal/mol) and nRotB (< 7) to prioritise PROTAC-like molecules with high <b>"cooperativity"</b> and low internal strain (<b>Figure 19</b>). Interestingly, the top-scoring candidates predominantly featured cyanamide warheads, with fewer types of Michael acceptor. Many of these "winners" adopted L-shaped conformations, perfectly complementing the CRBN-WIZ interface. Again these designs are attached in my GitHub/HuggingFace repository for any potential development of interest.
</p>
<video controls>
  <source src="photos_and_videos/video_18.mp4" type="video/mp4">
</video>
<font size="2"><b>Video 18</b>. All ensemble docking poses that are selected to match the Glutarimide pharacophore in reference ligands from WIZ ternary complexes (8TZX/9DJX).</font>
<br><br>
<img src="photos_and_videos/figure_19.png" alt="figure19" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 19</b>. The distribution and cumulative plots of positive candidates enrichment passing 3 tailored criteria for WIZ covalent PROTACs.</font><br>

## QSAR Modelling
<p style="text-align: justify;">
Following the virtual screening results, I merged the prioritised covalent candidates with the original non-covalent CRBN binder pool to create an enriched, multi-modality database. To ensure high-quality leads, I applied a final filter using the <b>Quantitative Estimate of Drug-likeness (QED)</b> score, setting a threshold of > 0.5. This index balances several physicochemical properties, including Lipinski’s rules, to assess overall lead-likeness. This refined the covalent library to approximately 2500 compounds, a size comparable to the non-covalent pool (~4000 compounds) derived from open-source and Enamine databases (<b>Figure 20</b>).
</p>
<img src="photos_and_videos/figure_20.png" alt="figure20" width="480px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 20</b>. The distribution of chemical space between covalent and non-covalant classes for CRBN.</font>
<br><br>
<p style="text-align: justify;">
For the initial QSAR study, I focused on a <b>classification task</b>. Binary classification is commonly used in industrial drug discovery, particularly when dealing with early-stage, high-throughput data that may be inherently noisy before making any initial decision. Establishing a robust classifier serves as a prerequisite, providing a "prior" that guides subsequent regression models and generative AI toward higher-confidence predictions.
</p>

### Classification Task: Identifying Covalent CRBN Ligands
<p style="text-align: justify;">
While chemical identification is frequently used in toxicology to flag hazardous substances, I applied it here to distinguish covalent CRBN candidates using ML. Since I had previously annotated the common covalent warheads (examples in <b>Figure 7</b>), the purpose was to develop a model that captures the "chemist's intuition" — automating the recognition of these specific modalities within the CRBN-binding context.
</p>
<p style="text-align: justify;">
<b>In practical cheminformatics, success often depends on focusing on the specific chemical domain</b>. During data preparation, I initially experimented with including covalent molecules from other Enamine libraries unrelated to CRBN (lower left, <b>Figure 20</b>). However, I found that this "out-of-domain" data just acted as noise - Including positives for general covalency that were negative for CRBN binding confused the model, making it difficult for the machine to extract the specific structural patterns, whether through molecular fingerprints or graph-based matrices, that define the covalent CRBN chemical space.
</p>
<p style="text-align: justify;">
Unless you are pursuing a large-scale <b>transfer learning</b> approach (which would require a massive expansion of the "non-CRBN/non-covalent" negative space as shown in upper left, <b>Figure 20</b>), it is generally more effective to build a lean, focused model. From my personal experience working in the biotech, a model tailored specifically to the drug discovery project at hand is often more accurate and interpretable than a generalised one.
</p>

#### Classic Machine Learning with SVM and Tree Classifiers
<p style="text-align: justify;">
For QSAR classification tasks involving chemical spaces under 10000 compounds, classical machine learning approaches often provide superior robustness and generalisation. I initiated my study with a <b>Support Vector Machine (SVM)</b> utilising 8192-bit Morgan fingerprints (radius = 2, chirality ignored) based on a preliminary occupancy screening. The screening also confirmed that the majority of "on-bits" originated from the essential imide pharmacophore (<b>Figure 21</b>). This concentration of features is not a problem for SVMs, which rather excel at defining decision boundaries in high-dimensional hyperplanes based on sparse but critical features.
</p>
<img src="photos_and_videos/figure_21.png" alt="figure21" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 21</b>. The most common structures of on-bit from CRBN chemical space embedded with Morgan fingerprints (size 8192, radius 2, chirality ignored).</font>
<br><br>
<p style="text-align: justify;">
To ensure true generalisation, I utilised a <b>scaffold-based split</b>, distributing unique Bemis-Murcko scaffolds into training (80%, including 20% validation) and testing (20%) sets. This prevents "data leakage" where similar analogs appear in both sets, providing a more rigorous test of the model's predictive power.
</p>
<p style="text-align: justify;">
Following a hyperparameter grid search (optimising cost, gamma, and kernel types) under 5 fold of cross-validation, the SVM model achieved near-perfect performance on the test set, with both accuracy and the <b>Matthews Correlation Coefficient (MCC)</b> approaching 1.0. The MCC is particularly valuable here as it provides a balanced statistical measure of precision and recall for binary classification. To validate the model's logic, I analysed the top 25 feature importances (top, <b>Figure 22</b>). The results were highly interpretable: The SVM successfully prioritised bits corresponding to sulfonyl fluoride and acrylamide warheads.
</p>
<p style="text-align: justify;">
I subsequently evaluated two ensemble tree-based models which often used in my work: <b>Random Forest (RF)</b> and <b>eXtreme Gradient Boosting (XGBoost)</b>. After cross-validated tuning of hyperparameters such as maximum tree depth, number of estimators, and feature sub-sampling etc., both models performed exceptionally. The XGBoost model proved to be the most stable, placing significant weight on cyanamide-related bits within its decision trees (bottom, <b>Figure 22</b>).
</p>
<img src="photos_and_videos/figure_22.png" alt="figure22" width="720px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 22</b>. The importance plots for top features of Morgan fingerprint respectively interpreted from tuned SVM, RF and XGBoost models, to classify the covalent modality from others in CRBN chemical space.</font>
<br><br>
<p style="text-align: justify;">
Nevertheless, exhaustive grid searches are computationally expensive and time-consuming. To streamline the workflow of building ML model, I implemented <b>Bayesian optimisation</b> using the <b>Optuna</b> module (<b>Text 23</b>) following some tips given by my Claude agent. By iterating 100 times over just a few hours, the algorithm identified an XGBoost configuration that classified the entire test set correctly.
</p>

```python
#Tuning hyperparameters of XGBoost using Optuna based on Bayesian optimisation
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
<font size="2"><b>Text 23.</b> The Python code to tune hyperparameters of XGBoost classifier with Bayesian optimisation using optuna module.</font><br>

<p style="text-align: justify;">
This approach reminded me of <b>Markov Chain Monte Carlo (MCMC)</b> methods used for conformational searching in molecular modelling - Both aim to locate optima (or minima) within a complex landscape without requiring an exhaustive search of all possibilities. As a physical chemist doing interdisciplinary research, this highlights a core principle of data science and engineering I have learnt so far: <b>To find a global optimum, whether in a hyperparameter distribution or a molecular energy landscape, we do not always require <i>ab initio</i> physics for every trial. Instead, the synergy of sufficient high-quality data, fittable empirical paradigms (such as DFT, force-field potentials, or even just robust mathematical models), and sophisticated statistical methods can navigate us toward the "ground truth" much faster. This encloses a primary goal of AI for Science: Identifying the most efficient approximation that yields a viable solution.</b>
</p>

#### Classification via Graph Neural Networks (GCN, GAT, and GIN)
<p style="text-align: justify;">
To complement the classical ML models, I developed a deep learning pipeline using Graph Neural Networks (GNNs). Following some tutorials from DeepChem, TeachOpenCADD, and Maxime Labonne, I represented each molecule in my library as a graph at the beginning. Using <b>Thalidomide</b> as an example (<b>Figure 24</b>), the chemical structure is encoded into an adjacency matrix representing bonding connectivities (edges) between atoms (nodes). With DeepChem’s featuriser, I converted these structures into three sub-matrices: <b>node features</b>, <b>edge index</b>, and <b>edge features</b>. For this study, the edge features were dropped because the node features implicitly capture bonding environments and they would be updated and aggregated for the awareness of edge type in most standard message-passing algorithms as far as I know. Furthermore, since we are not predicting bond-specific properties or generating alternative bonds, simplifying the graph to a node-and-edge-index format reduces computational redundancy without sacrificing much accuracy.  
</p>
<img src="photos_and_videos/figure_24.png" alt="figure24" width="480px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 24</b>. The adjacent matrix of Thalidomide as a simply encoded 2D graph, and the actual object featurised by DeepChem module for this study.</font>
<br><br>
<p style="text-align: justify;">
Admittedly, deep learning is often viewed as a "black box" by many computational chemists including myself who was not educated professionally with advanced mathematics. Without a formal background in linear algebra, I used the recent Xmas holiday to familiarise myself with <b>PyTorch</b> and modularise the following workflow based on my software engineering experience and AI proficiency:
<br><br>
<b>1. Graph Featurisation, Collate, Scaffold-based Splitting of Training/Validation/Test Sets and Dataloader Preparation in Batch.</b><br>
<b>2. Epoch-based Training using Backpropagation with the Adam Optimiser and Binary Cross Entropy (BCE) loss for classification.</b><br>
<b>3. Regularisations including Dropout and Weight Decay to prevent overfitting on our relatively small dataset (< 10000).</b><br>
<b>4. Evaluation using MCC as the primary metric for binary classification performance.</b><br> 
</p>
<p style="text-align: justify;">
I evaluated three distinct architectures: <b>Graph Convolutional Network (GCN), Graph Isomorphism Network (GIN) and Graph Attention Network (GAT) (Text 25)</b>. Both GCN and GIN were inspired from TeachOpenCADD tutorial while GAT was proposed by my Gemini agent. While some architectural choices (such as layers and readout functions) might be refined further by a dedicated data scientist, I leaned on a recent industry insight from GSK: <b>In QSAR studies, GNN architecture is often less critical than rigorous hyperparameter optimisation and feature engineering</b> (DOIs in reference). With the deepchem graph featurised from RDKit canonical smiles string (default tautomer but ignoring chirality), I decided to focus on tuning hyperparameters in order to maximise model performances on the classification of CRBN ligand modalities.
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
<font size="2"><b>Text 25.</b> The code for 3 common GNN architectures in PyTorch, which were used for chemical classification based on DeepChem GraphData.</font><br>
<p style="text-align: justify;">
As shown in the grid search results (<b>Figure 26</b>), all three GNN models could identify covalent CRBN modulators with exceptional precision and recall (MCC > 0.95). Nevertheless, the GIN model demonstrated the most robust MCC stability across varying hyperparameters. By utilising Bayesian optimisation, an optimal GIN configuration was more quickly found (Hidden Dim: 16, Batch Size: 16, LR: 0.001) that achieved an MCC up to 0.98. <b>Obviously both classical ML and GNN approaches proved highly capable of handling this classification task to identify those covalent modalities in the CRBN chemical space. But can these models handle the regression modeling as well?</b>
</p>
<img src="photos_and_videos/figure_26.png" alt="figure26" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 26</b>. The hyperparameter screening result for 3 GNN models trained to make binary classification between covalent and non-covalent CRBN binders, evaluated by MCC on test set.</font><br>

### Regression Task on Electrophilicity
<p style="text-align: justify;">
In covalent drug discovery, quantifying reactivity is a primary challenge for medicinal chemists. While biophysical assays can measure kinetic parameters such as <b>k_inact/K_I</b> for detailed mechanistic study in the protein environment, high-throughput alternatives like the <b>Glutathione (GSH) reactivity assay</b> provide a shortcut to evaluate a molecule's propensity for the cysteine engagement. Computationally, this reactivity can be even roughly estimated through the lens of frontier molecular orbital (FMO) theory — specifically by calculating <b>HOMO</b> (Highest Occupied Molecular Orbital) and <b>LUMO</b> (Lowest Unoccupied Molecular Orbital) energies. Having previously annotated our CRBN chemical space into covalent and non-covalent classes, I set out to determine if these empirical labels could be characterised and quantified through rigorous electronic descriptors.
</p>

#### Quantum Chemical Calculations
<p style="text-align: justify;">
To calculate molecular electronic properties at scale, I instructed my AI agent to develop a workflow utilising a "conformationally dependent" statistical QM approach. The pipeline begins with stereo-isomers enumeration, <b>ETKDG (MMFF)</b> conformational sampling, followed by <b>xTB</b> geometry optimisation, and culminates in single-point energy calculations using the <b>UMA</b> (Universal Machine Learning Approximation) model. Final properties were derived through <b>Boltzmann averaging</b> over the resulting low-energy ensembles in vacuum (<b>Figure 27</b>). This semi-empirical approach serves as a pragmatic compromise for screening over 10000 hit candidates: It avoids the extreme computational cost of full DFT or MD simulations while maintaining a level of accuracy superior to classic functionals or force fields, thanks to the integration of atomic neural network potentials (NNP) - as supported by the study in my previous blog.
</p>
<img src="photos_and_videos/figure_27.png" alt="figure27" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 27</b>. The example to calculate some electronic descriptors for 2 distinct CRBN ligand modalities respectively based on a workflow of quick statistical quantum chemical computation.</font>
<br><br>
<p style="text-align: justify;">
Following the computational screening, a comparison of the electronic profiles between the covalent and non-covalent classes revealed statistically significant differences (p < 0.05 via Mann-Whitney U and t-tests). Covalent species generally exhibited lower LUMO energies, higher HOMO energies, and smaller HOMO-LUMO gaps (<b>Figure 28</b>). Furthermore, the distribution of the electrophilicity index (ω), calculated using the following relationship, was markedly higher for the covalent class:
</p>

$$\omega = \frac{(E_{H} + E_{L})^2}{4(E_{L} - E_{H})}$$

<img src="photos_and_videos/figure_28.png" alt="figure28" width="1080px" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;"/>
<font size="2"><b>Figure 28</b>. The distribution of HOMO, LUMO, gap energies and electrophilicty index (ω) respectively in covalent and non-covalent classes of CRBN chemical space.</font>
<br><br>
<p style="text-align: justify;">
Despite these trends, molecular-level QM features alone are often insufficient for high-confidence classification of covalency - A finding consistent with research from <b>Bayer</b> and <b>Boehringer Ingelheim</b> (DOIs in reference). True predictive power likely requires fragment-specific descriptors, such as <b>Fukui indices</b> on the warhead atoms and further calculated <b>transition-state activation energies</b> for the nucleophilic attack. However, because the LUMO energy is the primary orbital for accepting nucleophilic electrons and its distribution in our dataset closely follows a <b>Gaussian-like</b> profile (second plot, <b>Figure 28</b>), I selected it as the target variable for our regression modeling.            
</p>

#### Benchmarking ML Models for LUMO Prediction
<p style="text-align: justify;">
The regression modelling workflow followed a similar logic to the previous classification task, with a critical difference in the loss function: <b>Mean Squared Error (MSE)</b> was implemented to fit and predict continuous energy values. Another significant adjustment was made regarding molecular featurisation. Since our target, QM-calculated LUMO energies, is derived from conformational analysis of specific stereoisomers, this time I incorporated <b>stereochemical features</b> into both the 1D Morgan fingerprints and the 2D graph matrices. By including chirality, I aimed to reduce "structural noise" and increase physical relevance, allowing the models to better recognise the subtle patterns that govern 3D-dependent quantum chemical properties. 
</p>
<p style="text-align: justify;">
Using the same scaffold-based train/test split and a combination of Grid Search and Bayesian optimisation, I benchmarked the regression performance across 6 pre-trained and tuned architectures again: <b>SVM, RandomForest, XGBoost, GCN, GAT and GIN (Table 29)</b>.
</p>

| Regression Models | Molecular Features | Test MSE | Test MAE | Test R2 | Running Time | Model Size |
| :---: | :---: | :---:| :---: | :---: | :---: | :---: |
| SVM | Morgan - 8192 bits, 2 radius & include chirality | 0.0408 | 0.1409 | 0.7269 | Slow | .pkl file ~ 600MB  |
| RandomForest | Morgan - 8192 bits, 2 radius & include chirality | 0.0530 | 0.1613 | 0.6454 | Medium | .pkl file ~ 100MB |
| XGBoost | Morgan - 8192 bits, 2 radius & include chirality | 0.0414 | 0.1452 | 0.7232 | Fast | .pkl file ~ 500KB |
| GCN | Graph (exclude edge features) | 0.0497 | 0.1716 | 0.6677 | Fast (GPU) | .pth file < 10KB |
| GAT | Graph (exclude edge features) | 0.0476 | 0.1656 | 0.6818 | Fast (GPU) | .pth file ~ 12KB |
| GIN | Graph (exclude edge features) | 0.0409 | 0.1447 | 0.7266 | Fast (GPU) | .pth file ~ 12KB |

<font size="2"><b>Table 29.</b> Benchmark performances across 3 classic ML and 3 GNN models for the prediction of QM-calculated LUMO energies within our CRBN chemical space. (ps. Results are subject to minor stochastic variation based on the random seed)</font><br>  

<p style="text-align: justify;">
The results highlight an interesting trend: For our focused CRBN dataset, the graph models showed no significant improvement over classical ML models in terms of <b>R2 score (coefficient of determination)</b>. Both <b>SVM</b> and <b>GIN</b> regressions were optimised to produce a strong fit (Test R2 up to 0.72) on the QM-calculated LUMO values. However, The GIN architecture offered a distinct engineering advantage: The training was significantly faster due to GPU acceleration, and the final model deployment is more efficient, requiring only the saved parameter dictionary (remember the SVM utilise RBF kernel). Meanwhile, <b>XGBoost</b> also proved to be a standout performer - high stability, minimal overfitting, lightweight storage as well as interpretable reasoning - making it an excellent alternative for rapid re-usage in production pipelines.
</p>                           
