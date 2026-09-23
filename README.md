############
# InfoGene #
#############

InfoGene is a Django web app which allows users to be able to search and receive information about human genes.

Gene searches can be directly using the HGNC-approved gene symbol or via the HGNC ID. 

Information which can be obtained are listed below: 
• HGNC-approved gene symbol
• HGNC ID
• Approved gene name
• Previous gene symbols
• Previous gene names
• Gene aliases/synonyms
• MANE Select transcript
• MANE Plus Clinical transcripts


################
# Requirements #
################

Prior to installation, ensure 'Anaconda' or 'Miniconda' is installed

################
# Installation #
################

### 1. Create Conda environment

From the project's root directory, create the environment using the 'environment.yml':
         
```bash
conda env create -f environment.yml
```

(This provides the required python and pip to be installed.)

### 2. Activate Conda environment

Activate the newly made conda environment using:
        
```bash
conda activate InfoGene
```

(you can verify which conda environments are available using `conda env list`.)

### 3. Install InfoGene app and dependencies in editable mode.
        
With the conda environment active, install dependencies using:
       
```bash
pip install -e .
```

(Installs app and pinned dependencies from the requirements.txt file)

### OPTIONAL. Check that InfoGene and associated dependencies are installed using:
    
```bash
python -m django --version
python -m pytest --version
pip check
```

Expected outputs should report Danjo version at '6.0.5' and pytest at '9.0.3'. Successful pip check should show:

```text 
No broken requirements found.
```
