import csv
import re
import time
import matplotlib.pyplot as plt
from ArithmeticEvaluator import NumericStringParser
from LogicalEvaluator import nested_bool_eval

ctr = 0
plot_eval = list()
plot_algo = list()
in_var = dict()
main_equa = list()
count = 0

def evaluate(expression):
    our_token = ''
    nsp = NumericStringParser()
    in_equa = expression
    math_tokens = ['==', '<=', '>=', '<', '>', '!=']
    for tokens in math_tokens:
        if in_equa.find(tokens) == -1:
            pass
        else:
            our_token = tokens
            break
    #print (our_token)
    in_expr = in_equa.split(our_token)
    result = [0,0]
    for idx,values in enumerate(in_expr):
        count_left = values.count('(')
        count_right = values.count(')')
        if count_left > count_right:
            diff = count_left - count_right
            try:
                result[idx] = nsp.eval(values[diff:])
            except ZeroDivisionError:
                print ("divide by zero in equation %d" % (values[diff:]))
        elif count_left < count_right:
            diff = count_right - count_left
            #print (values[:len(values)-diff])
            try:
                result[idx] = nsp.eval(values[:len(values)-diff])
            except ZeroDivisionError:
                print ("divide by zero in equation %d" % (values[:len(values)-diff]) )
        elif count_left == count_right:
            try:
                result[idx] = nsp.eval(values)
            except ZeroDivisionError:
                print ("divide by zero in equation %d" % (values) )
        
    final_result = eval(str(result[0])+our_token+str(result[1]))
    if final_result:
        return ('1')
    else:
        return ('0')

def eval_equa(math_equa):
    math_equa = '((10000/10+100-1000+1+21-41*2+555-444+11*89-100/100-100)>1028)||((102900/100-1)==1029)'
    sec_math = math_equa
    global ctr
    math_tokens = ['&&', '||']
    global count    

    math_expr = re.split('&&|\||',math_equa)
    math_expr = [i for i in math_expr if i != '']
 
    count = count + 1
    start = time.time() 
    for values in math_expr:
        count_left = values.count('(')
        count_right = values.count(')')

        if count_left > count_right:
            diff = count_left - count_right
            #print (values[diff:])
            sec_math = sec_math.replace(values[diff:], evaluate(values[diff:]))
        elif count_left < count_right:
            diff = count_right - count_left
            #print (values[:len(values)-diff])
            sec_math = sec_math.replace(values[:len(values)-diff], evaluate(values[:len(values)-diff]))
        elif count_left == count_right:
            #print (values)
            sec_math = sec_math.replace(values,evaluate(values))
                
    print (sec_math)
    main_result = nested_bool_eval(sec_math)
    end = time.time()
    plot_algo.append(end-start)
  #  print(end - start)
    start1 = time.time()
    math_equa = math_equa.replace('&&', ' and ')
    math_equa = math_equa.replace('||', ' or ')
    eval(math_equa)
    end1 = time.time()
    plot_eval.append(end1-start1)
  #  print (end1 - start1)
    return main_result

print ("Starting Mad Max parser...")
ifile  = open("inputExpressions.txt", "rt")
efile  = open("inputVariables.csv", "rt")
ofile  = open("outputExpressions.csv", "w")

try:
    reader = csv.reader(efile)
    for row in reader:
        in_var[row[0]] = row[1]
finally:
    efile.close()

for line in iter(ifile):
    temp_line = line
    try:
        writer = csv.writer(ofile, delimiter=',')
        for key, value in in_var.items():
            line = line.replace(key, value)
        result = eval_equa(line)
        print (('%s \t %s') % (temp_line, str(result)))
        writer.writerow([temp_line, str(result)])
    except (IOError, OSError) as e:
        print  ('The file specified had an IO Error ')
ofile.close()
ifile.close()
y_list = range(0,count)
plt.title('Performance of eval vs our algorithm')
plt.ylabel('Execution time (secs)')
plt.xlabel('Expressions(using Algo(blue) and Eval(red))')
plt.plot(y_list, plot_eval,'r-', label='Eval performance')
plt.plot(y_list, plot_algo,'b-', label='Our algorithm performance')
plt.savefig('PerformanceGraph.png')
plt.show()

