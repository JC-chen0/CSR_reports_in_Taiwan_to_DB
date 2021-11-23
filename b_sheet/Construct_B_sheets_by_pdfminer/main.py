from Construct_B_sheets import construct_gri_df
import Exception_handling
import GRIPointers_B
from GRIPointers_B import GRIPointers_B
import Judging_csr_reports_level
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "--csr_report_path",
    help="Please input the folder containing all csr reports in pdf format",
    default='..\csr_reports\CSR報告書(2020年發佈)')
parser.add_argument(
    "--get_gri_pointers",
    action='store_true',
    help=
    "modifying the csv file with containing the declosed pointers of each company"
)

args = parser.parse_args()
b_sheets_process = GRIPointers_B(csr_report_path=args.csr_report_path,
                                 gri_pointers_csv_name="gri_pointers_b")

# Detect if gri_pointers.csv exists. If not, then create it.
all_file_list = os.listdir('.')
is_gri_pointers = 0
# for file in all_file_list:
#     if file == "gri_pointers_b.csv":
#         is_gri_pointers = 1
#         break
# if not is_gri_pointers:
construct_gri_df()

#initialize the gri pointers csv file to process it in easy way
b_sheets_process.init_gri_pointers_csv_file(
    b_sheets_process.gri_pointers_csv_name)

if args.get_gri_pointers:
    b_sheets_process.catch_gri_pointers(
        gri_csv_name=b_sheets_process.get_gri_pointers_csv_name(),
        csr_report_path=b_sheets_process.get_csr_report_path(),
        search_term='GRI')
    b_sheets_process.output_B_pointers()