#!/usr/bin/python

import os, sys, getopt, shutil
from subprocess import call

idir = ''
remove = False

def usage():
	print
	print
	print "This tool is only for decrypted ROMS that contain .szs files (i.e. a Nintendo ROM)"
	print
	print
	print "How to/What do's"
	print
	print
	print "-h --help - Displays this :)"
	print "ex. gc_dumper.py -h"
	print
	print "-i --input - The local path to the root directory of the rom"
	print "gc_dumper.py -i <path/to/rom/dir/>"
	print
	print "-r --remove - Remove all created directories and .0rarc files"
	print "ex. gc_dumper.py -i <path/to/rom/> -r"
	print
	print

	sys.exit(0)

def main():
	global idir
	global remove

	if not len(sys.argv[1:]):
		usage()

	try: 
		opts, args = getopt.getopt(sys.argv[1:], "hi:r", ["help", "input", "remove"])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-i", "--input"):
			idir = a
		elif o in ("-r", "--remove"):
			remove = True
		else:
			assert False, "Unhandled Option"

	if not remove:
		extract_szs()
	else:
		removeFiles()


def extract_szs():
	any_rarcs = False
	for subdir, dirs, files in os.walk(idir):
		for file in files:
			if ".szs" in file:
				if "0.rarc" not in file:
					print "Extracting " + file
					any_rarcs = True
					call(["yaz0dec.exe", os.path.join(subdir, file)])
	if any_rarcs:
		extract_rarc()

def extract_rarc():
	for subdir, dirs, files in os.walk(idir):
		for file in files:
			if "0.rarc" in file:
				print "Extracting " + file 
				call(["rarcdump.exe", os.path.join(subdir, file)])
	cleanup()

def convert_bti():
	print "hi"

def cleanup():
	for subdir, dirs, files in os.walk(idir):
		for file in files:
			if "0.rarc" in file:
				print "Cleaning up " + file
				os.remove(os.path.join(subdir, file))

def removeFiles():
	for subdir, dirs, files in os.walk(idir):
		for file in files:
			if "0.rarc" in file:
				print "Removing " + file
				os.remove(os.path.join(subdir, file))
		for cdir in dirs:
			if "0.rarc_dir" in cdir:
				print "Removing " + cdir
				shutil.rmtree(os.path.join(subdir, cdir))

if __name__ == '__main__':
	main()



