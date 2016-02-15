#!/usr/bin/python

# Note, in your .bashrc, put: 
#  export SODIUM_LIB_DIR=/usr/local/lib
#  export RUST_TEST_THREADS=1
# See maidsafe forums for info re. installing libsodium
# and other configuration tips.

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
    if "clone" in options:
      print "git clone " + project
      url = "https://github.com/maidsafe/" + project + ".git"
      subprocess.call(["git", "clone", url])
    if "pull" in options:
      print "git pull " + project
      call_with_cwd(project, ["git", "pull"])
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

  # Check required env vars
  for env_key in ["RUST_TEST_THREADS", "SODIUM_LIB_DIR"]:
    env_val = os.environ.get(env_key)
    if env_val is None:
      print "** " + env_key + " env var not set."
      ret = False
    else:
      print env_key + " is " + env_val
  return ret

# Check for a few simple command line args.
options = ["build", "clean", "clone", "pull", "test", "update"]
if len(sys.argv) < 2:
  print "Please specify at least one of: " + ", ".join(options)
elif not check_env():
  print "Environment checks failed." 
  print "See maidsafe forums for tips on fixing your environment."
else: 
  do_runner(sys.argv)

