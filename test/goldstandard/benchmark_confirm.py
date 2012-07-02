import sqlite3 as sql
import os
import sys
import logging
import benchmark



#  bmVerify(['final_r7', 'final_r8'], filepath="/home/ysun/disambig/newcode/all/", outdir = "/home/ayu/results_v2/")
        

# Text Files
txt_file = 'benchmark_errors.txt'
opened_file = open(txt_file, 'U')
log_file = 'benchmark_results.log'
