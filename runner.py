#!/usr/bin/python

import subprocess

def cargo_exec(project, cargo_args):
  p = subprocess.Popen(cargo_args, cwd=project)
  p.wait()
  
def cargo_test(project, use_mock_routing=False):
  cargo_args = ["cargo", "test"]

  # Add mock routing feature if specified
  if (use_mock_routing): 
    cargo_args.extend(["--features", "use-mock-routing"])

  cargo_exec(cargo_args, project)

def do_runner():
  projects = [
    "accumulator",
    "drive",
    "kademlia_routing_table", 
    "lru_time_cache",
    "maidsafe_utilities",
    "message_filter",
    "routing crust",
    "rust-utp", 
    "QA", 
    "rfcs", 
    "safe_vault",
    "safe_ffi",
    "safe_launcher",
    "self_encryption",
    "safe_launcher",
    "safe_dns",
    "safe_nfs safe_core", 
    "xor_name"
  ]
  for (project in projects):
    cargo_test(project)

