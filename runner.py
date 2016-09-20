#!/usr/bin/env python

import os
import subprocess
import sys

def call_with_cwd(project, exec_args):
  # Use Popen to set directory in project
  p = subprocess.Popen(exec_args, cwd=project)
  p.wait()

def cargo_build_or_test(project, options, use_mock_routing=False):
  if "test" in options:
    print "test " + project
    cargo_args = ["cargo", "test"]
  else:
    print "build " + project
    cargo_args = ["cargo", "build"]

  # Add mock routing feature if specified
  if (use_mock_routing):
    cargo_args.extend(["--features", "use-mock-routing"])

  call_with_cwd(project, cargo_args)

def do_runner(options):
  projects = [
    "accumulator",
    "config_file_handler",
    "crust",
    "kademlia_routing_table",
    "lru_time_cache",
    "maidsafe_utilities",
    "routing",
    "rust_sodium",
    "safe_core",
    "safe_launcher",
    "safe_vault",
    "secure_serialisation",
    "self_encryption",
  ]
  mock_routing_projects = [
    "safe_core",
    "safe_launcher",
  ]
  node_projects = [
    "safe_launcher"
  ]

  for project in projects:
    if "clone" in options:
      print "git clone " + project
      url = "https://github.com/maidsafe/" + project + ".git"
      subprocess.call(["git", "clone", url])
    if "pull" in options:
      print "git pull " + project
      call_with_cwd(project, ["git", "pull"])
    if project not in node_projects:
      if "clean" in options:
        print "cargo clean " + project
        call_with_cwd(project, ["cargo", "clean"])
      if "update" in options:
        print "cargo update " + project
        call_with_cwd(project, ["cargo", "update"])
      if "build" in options or "test" in options:
        mock_routing = project in mock_routing_projects
        cargo_build_or_test(project, options, use_mock_routing=mock_routing)

def check_env():
  print "Running environment checks."
  ret = True

  # Check required executables
  for prog in ["cargo", "rustc", "git"]:
    try:
      subprocess.call([prog, "--version"])
    except:
      print "** Trouble finding version of " + prog
      ret = False
  return ret

# Check for a few simple command line args.
options = ["build", "clean", "clone", "pull", "test", "update"]
if len(sys.argv) < 2:
  print "Please specify at least one of: " + ", ".join(options)
elif not check_env():
  print "Environment checks failed."
  print "See MaidSafe forums for tips on fixing your environment."
else:
  do_runner(sys.argv)
