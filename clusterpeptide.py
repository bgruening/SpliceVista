import sys
import os
import getopt
import numpy
import scipy.cluster.hierarchy as sch

def formatoutput(array): #format output
    for i in range(0,len(array)):
        newline='\t'.join(array[i]) +'\n'
        output.write(newline)

def main(): #clustering and write output
    if len(pep_array)>1:
        matrix=[]
        for i in range(0,len(pep_array)):
            matrix.append(pep_array[i][3].split(','))

        dataMatrix=numpy.array(matrix,dtype=float)
        d = sch.distance.pdist(dataMatrix,metric)# vector of pairwise distances
        D = numpy.clip(d,0,2)
        L = sch.linkage(D, method,metric)
        ind = sch.fcluster(L,distance,'distance')#distance is dissmilarity(1-correlation)
        p=numpy.array(pep_array)
        p=numpy.column_stack([p,ind])
        formatoutput(p)
    else:
        p=numpy.array(pep_array)
        p=numpy.column_stack([p,[0]])
        formatoutput(p)
    
if __name__=='__main__':
    ################  Default  ################
    method = 'average'
    distance= 0.4
    metric = 'euclidean'
    
    ################  Comand-line arguments ################
    if len(sys.argv[1:])<=1:  ### Indicates that there are insufficient number of command-line arguments
        print "Warning! wrong command, please read the mannual in Readme.txt."
        print "Example: python pqpq2.py --i heavy_pepdata.txt --o heavy_pqpqout.txt"
    else:
        options, remainder = getopt.getopt(sys.argv[1:],'', ['metric=',
                                                             'method=','d=',
                                                             'i=','o='])
        for opt, arg in options:
            if opt == '--metric': metric=arg
            elif opt == '--method': method=arg
            elif opt == '--d': distance=arg
            elif opt == '--i':infilename=arg
            elif opt == '--o':outfilename=arg
            else:
                print "Warning! Command-line argument: %s not recognized. Exiting..." % opt; sys.exit()
    
    print metric,"metric is used to measure the distance of elements"
    print "distance cutoff to form a new cluster is",distance

    handle=open(infilename,'r')
    handle.readline()
    gene_peparray={}
    for line in handle:
        row=line[:-1].split("\t")[:-1] # the last column in pepdata.txt is removed, a new cluster will be assigned to each peptide
        gene=row[0]
        if gene not in gene_peparray:
            gene_peparray[gene]=[row]
        else:
            gene_peparray[gene].append(row)

    print 'there are',len(gene_peparray),'genes in total'
    handle.close()
    
    newheader=['gene','pep','PSM count','foldchange','standard_dev','cluster']
    firstline='\t'.join(newheader)+'\n'
    output=open(outfilename,'w')
    output.write(firstline)
    
    i=0
    for gene in gene_peparray.keys():
        i+=1
        pep_array=gene_peparray[gene]
        main()
        if i%1000==0:
            print i,'genes processed'
    print len(gene_peparray),'genes processed'
    print 'program finished'    