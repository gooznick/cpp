from string import Template
import subprocess

ccode_template = "$VISIBILITY int foo(){ return 4;}"
code_visibilities = {"no attr":"", "attr def":'__attribute__ ((visibility ("default")))', "attr hid":'__attribute__ ((visibility ("hidden")))'}

gcc_template = "g++ foo.cpp -ofoo.so -shared $GVISIBILITY $LVISIBILITY"
gcc_visibilities = {"no -f":"", "-f def":'-fvisibility=default', "-f hidd":'-fvisibility=hidden'}

with open("global.vs", "w") as fid:
    fid.write("{global:*;};")
with open("local.vs", "w") as fid:
    fid.write("{local:*;};")

linker_visibilities = {"no script":"", "script local":'-Wl,--version-script=local.vs', "script global":'-Wl,--version-script=global.vs'}

results = {}
for lvis_name, lvis in linker_visibilities.items():
    for gvis_name, gvis in gcc_visibilities.items():
        for cvis_name, cvis in code_visibilities.items():
            ccode = Template(ccode_template).substitute(VISIBILITY=cvis)
            with open("foo.cpp", "w") as fid:
                fid.write(ccode)

            gcc = Template(gcc_template).substitute(GVISIBILITY=gvis, LVISIBILITY=lvis)

            out = subprocess.check_output(gcc, shell=True)
            assert not out

            foo_export = subprocess.check_output("nm foo.so | grep foo", shell=True, encoding='UTF-8')
            res = "X"
            if " T " in foo_export:
                res ="T"
            elif " t " in foo_export:
                res = "t"

            results[(cvis_name, lvis_name, gvis_name)] = res
import pprint
pprint.pprint(results)