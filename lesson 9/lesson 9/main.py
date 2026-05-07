from KerriElektrik import KerriElektrik
from kerri import Kerri


kerri1 = Kerri("tesla","2000","sdf")
kerri1.info()

kerri2 = KerriElektrik("byd",2025,"plus","85%")
kerri2.info()

kerri2.mbusheBaterin()
kerri2.rritjeShpejtesise()
kerri2.nalu()
