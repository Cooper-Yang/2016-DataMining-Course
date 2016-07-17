#2016 Data Mining
##Apriori algorithm

PyApropri.py :

Usage:

	PyApropri.py inputfile.ext outputfile.ext
	
    By default, will use ./test.txt as input, will use ./output.txt as output

About inputfile:
  
  standard csv file format, but only support digit and alphabet, don' support regex
  
  line begin with '#' will be consider as comment

##KNN algorithm

KNN.py:

	KNN.py test_data.file train_data.file output.file
	
	By default, will use ./iris.2D.test.arff as test data, and ./iris.2D.train.arff, and ./output.txt as output
	
exit code 1 represent "no such file"

make sure:
  
  the last column of input_data is the class name which a row belongs to
  
  data in all column except the last column are numeric data

##K-Means algorithm

main_func.py:

    main_func.py input_data output_text
    
    By default, will use ./data.arff as input, and ./output.txt as output
    
exit code 1 represent "IOError" when trying to open input/output file
