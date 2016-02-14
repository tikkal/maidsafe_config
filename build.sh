#!/bin/bash 
function ct { 
  pushd $1
  if [[ $1 == "safe_launcher" ]]; then
    cargo test --features "use-mock-routing"
  else
    cargo test
  fi
  popd
}

function cb { 
  pushd $1
  if [[ $1 == "safe_launcher" ]]; then
    cargo build --features "use-mock-routing"
  else
    cargo build
  fi
  popd
}

function cclean {
 pushd $1
 cargo clean
 popd 
}

function cupdate {
 pushd $1
 cargo update
 popd 
}

for PROJECT in rust-utp routing crust safe_vault safe_ffi self_encryption \
  safe_launcher safe_dns safe_nfs safe_core message_filter accumulator \
  xor_name maidsafe_utilities lru_time_cache drive QA rfcs kademlia_routing_table
do
 if [[ $1 == "clean" ]]; then
   cclean $PROJECT
 elif [[ $1 == "update" ]]; then
   cupdate $PROJECT
 else
   ct $PROJECT
 fi
done

