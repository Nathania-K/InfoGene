.________________________________________________________________________________.
| ||======||  ||\   || ||====||  ||======|| ||=====|| ||====|| ||\   || ||====|| |
|     ||      || \  || ||        ||      || ||        ||____   || \  || ||____   |
|     ||      ||  \ || ||====||  ||      || ||   ==|| ||       ||  \ || ||       |
| ||======||  ||   \|| ||        ||======|| ||=====|| ||====|| ||   \|| ||====|| |
|________________________________________________________________________________|

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
    
``bash                                  Expected Output
python -m django --version      ---> "$ python -m django --version 6.0.5"
python -m pytest --version      ---> "$ python -m pytest --version pytest 9.0.3"
pip check                       ---> "No broken requirements found."    
pip show InfoGene               ---> "$ pip show InfoGene
```                                     Name: InfoGene
                                        Version: 0.1.0
                                        Summary: A web application for searching HGNC gene information
                                        Home-page:
                                        Author:
                                        Author-email: Nathania Kulkarni <nathania.kulkarni@postgrad.manchester.ac.uk>
                                        License:
                                        Location: /Users/<name>/miniconda3/envs/InfoGene/lib/python3.12/site-packages
                                        Editable project location: <selected_path>/InfoGene
                                        Requires: Django, pytest, pytest-cov, pytest-django
                                        Required-by:                           "
