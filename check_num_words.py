import pandas as pd

boi = pd.read_csv("./distrib_boilerpipe")
bs4 = pd.read_csv("./distrib_bs4")
jus = pd.read_csv("./distrib_justext")

print "Metric, Bs4, Boi, jus"
for col in ["words", "sentences_c", "sentences_nc"]:
    print "%s, %.1f (%.1f), %.1f (%.1f), %.1f (%.1f)" % (col, bs4[col].mean(), bs4[col].std(),\
                                                              boi[col].mean(), boi[col].std(),\
                                                              jus[col].mean(), jus[col].std())

print "In the final text, sentence_c is the LONG sentence version (no full stops added) while sentence_nc is the SHORT sentence version (full stops added whenever it is missing)"

