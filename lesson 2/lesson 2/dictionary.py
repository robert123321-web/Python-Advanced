numrat = {
          "KS":"+383",
          "IT" : "+35",
          "AL" : "+355"
           }

kosova = numrat["KS"]
print   (numrat)
print   (numrat["AL"])

numrat["KS"]= "+299"

print (numrat["KS"])

del numrat ["AL"]

print (numrat)


keys = numrat.keys()
vlerat = numrat.values()
print(keys)
print(vlerat)