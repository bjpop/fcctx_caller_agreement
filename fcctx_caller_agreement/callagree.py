'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 2018
License     : BSD-2-Clause 
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX

Blah XXX 
'''

from argparse import ArgumentParser
import sys
import logging
import pkg_resources
import csv
from intervaltree import Interval, IntervalTree


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
EXIT_CNV_FILE_ERROR = 3
DEFAULT_VERBOSE = False
DEFAULT_OVERLAP = 0.8
PROGRAM_NAME = "callpagree"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Blah XXX'
    parser = ArgumentParser(description=description)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
                        metavar='LOG_FILE',
                        type=str,
                        help='record program progress in LOG_FILE')
    parser.add_argument('--overlap',
                        metavar='OVERLAP',
                        default=DEFAULT_OVERLAP,
                        type=float,
                        help='proportion of overlap required between two CNVs to be considered equal, default: {}'.format(DEFAULT_OVERLAP))
    parser.add_argument('--penn',
                        metavar='PENN_CNV_FILE',
                        type=str,
                        help='Input Penn CNV file')
    parser.add_argument('--cnvpart',
                        metavar='CNVPART_FILE',
                        type=str,
                        help='Input CNV Partition file')
    return parser.parse_args()


def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))


class Intervals(object):
    def __init__(self):
        self.samples = {}

    def insert(self, sample, chrom, start, end, val):
        if sample not in self.samples:
            sample_dict = {}
            self.samples[sample] = sample_dict
        else:
            sample_dict = self.samples[sample]

        if chrom not in sample_dict:
            sample_dict[chrom] = IntervalTree()

        sample_dict[chrom][start:end] = val 

    def lookup(self, sample, chrom, start, end):
        if sample in self.samples:
            if chrom in self.samples[sample]:
                return self.samples[sample][chrom][start:end]
        return set()

def overlap_filter(start1, end1, start2, end2, min_overlap):
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)
    if overlap_start < overlap_end:
        overlap_size = float((overlap_end - overlap_start) + 1)
        cnv1_size = (end1 - start1) + 1
        cnv2_size = (end2 - start2) + 1
        cnv1_overlap = overlap_size / cnv1_size
        cnv2_overlap = overlap_size / cnv2_size
        return cnv1_overlap >= min_overlap and cnv2_overlap >= min_overlap
    return False


def read_penn(penn_filename):
    intervals = Intervals()
    num_cnvs = 0
    with open(penn_filename) as file:
        reader = csv.DictReader(file, delimiter=",")
        # chr,start,end,numsnp,length,state,cn,sampleID,startsnp,endsnp,conf
        for row in reader:
            # drop "signal" from front of sampleID
            this_sample = row['sampleID'][6:]
            intervals.insert(this_sample, row['chr'], int(row['start']), int(row['end']), float(row['conf']))
            num_cnvs += 1
    return intervals, num_cnvs


def read_cnvpart(min_overlap, cnvpart_filename, penn_intervals):
    agree = 0
    num_cnv_calls = 0
    with open(cnvpart_filename) as file:
        reader = csv.DictReader(file, delimiter=",")
        # Sample ID,Chr,Start,End,CNV Value,CNV Conf,Comment,Callrate
        for row in reader:
            num_cnv_calls += 1
            this_start = int(row['Start'])
            this_end = int(row['End'])
            intersects = penn_intervals.lookup(row['Sample ID'], "chr" + row['Chr'], int(row['Start']), int(row['End']))
            for i in intersects:
                if overlap_filter(i.begin, i.end, this_start, this_end, min_overlap):
                    agree += 1
                    break
    return agree, num_cnv_calls


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    penn_intervals, num_penn_cnvs = read_penn(options.penn)
    agree, num_cnvpart_cnvs = read_cnvpart(options.overlap, options.cnvpart, penn_intervals)
    print((num_penn_cnvs, num_cnvpart_cnvs, agree))


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
