# import camelot

# file = "D:\\Non_system\\NCCU\\case\\csr_reports\\CSR報告書(2020年發佈)\\1101_台泥_2019(v1).pdf"

# # extract all the tables in the PDF file
# tables = camelot.read_pdf(file)

# # number of tables extracted
# print("Total tables extracted:", tables.n)

import ctypes
from ctypes.util import find_library
find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))