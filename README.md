############
# InfoGene #
#############

InfoGene is a Django web app which allows users to be able to search and receive information about human genes.

Gene searches can be directly using the HGNC-approved gene symbol or via the HGNC ID. 

Information which is obtained in the form of a 'GeneRecord' are listed below: 
• HGNC-approved gene symbol
• HGNC ID
• Approved gene name
• Previous gene symbols
• Previous gene names
• Gene aliases/synonyms
• MANE Select transcript
• MANE Plus Clinical transcripts


##############################
# Requirements & Data Source #
##############################

Prior to installation, ensure 'Anaconda' or 'Miniconda' is installed

This app does not use a typical Django database therefore, a download of the dataset (hgnc_complete_set.txt) is required to allow fast lookup of HGNC genes. Instuctions are supplied in the 'Installation' section below.

In future versions, a dataset should be integrated within the application so amanual download will no longer be needed. However, doing this will mean that the app will require regular updates to reflect the regular updates from the datasource (https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt).

################
# Installation #
################

### 1. Clone the Repo.
Clone the InfoGene repository to your local machine using the following command: 

```bash
git clone https://github.com/Nathania-K/InfoGene.git
cd InfoGene
```

### 2. Create Conda environment.

From the project's root directory, create the environment using the 'environment.yml':
         
```bash
conda env create -f environment.yml
```

(This provides the required python and pip to be installed.)

### 3. Activate Conda environment.

Activate the newly made conda environment using:
        
```bash
conda activate InfoGene
```

(you can verify which conda environments are available using `conda env list`.)

### 4. Install InfoGene app and dependencies in editable mode.
        
With the conda environment active, install dependencies using:
       
```bash
pip install -e .
```

(Installs app and pinned dependencies from the requirements.txt file)

### 5. Download HGNC dataset.

The 'Data' directory and HGNC Data Source are not included wihtin the application and therefore will require creation and download. To do this, enter the following commands from the project root.

```bash
mkdir -p Data

curl --fail --location --show-error \
  --output "Data/hgnc_complete_set.txt" \
  "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt"
```

### OPTIONAL. Check that InfoGene and associated dependencies are installed using:
    
```bash
python manage.py check
pip check
python -m django --version
python -m pytest --version
```

Expected outputs should report Danjo version at '6.0.5' and pytest at '9.0.3'. Successful pip check should show:

```text 
No broken requirements found.
System check identified no issues
```
###################
# Running the App #
###################

Once installation is complete, run the app by enter the following command from the project root:

```bash 
python manage.py runserver
```
Then open the Open http://127.0.0.1:8000/ in a web browser by holding the command button and clicking on the link.

To exit the session, press `Ctrl+c` within the terminal

#######################
# Lightweight Dataset #
#######################

Unlike other Django applications, this app does not use a database, instead InfoGene will read the .txt file in 'Data/hgnc_complete_set.txt', select the required fields and generates Python dictionaries which can be searched via a HGNC gene symbol or ID. The app will return the relevant 'GeneRecord' information.

###################
#  Running Tests  #
###################

To run the tests within the 'Tests' folder use the following command from the project root:

```bash 
python -m pytest
```

#####################
# Coverage Reports  #
#####################