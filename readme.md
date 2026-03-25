# Set executables 
Not necessary, but makes life easier
```chmod +x <bash_script>.sh```

To be done on the following scripts:

```setEnv.sh```/```copy_proxy.sh```/```generateInputList.sh```/```subJobs.sh```/```plotHLT.sh```/```plotEff.sh```



# Set up enviroment
Run every time:
- ```./setEnv.sh ```
- ```./copy_proxy.sh```

Note: modify the proxy directory in ```copy_proxy.sh```


# Get input nanoAOD list
To run the script
- ```./generateInputList.sh```

In the executable, add commands such as
- ```python3 generateInputList.py --tag <Muon2025C, Muon2025D, EGamma2025D...>```

Now fully automated, creates the query command on DAS for you.

Parser now selects reco & tier (useful for MC implementation).

# Skim nanoAOD
- Test locally: ```python3 skimNano.py```
- Submit jobs
  Run: ```./subJobs.sh```
  
That submits commands such as ```python3 subJobs.py --tag <EGamma2025C> --jobVersion <outut_directory>```

Note: in ```subJobs.py```, specify the user and the eos directory in the functions ```make_out_dir``` & ```write_sub_file```

The outDir mechanism is a bit redundant, it could be improved.

Check ```skimNano.py``` & ```subJobs.py``` for details of the arguments and the preselection cuts

# Obtain and plot HLT efficiencies

Divided in 2 steps ran by 2 separate scripts

## plotHLT.py

Deceiving name, it actually generates HLT efficiency hists and saves them in a ROOT file

```./plotHLT.sh``` submits commands like ```python3 plotHLT.py --inputDir /eos/user/<...> --era <e.g. 2025E, 2024I...> --outVersion <subdir_name> --offilne <offline_cut>``` and saves the efficiency file as ```/eos/user/<...>/result/<subdir_name>/eff.root```

There are more parse arguments relative to whether or not one is running the hadronic or leptonic analysis, check the bash files or scripts for details.

## plotEff.py
This one actually plots the efficiencies, it is ran by the relative bash script and the parser is pretty self-explanatory

Note: the ```specialEra``` argparser can be repurposed every time there is a specific requirement with plotting the runs in a single era separately.

The run-based selection must be ran in the previous step of the analysis (```plotHLT.py```), by using the ```otherCuts``` argument.



# To do
- [OK] Make the workflow more automated
   - [OK] Missing autom of plotHLT.py
- [] Intergate nanoAOD tool data format for object selection
- [] Check the btag change during data taking
