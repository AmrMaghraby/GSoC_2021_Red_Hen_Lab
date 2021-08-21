# ColorFilmCutDetection
[![Status](https://img.shields.io/badge/status-active-success.svg)]() 
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

## About
This is a CLI tool to detect cuts in color video films, especially old films with noise frames.
It works by taking input video and pass the frames to pyScene tool to analyze it and extract the scenes start time and end time in CSV and JSON file describing details of each scene.
It also outputs in anther CSV file cuts numbers with the corrosponding frame number. This tool was produced for [Google Summer Code 2021](https://amrmaghraby.github.io/MyJourneyGS0C2021/) with RedHenLabs and Media Ecology Project. Mentors for this project are: [Mark J. Williams](https://faculty-directory.dartmouth.edu/mark-j-williams), [John P. Bell](https://itc.dartmouth.edu/people/john-p-bell), [Vera Tobin](https://cognitivescience.case.edu/faculty/vera-tobin/) and [Ahmed Ismail](https://ai-zahran.github.io/)

## Getting Started


### Prerequisites
You need Python 3.9 to run this tool

### Installation
For installing this tool with our pipeline, follow the steps below :
1. Clone this repository `git clone https://github.com/AmrMaghraby/GSoC_2021_Red_Hen_Lab`
2. cd phase 2 
3. Install `requirements.txt` file by `pip install requirements.txt`

Now we are ready for testing our pipeline.

#### Testing on Case HPC
By the help of [Ahmed Ismail](https://ai-zahran.github.io/) I have uplaoded the image successfully on HPC and resolve dependency issues.

Now we can test the pipeline by follwoing the steps below :

1. Module load singularity
2. singularity run GSOC.img video_dir
   
   In case you want JSON output describing each scene then add --output-json like the following example 
   
   For example: singularity run GSOC.img ‘/mnt/rds/redhen/gallina/home/aam193/GSOC2021_Detect_Video_Cuts/306-706.mp4’ --output-json
   
   In case you want CSV output contains cut num and cut frame in single file and output in anther file scene num and start time and end time for each scene 
   then add --output-csv like the following example 
   
   For example: singularity run GSOC.img ‘/mnt/rds/redhen/gallina/home/aam193/GSOC2021_Detect_Video_Cuts/306-706.mp4’ --output-csv

## Usage

To run the tool on local machine, follow the steps in the **Installation** section.
After setting up the environment, Run :
```bash
python outputScriptGenerator.py `<path/to/video>` --output-json --output-csv
```
- `<path/to/video>` - Path of target video path
- `<result_output_format>` - Output format of the result. Available formats : `cuts` - CSV file containing frame index of cuts and frame num of such cut and - JSON format containing start time and end time of scenes in Media Ecology Project annotation format.

  To get help about the syntax format : `python main.py --help`
  
## Singularity Usage
To access Singularity image of this tool in the CWRU HPC environment :
1. Connect to CWRU VPN
2. ssh into HPC
```bash
ssh abc123@rider.case.edu
```
3. Navigate to this project folder directory
```bash
cd /mnt/rds/redhen/gallina/home/sxg1139/GSOC_SINGULARITY
```
4. Request a GPU node for computation
```bash
srun -p gpu -C gpu2080 gpu=gres:1 --pty bash
```
5. Load Singularity into HPC environment
```bash
module load singularity/3.7.1
```
6. Run the image
```bash
singularity run -B <path/to/video> -B <path/to/model> filmedit.img --vidpath <path/to/video> --modpath <path/to/model> 
```
- `<path/to/video>` denotes the absolute input video path
- `<path/to/model>` denotes the absolute path to trained model. If empty, the tool will tun on pre trained model.

# Dataset

By the help of [Mark J. Williams](https://faculty-directory.dartmouth.edu/mark-j-williams) and [John P. Bell](https://itc.dartmouth.edu/people/john-p-bell) and there students from Dartmouth college and University of Chicago.
Special Thanks to the following students for their efforts in annotating the datasets:
- Kevin Chen (Dartmouth College)
- Elijah Czysz (Dartmouth College)
- Maria Graziano (Dartmouth College)
- Noah Hensley (Dartmouth College)
- Emily Hester (Dartmouth College)
- Adithi Jayaraman (Dartmouth College)
- Yangqiao Lu (University of Chicago)
- Momina Naveed (Dartmouth College)
- Frandy Rodriguez (Dartmouth College)
- Ileana Sung (Dartmouth College)

The following screenshot contains sample of the dataset provided by our mentors and their students which contains three different types of annotations soft cuts, hard cuts and multiframe cuts(hard cuts that will be transformed to mutltiframe cuts due to codec problem).
![screenshot of dataset](https://raw.githubusercontent.com/AmrMaghraby/GSoC_2021_Red_Hen_Lab/main/Contributors/Screenshot%20from%202021-08-21%2017-00-56.png)


# Future Work

1- Training
Now we can train the model to get the best thrshold required by pyScene, but unfourtanley we didnot have time to test everything so as future work we need to investigate more in it. In order to run the training pipeline follow the follwoing the steps below :

1. Module load singularity
2. singularity shell GSOC.img
3. source activate pyscene_env
4. python getOptimalThreshold.py ‘path/to/directory/contain/mp4/files’ ‘path/to/directory/contains/test/csv/files/to/calculate/accuracy’

Again thanks to [Ahmed Ismail](https://ai-zahran.github.io/) for suggesting Bayesain optimizer method which helped in finding the optimal threshold to be used in pyScene

2- Classify soft cuts and hard cuts in an efficient way baased on the output of pyScene.
