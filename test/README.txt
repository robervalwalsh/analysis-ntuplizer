== Submiting to crab using the crab utilities ==

Examples of job submission:

# Run2018ABC ReReco \
crab_submit.py ntuplizer \
-c ntuplizer_102X_2018_rereco17Sep2018ABC-v3.py \
-f samples/data/Run2018/JetHT_ReReco_17Sep2018.txt \
-l Run2018 \
--submit


# Run2018D PromptReco \
crab_submit.py ntuplizer \
-c ntuplizer_102X_2018_promptreco2018D-v3.py \
-f samples/data/Run2018/JetHT_PromptReco_2018D.txt \
-l Run2018 \
--submit
