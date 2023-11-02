# import os
import yaml
from yaml import CLoader, CDumper
# from typing import Any


# def load_log(log_file: str, all: bool = True) -> list[list[Any]]:
#     yaml_docs: list[list[Any]] = []
#     with open(log_file, "r") as file:
#         yaml_docs2: list[Any] = []
#         yaml_src = ""
#         dist_start = False
#         record_start = False or all
#         for line in file:
#             if not record_start:
#                 if "===== DaCapo 23.9-RC3-chopin " in line:
#                     if "starting =====" in line:
#                         record_start = True
#                     elif "PASSED in " in line:
#                         record_start = False
#                 continue
#             if "@@ FRAGMENTATION DISTRUBUTION - Full" in line:
#                 if len(yaml_docs2) > 0:
#                     yaml_docs.append(yaml_docs2)
#                 yaml_docs2 = []
#             elif "@@ FRAGMENTATION DISTRUBUTION - RC" in line:
#                 dist_start = "End" not in line
#                 if "End" in line:
#                     yaml_docs2.append(yaml.safe_load(yaml_src))
#                     yaml_src = ""
#             elif dist_start:
#                 yaml_src += line
#     if len(yaml_docs2) > 0:
#         yaml_docs.append(yaml_docs2)
#     return yaml_docs


# def load_logs(log_dir: str, all: bool = True) -> dict[str, list[list[Any]]]:
#     data: dict[str, list[list[Any]]] = {}
#     for file in os.listdir(log_dir):
#         path = os.path.join(log_dir, file)
#         if os.path.exists(path) and os.path.isfile(path) and path.endswith(".log"):
#             print(f" - load {file}")
#             docs = load_log(path, all=all)
#             bench = file.split(".")[0]
#             if len(docs) > 0:
#                 data[bench] = docs
#                 print(f" - load {file} DONE")
#             else:
#                 print(f" - load {file} SKIP")
#     return data


# d = load_log("/home/wenyu/mmtk-dev/evaluation/results/log/lxr-frag-dist-boar-2023-10-29-Sun-050606-deflated/jme.1989.58.jdk-lxr.lxr.common3.tph.dacapochopin-rc3.log",False)
# print(d)
# data = load_logs("/home/wenyu/mmtk-dev/evaluation/results/log/lxr-frag-dist-boar-2023-10-29-Sun-050606-deflated")
# print(data.keys())

# with open("/home/wenyu/mmtk-dev/evaluation/results/log/lxr-frag-dist-boar-2023-10-29-Sun-050606-deflated/frag-dist.yml", "w") as outfile:
#     yaml.dump(data, outfile)
# scripts/lxr-dacapo-frag-dist.ipynb
print('loading...')
with open("./_frag-dist-raw.yml", "r") as infile:
    data = yaml.load(infile, Loader=CLoader)
print('writing...')
with open("./_frag-dist.yml", "w") as outfile:
    yaml.dump(data, outfile, width=float("inf"), default_flow_style=None, Dumper=CDumper)
