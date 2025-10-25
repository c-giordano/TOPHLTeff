# Set up enviroment
- ``` bash setEnv.sh ```
- ```voms-proxy-init --voms cms```



# Get input nanoAOD list
- ```bash generateInputList.sh```
- In the bash script, add commands such as
- ```python3 generateInputList.py --tag <2025C, 2025D, 2025D...>```

# Skim nanoAOD
- Test locally 
   ```python3 skimNano.py```
- Submit jobs
    ```bash subJobs.sh```
    That submits commands such as
    ```python3 subJobs.py --tag <EGamma2025C> --jobVersion <outut_directory>```
    - check job

# Plot HLT efficiency
- Generate HLT efficieny hists
```bash plotHLT.sh```
```python3 plotHLT.py```

- Plot efficieny 
```python3 plotEff.py```


# To do
- [] Make the workflow more automated 
- [] Setup enviroment properly in CenOS9
- [] Intergate nanoAOD tool data format for object selection
- [] Check the btag change during data taking
