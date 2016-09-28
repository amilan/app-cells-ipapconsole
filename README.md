
Ipapconsole
-----------

Ipapconsole is an interactive Icepap client build on top of IPython.


How to use it
-------------
Once it's installed you just need to type in a terminal:

```
ipapconsole
```

or use directly the ipython profile:

```
ipython --profile=ipapconsole
```

Notes extracted from code
-------------------------
```
# ALL THIS INFO IS IN RT 13748
# https://rt.cells.es/Ticket/Display.html?id=13748
#
# IT WOULD BE VERY USEFUL TO HAVE SOME MAGIC COMANDS TO:
# - SAVE POSITION REGS
# - COMPARE THEM
# - AND RESET THEM IF THEY DIFFER (USING A CONFIRMATION I/O OPERATION)
#
# THE IDEA WOULD BE TO CONVERT THE OUTPUT OF THE FOLLOWING PROCEDURE
# AS A DICTIONARY (using wro), RETURN IT, AND BE ABLE TO DO COMPARISONS
#
# ANOTHER FEATURE TO BE CHECKED AFTER AN UPGRADE IS THE DISDIS STATUS

#for d in range(1,7):
#    print('--------------------------------------------------')
#    wr $d:?indexer
#    wr $d:?cfg possrc
#    wr $d:?cfg tgtenc
#    for reg in ['','INDEXER','ENCIN','INPOS','ABSENC','MOTOR','TGTENC','SHFTENC']:
#        wr $d:?pos $reg
#        wr $d:?enc $reg
#        print('--------------------------------------------------')
```
