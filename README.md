############
# InfoGene #
#############

[![codecov](https://codecov.io/gh/Nathania-K/InfoGene/branch/main/graph/badge.svg?token=BL39YUB86L)](https://codecov.io/gh/Nathania-K/InfoGene)

InfoGene is a Django web application which allows users to be able to search and receive information about human genes.

Searches can be directly using the HGNC-approved gene symbol or via the HGNC ID. 

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

InfoGene can be installed using either:

1. Conda (for local use).
2. Docker (containerised execution)

For Conda, prior installation of `Anaconda` or `Miniconda` is required.
For Docer, prior installation and running of `Docker Desktop` or `Docker Engine` is required.

This app does not use a typical Django database, therefore, a download of the dataset (hgnc_complete_set.txt) is required to allow fast lookup of HGNC genes. Instructions are supplied in the 'Installation' section below.

In future versions, a dataset should be integrated within the application so manual download will no longer be needed. However, doing this will mean that the app will require regular updates to reflect the regular updates from the datasource (https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt).

######################
# Conda Installation #
######################

### 1. Clone the Repo.
Clone the InfoGene repository to your local machine using the following command: 

```bash
git clone https://github.com/Nathania-K/InfoGene.git
cd InfoGene
```

### 2. Create Conda environment.

From the project's root directory, create the environment using the `environment.yml`:
         
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
python -m pip install -e .
```

(Installs app and pinned dependencies from the requirements.txt file)

### 5. Download HGNC dataset.

The 'Data' directory and HGNC Data Source are not included within the application and therefore will require creation and download. To do this, enter the following commands from the project root.

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

Expected outputs should report Django version at '6.0.5' and pytest at '9.0.3'. Successful pip check should show:

```text 
No broken requirements found.
```
Successful `python manage.py check` should show:

```text
System check identified no issues
```
###################
# Running the App #
###################

Once installation is complete, run the application from the project root using the following command:

```bash 
python manage.py runserver
```
Then open http://127.0.0.1:8000/ in a web browser.

To exit the session, hold `Ctrl+c` within the terminal.

#######################
# Docker Installation #
#######################

### 1. Build InfoGene image.
Build InfoGene's image using the following command from the porject root:
(Note: the docker image repo names should be lowercase): 

```bash
docker build -t infogene .
```

### 2. Create dataset volume.

Enter the following command on your terminal to create InfoGene's dataset volume:
         
```bash
docker volume create infogene-data
```

### 3. Download dataset to the volume.

After volume creation, download the dataset into the infogene-data volume:
         
```bash
docker run --rm \
  --mount type=volume,source=infogene-data,target=/app/Data \
  infogene \
  python -c "import os, urllib.request; url='https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt'; final='/app/Data/hgnc_complete_set.txt'; temporary=final+'.part'; urllib.request.urlretrieve(url, temporary); os.replace(temporary, final)"
```
(the dataset is downloaded to the volume wihtin a temporary container after the image has been created as the download requires InfoGene's Python. The temporary container is removed once the download is complete and the volume is retained, ready for mounting).

### 4. Run the container.

Once the dataset download is complete, enter the following command to run the container:
         
```bash
docker run --rm \
  -p 8000:8000 \
  --mount type=volume,source=infogene-data,target=/app/Data,readonly \
  infogene
```
If you wish to confirm that the container is running, use the following command:

```bash
docker ps
```

`infogene` should be displayed in the terminal as running.

The port used for this application is 8000.

### 5. Run the container.

Once the container is running, open the InfoGene app by entering `http://localhost:8000/` in the terminal. 

To stop the container, hold `Ctrl+c` within the terminal.
The `infogene-data` volume will persist after the container stops.

#######################
# Lightweight Dataset #
#######################

Unlike other Django applications, this app does not use a database, instead InfoGene will read the .txt file in 'Data/hgnc_complete_set.txt', select the required fields and generates Python dictionaries which can be searched via a HGNC gene symbol or ID. The app will return the relevant 'GeneRecord' information.

### Please note
The hgnc_complete_set.txt datasource is regularly updated from the third party therefore, downloads of the dataset will be subject to during installation may differ if the data is updated post installation. 

##########################
#  Running Tests (Conda) #
##########################

To run the tests within the 'Tests' folder, use the following command from the project root:

```bash 
python -m pytest
```
###########################
#  Running Tests (Docker) #
###########################

To run the tests within the 'Tests' folder, use the following command from the project root:

```bash 
docker run --rm \
  --mount type=volume, source=infogene-data, target=/app/Data,readonly \
  infogene \
  python -m pytest
```

#####################
# Coverage Reports  #
#####################

To generate coverage reports, use the following commands: 

```bash
pytest -m --cov=InfoGene --cov-report=term-missing --cov-report=html
```

Then open the coverage reports using:

```bash
open htmlcov/index.html
```

(Opens a webpage where coverage reports can be viewed).

