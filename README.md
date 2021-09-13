Create Environment
```bash
conda create -n score python=3.7 -y
```

Activate new environment
```bash
conda activate score
```

Create and Install requirements.txt file  
```bash
pip install -r requirements.txt
```
```bash
git init
```

```bash
dvc init 
```

```bash
dvc add data_given/Admission_Prediction.csv
```

```bash
git add . && git commit -m "first commit"
```

```bash
git remote add origin https://github.com/Pooja1994Profile/mlflow_dvc_demo.git
git branch main
git push origin main
```
Tox Commands
```bash
tox
```
For rebuilding tox
```bash
tox -r
```

pytest command
```bash
pytest -v
```

Setup command
```bash
pip install -e .
```

Build own package commands (.tar file)
```bash
python setup.py sdist bdist_wheel
```