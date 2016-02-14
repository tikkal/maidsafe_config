#!/usr/bin/python

import subprocess
import sys

def cargo_exec(project, cargo_args):
  # Use Popen to set directory in project
  p = subprocess.Popen(cargo_args, cwd=project)
  p.wait()
  
def cargo_test(project, use_mock_routing=False):
  cargo_args = ["cargo", "test"]

  # Add mock routing feature if specified
  if (use_mock_routing): 
    cargo_args.extend(["--features", "use-mock-routing"])

  cargo_exec(project, cargo_args)

def do_runner(cleaning=False, cloning=False):
  # Projects that require mock routing
  projects = [
    "accumulator",
    "crust",
    "drive",
    "kademlia_routing_table", 
    "lru_time_cache",
    "maidsafe_utilities",
    "message_filter",
    "routing",
    "rust-utp",
    "safe_vault",
    "safe_ffi",
    "safe_launcher",
    "self_encryption",
    "safe_dns",
    "safe_launcher",
    "safe_nfs",
    "safe_core", 
    "xor_name"
  ]
  mock_routing_projects = [
    "safe_dns",
    "safe_launcher"
  ]
  for project in projects:
    if cleaning:
      print "cleaning " + project
      cargo_exec(project, ["cargo", "clean"])
    elif cloning:
      print "cloning " + project
      url = "https://github.com/maidsafe/" + project + ".git"
      subprocess.call(["git", "clone", url])
    else:
      print "building and testing " + project
      mock_routing = project in mock_routing_projects
      cargo_test(project, use_mock_routing=mock_routing)

# Check for a few simple command line args.
cleaning = len(sys.argv) >= 2 and sys.argv[1] == "clean"
cloning = len(sys.argv) >= 2 and sys.argv[1] == "clone"
do_runner(cleaning, cloning)

