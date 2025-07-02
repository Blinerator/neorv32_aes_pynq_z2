
create_project aes_project . -part xc7z020clg400-1 -force

# Package neorv32 as IP
cd ../neorv32/rtl/system_integration/
source neorv32_vivado_ip.tcl
set_property  ip_repo_paths  ./neorv32_vivado_ip_work/packaged_ip [current_project]
update_ip_catalog
cd ../../../syn/

# add_files [glob ./neorv32/rtl/core/*.vhd]
# add_files [glob ./neorv32/rtl/system_integration/*.vhd]
add_files constraints.xdc

source block_design.tcl

make_wrapper -files [get_files ./aes_project.srcs/sources_1/bd/block_design/block_design.bd] -top
add_files -norecurse ./aes_project.srcs/sources_1/bd/block_design/hdl/block_design_wrapper.v
set_property top block_design_wrapper [current_fileset]

update_compile_order -fileset sources_1

launch_runs synth_1 -jobs 4
wait_on_run synth_1

launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1

set log_file "vivado.log"
if {![file exists $log_file]} {
    puts "ERROR: $log_file not found."
    exit 1
}

set fp [open $log_file r]
set content [read $fp]
close $fp

set pass_banner {
  _____         _____ _____ 
 |  __ \ /\    / ____/ ____|
 | |__) /  \  | (___| (___  
 |  ___/ /\ \  \___ \___ \ 
 | |  / ____ \ ____) |___) |
 |_| /_/    \_\_____/_____/                     

}

set fail_banner {
  ______      _____ _      
 |  ____/\   |_   _| |     
 | |__ /  \    | | | |     
 |  __/ /\ \   | | | |     
 | | / ____ \ _| |_| |____ 
 |_|/_/    \_\_____|______|
                           
}

set success_string "write_bitstream completed successfully"
if {[string first $success_string $content] != -1} {
    puts "SUCCESS: Build complete."
    puts $pass_banner
    exit 0
} else {
    puts "ERROR: Bitstream generation failed."
    puts $fail_banner
    exit 1
}
