Create Environment
'''bash
conda create -n score python=3.7 -y
'''

Activate new environment
'''bash
conda activate score
'''

Create and Install requirements.txt file  
'''bash
pip install -r requirements.txt
'''

git init

dvc init 

dvc add data_given/Admission_Prediction.csv

