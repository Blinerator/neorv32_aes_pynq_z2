import subprocess
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

def clean_syn():
    syn_dir = "./syn"
    keep_files = {"block_design.tcl", "constraints.xdc"}

    if not os.path.exists(syn_dir):
        print(f"Directory '{syn_dir}' does not exist. Skipping cleanup.")
        return

    for filename in os.listdir(syn_dir):
        file_path = os.path.join(syn_dir, filename)
        if filename not in keep_files:
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    print(f"Deleting file: {file_path}")
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    print(f"Deleting directory: {file_path}")
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def get_all_vhdl_files(root_dir):
    vhdl_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(".vhd"):
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                vhdl_files.append(rel_path)
    return vhdl_files


if __name__ == "__main__":

    clean_syn()

    tcl_script = "build.tcl"
    project_name = "aes_project"
    part = "xc7z020clg400-1"  # PYNQ-Z2
    vivado_path = "E:\\Xilinx_Vivado\\Vivado\\2023.2\\bin\\vivado.bat"

    # Build directory
    os.makedirs("syn", exist_ok=True)

    # Create TCL script
    with open(os.path.join("syn", tcl_script), "w") as f:
        f.write(f"""
    set pass_banner {{
     _____         _____ _____ 
    |  __ \ /\    / ____/ ____|
    | |__) /  \  | (___| (___  
    |  ___/ /\ \  \___ \\___ \ 
    | |  / ____ \ ____) |___) |
    |_| /_/    \_\_____/_____/                     

    }}

    set fail_banner {{
     ______      _____ _      
    |  ____/\   |_   _| |     
    | |__ /  \    | | | |     
    |  __/ /\ \   | | | |     
    | | / ____ \ _| |_| |____ 
    |_|/_/    \_\_____|______|
                            
    }}
                
    create_project {project_name} . -part {part} -force

    # Package neorv32 as IP
    cd ../neorv32/rtl/system_integration/
    source neorv32_vivado_ip.tcl
    set_property  ip_repo_paths  ./neorv32_vivado_ip_work/packaged_ip [current_project]
    update_ip_catalog
    cd ../../../syn/

    add_files ../neorv32/rtl/aes_core/aes-128-fpga/src/aes_128_top_wrapper_simple.vhd
    add_files constraints.xdc

    update_compile_order -fileset sources_1

    source block_design.tcl

    make_wrapper -files [get_files ./{project_name}.srcs/sources_1/bd/block_design/block_design.bd] -top
    add_files -norecurse ./{project_name}.srcs/sources_1/bd/block_design/hdl/block_design_wrapper.v
    set_property top block_design_wrapper [current_fileset]

    update_compile_order -fileset sources_1

    launch_runs synth_1 -jobs 4
    wait_on_run synth_1

    launch_runs impl_1 -to_step write_bitstream -jobs 4
    wait_on_run impl_1

    set log_file "vivado.log"
    if {{![file exists $log_file]}} {{
        puts "ERROR: $log_file not found."
        exit 1
    }}

    set fp [open $log_file r]
    set content [read $fp]
    close $fp

    set success_string "write_bitstream completed successfully"
    if {{[string first $success_string $content] != -1}} {{
        puts "SUCCESS: Build complete."
        puts $pass_banner
        exit 0
    }} else {{
        puts "ERROR: Bitstream generation failed."
        puts "$fail_banner"
        exit 1
    }}
    """)

    # Run Vivado in batch mode
    subprocess.run([vivado_path, "-mode", "batch", "-source", tcl_script],
                   cwd="./syn")
    # TODO: pass/fail in python