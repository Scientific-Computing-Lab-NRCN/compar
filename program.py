import argparse
from compar import Compar
import traceback
import os
import shutil
from exceptions import assert_rel_path_starts_without_sep


def main():
    parser = argparse.ArgumentParser(description='Compar')
    parser.add_argument('-wd', '--working_directory', help='Working directory path', required=True)
    parser.add_argument('-dir', '--input_dir', help='Input directory path', required=True)
    parser.add_argument('-comp', '--binary_compiler_type', help='Binary compiler type', default="")
    parser.add_argument('-comp_v', '--binary_compiler_version', help='Binary compiler version', default=None)
    parser.add_argument('-comp_f', '--binary_compiler_flags', nargs="*", help='Binary compiler flags', default=None)
    parser.add_argument('-save_folders', '--delete_combinations_folders', help='Save all combinations folders',
                        action='store_false')
    parser.add_argument('-make', '--is_make_file', help='Use makefile flag', action='store_true')
    parser.add_argument('-make_c', '--makefile_commands', nargs="*", help='Makefile commands', default=None)
    parser.add_argument('-make_op', '--makefile_exe_folder_rel_path',
                        help='Makefile output executable folder relative path to input directory',
                        default="")
    parser.add_argument('-make_on', '--makefile_output_exe_file_name', help='Makefile output executable file name',
                        default="")
    parser.add_argument('-ignore', '--ignored_rel_paths', nargs="*",
                        help='List of relative folder paths to be ignored while parallelizing', default=None)
    parser.add_argument('-p4a_f', '--par4all_flags', nargs="*", help='Par4all flags', default=None)
    parser.add_argument('-autopar_f', '--autopar_flags', nargs="*", help='Autopar flags', default=None)
    parser.add_argument('-cetus_f', '--cetus_flags', nargs="*", help='Cetus flags', default=None)
    parser.add_argument('-include', '--include_dirs_list', nargs="*",
                        help='Include dir names for compilation - relative paths', default=None)
    parser.add_argument('-main_file', '--main_file_name', help='Main c file name', default="")
    parser.add_argument('-main_file_p', '--main_file_parameters', nargs="*", help='Main c file parameters',
                        default=None)
    parser.add_argument('-slurm_p', '--slurm_parameters', nargs="*", help='Slurm parameters', default=None)
    parser.add_argument('-nas', '--is_nas', help='Is NAS Benchmark', action='store_true')
    args = vars(parser.parse_args())

    # TODO: should be depend on users choice
    if os.path.exists(args['working_directory']):
        shutil.rmtree(args['working_directory'])
    os.mkdir(args['working_directory'])

    assert_rel_path_starts_without_sep(args['makefile_exe_folder_rel_path'])
    for path in args['makefile_exe_folder_rel_path']:
        assert_rel_path_starts_without_sep(path)

    compar_obj = Compar(
        working_directory=args['working_directory'],
        input_dir=args['input_dir'],
        binary_compiler_type=args['binary_compiler_type'],
        binary_compiler_version=['args.binary_compiler_version'],
        binary_compiler_flags=args['binary_compiler_flags'],
        delete_combinations_folders=args['delete_combinations_folders'],
        is_make_file=args['is_make_file'],
        makefile_commands=args['makefile_commands'],
        makefile_exe_folder_rel_path=args['makefile_exe_folder_rel_path'],
        makefile_output_exe_file_name=args['makefile_output_exe_file_name'],
        ignored_rel_paths=args['ignored_rel_paths'],
        par4all_flags=args['par4all_flags'],
        autopar_flags=args['autopar_flags'],
        cetus_flags=args['cetus_flags'],
        include_dirs_list=args['include_dirs_list'],
        main_file_name=args['main_file_name'],
        main_file_parameters=args['main_file_parameters'],
        slurm_parameters=args['slurm_parameters'],
        is_nas=args['is_nas']
    )
    compar_obj.fragment_and_add_timers()
    compar_obj.run_serial()
    compar_obj.run_parallel_combinations()
    compar_obj.generate_optimal_code()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()