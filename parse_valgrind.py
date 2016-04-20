#!/usr/bin/python
# -*-coding:utf-8 -*

import re
import sys

reBeginningBlock = re.compile(r'([0-9,]+) bytes in ([0-9,]+) blocks are (possibly lost|still reachable) in loss record ([0-9,]+) of ([0-9,]+)')
forbiddenLibs = ["libopencv_core", "libgnutls", "libgtk", "libp11-kit", "libglib-2", "libopencv_highgui", "libgobject", "libopencv_features2d", "libopencv_imgproc", "libpixman", "libavformat"]

def help():
    print """Parses the valgrind output to remove useless libraries.
Should be used after such command:
    
    valgrind --tool=memcheck --leak-check=yes --leak-check=full --show-leak-kinds=all --log-file=output.txt --gen-suppressions=all ./binary

This will generate a file, output.txt, which contains the valgrind output and code to remove noisy log. You can now call:
    
    parseValgrind --get-exceptions output.txt

This script will create a output_exceptions.txt which contains the blocks removing the so called noisy log.

You can now use valgrind normally. By adding --suppressions=output_exceptions.txt, valgrind will shut down the undesired logs.
    
    valgrind --tool=memcheck --leak-check=yes --leak-check=full --show-leak-kinds=all --log-file=output.txt --suppressions=output_exceptions.txt ./binary

The libraries list is (for now) static in the script file but it could be a good idea to find a way to make it dynamic (maybe look for ??? in the last line of the block?): """
    print "\n\t* "+"\n\t* ".join(forbiddenLibs) + "\n"
    print """The script will also generate a output_parsed.txt file which contains the valgrind log without the noisy log. You can either use the valgrind --suppressions function or the python script (by putting it as an alias in your bashrc for e.g.)."""

if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        help()
    else:
        filelist = sys.argv[1:]
        if sys.argv[1] == "--get-exceptions":
            getExceptions = True
            filelist = sys.argv[2:]
        getExceptions = False
        for filename in filelist:
            # if is parameter
            linesToKeep = []
            opencvBlock = False
            blockLines = []
            exceptionsLines = []
            lastBlock = -1
            currentLib = ""
            alreadyReplacedDots = False
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    infoBeginning = reBeginningBlock.findall(line)
                    if len(infoBeginning) > 0:
                        if not opencvBlock:
                            linesToKeep += blockLines
                        opencvBlock = False
                        blockLines = []
                        if getExceptions:
                            lastBlock += 1
                            exceptionsLines.append([])
                    # elif not "    " in line and len(line) > 12:
                    #     print "Possibly failed"
                    #     print line
                    for lib in forbiddenLibs:
                        if lib in line:
                            currentLib = lib
                            opencvBlock = True
                    if not "==" in line:
                        if opencvBlock and getExceptions:
                            #if "fun:" in line and not alreadyReplacedDots:
                            #    line = "\t...\n"
                            #    alreadyReplacedDots = True
                            #elif "fun:" in line:
                            #    line = ""
                            #elif alreadyReplacedDots:
                            #    alreadyReplacedDots = False
                            if "insert_a_suppression_name_here" in line:
                                line = line.replace("<insert_a_suppression_name_here>", currentLib)
                            exceptionsLines[lastBlock].append(line)
                    else:
                        blockLines.append(line)
            linesToKeep += blockLines
            filenameExt = filename.split(".")
            outName = ".".join(filenameExt[:-1]) + "_parsed." + filenameExt[-1]
            with open(outName, 'w') as f:
                f.write("".join(linesToKeep))
            print filename + " has been parsed and saved to " + outName
            if getExceptions:
                exceptionsBlocks = ["".join(block) for block in exceptionsLines]
                outputBlocks = ""
                for i, block in enumerate(exceptionsBlocks):
                    if block in exceptionsBlocks[i+1:]:
                        continue
                    else:
                        outputBlocks += block
                outName = ".".join(filenameExt[:len(filenameExt)-1]) + "_exceptions." + filenameExt[len(filenameExt)-1]
                with open(outName, 'w') as f:
                    f.write(outputBlocks)
                print filename + " exceptions have been parsed and saved to " + outName

        if len(filelist) == 0:
            print "No file has been sent. Please add arguments to the script."
else:
    help()