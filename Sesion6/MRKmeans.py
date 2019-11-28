"""
.. module:: MRKmeans

MRKmeans
*************

:Description: MRKmeans

    Iterates the MRKmeansStep script

:Authors: bejar
    

:Version: 

:Created on: 17/07/2017 10:16 

"""

from MRKmeansStep import MRKmeansStep
import shutil
import argparse
import os
import time
from mrjob.util import to_lines

__author__ = 'bejar'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prot', default='prototypes.txt', help='Initial prototpes file')
    parser.add_argument('--docs', default='documents.txt', help='Documents data')
    parser.add_argument('--iter', default=5, type=int, help='Number of iterations')
    parser.add_argument('--ncores', default=2, type=int, help='Number of parallel processes to use')

    args = parser.parse_args()
    assign = {}

    if not os.path.exists('res'):
        os.mkdir('res')

    # Copies the initial prototypes
    cwd = os.getcwd()
    shutil.copy(cwd + '/' + args.prot, cwd + '/res/prototypes0.txt')

    nomove = False
    for i in range(args.iter):
        
        tinit = time.time()
        print('Iteration %d ...' % (i + 1))

        # The --file flag tells to MRjob to copy the file to HADOOP
        # The --prot flag tells to MRKmeansStep where to load the prototypes from
        mr_job1 = MRKmeansStep(args=['-r', 'local', args.docs,
                                     '--file', cwd + '/res/prototypes%d.txt' % i,
                                     '--prot', cwd + '/res/prototypes%d.txt' % i,
                                     '--num-cores', str(args.ncores)])

        # Runs the script
        with mr_job1.make_runner() as runner1:
            
            runner1.run()
            new_assign = {}
            new_proto = {}

            # Process the results of the script iterating the (key,value) pairs
            for (key, value) in mr_job1.parse_output(runner1.cat_output()):
                print(key)
                new_assign[key] = value[0]
                new_proto[key] = value[1]
                
            print(mr_job1.prototypes)

            # If your scripts returns the new assignments you could write them in a file here
            new_assign_file = open(cwd + '/res/assignments%d.txt' %(i+1), 'w')
            for key in new_assign:
                aux_string = key + ':'
                for item in new_assign[key]:
                    aux_string = aux_string + item + ' '
                new_assign_file.write(aux_string + '\n')

            new_assign_file.close()

            # You should store the new prototypes here for the next iteration
            if new_assign == assign:
                nomove = True

            assign = new_assign

            if (i + 1) == args.iter or nomove:
                new_proto_file = open(cwd + '/prototypes-result.txt', 'w')
            else:
                new_proto_file = open(cwd + '/res/prototypes%d.txt'%(i+1), 'w')

            for key in new_proto:
                aux_string = key + ':'
                for item in new_proto[key]:
                    aux_string = aux_string + item[0] + '+' + repr(item[1]) + ' '
                aux_string = aux_string[:-1]
                new_proto_file.write(aux_string + '\r\n')

            new_proto_file.close()

        # If you have saved the assignments, you can check if they have changed from the previous iteration

        print("Time= %f seconds" % (time.time() - tinit))

        if nomove:
            print("Algorithm converged")
            break

            # Now the last prototype file should have the results