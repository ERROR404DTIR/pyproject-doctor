#!/usr/bin/env python3
"""Static pyproject.toml checker (Python 3.11+)."""
import argparse,json,tomllib
from pathlib import Path
def audit(data,root):
 issues=[]
 def add(level,msg):issues.append({"level":level,"message":msg})
 project=data.get("project",{});build=data.get("build-system",{})
 if not build:add("error","missing [build-system] table")
 else:
  if not build.get("requires"):add("error","build-system.requires is empty")
  if not build.get("build-backend"):add("error","build-system.build-backend is missing")
 if not project:add("warning","missing [project] metadata table")
 if project:
  for key in ("name","version","description"):
   if not project.get(key):add("warning",f"project.{key} is missing")
  readme=project.get("readme")
  if isinstance(readme,str) and not (root/readme).is_file():add("error",f"README file not found: {readme}")
  elif isinstance(readme,dict) and readme.get("file") and not (root/readme["file"]).is_file():add("error",f"README file not found: {readme['file']}")
  if "requires-python" not in project:add("warning","requires-python is not declared")
  deps=project.get("dependencies",[])
  if not isinstance(deps,list):add("error","project.dependencies must be an array")
  else:
   for i,d in enumerate(deps):
    if not isinstance(d,str) or not d.strip():add("error",f"dependency {i} is empty or invalid")
  scripts=project.get("scripts",{})
  if not isinstance(scripts,dict):add("error","project.scripts must be a table")
  else:
   for name,target in scripts.items():
    if not isinstance(target,str) or ":" not in target:add("warning",f"script {name} should use module:function syntax")
 return {"issues":issues,"errors":sum(x["level"]=="error" for x in issues),"warnings":sum(x["level"]=="warning" for x in issues)}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("file",nargs="?",default="pyproject.toml",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args()
 try:data=tomllib.loads(a.file.read_text(encoding="utf-8"))
 except (OSError,tomllib.TOMLDecodeError) as e:p.error(str(e))
 r=audit(data,a.file.resolve().parent)
 if a.json:print(json.dumps(r,indent=2));return
 print(f"Errors: {r['errors']} · Warnings: {r['warnings']}")
 for x in r["issues"]:print(x["level"].upper()+": "+x["message"])
 if not r["issues"]:print("Project metadata looks healthy.")
if __name__=="__main__":main()
