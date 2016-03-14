import math, copy, sys, random

class Node():
    index = 0
    def __init__(self):
        self.attribute_name = None
        self.number = Node.index
        Node.index += 1
        self.childNodes = {}
        
reset = {"Yes":0, "No":0}
added = 0
size = {"Large":copy.deepcopy(reset), "Medium":copy.deepcopy(reset), "Small":copy.deepcopy(reset)}
occupied = {"High":copy.deepcopy(reset), "Moderate":copy.deepcopy(reset), "Low":copy.deepcopy(reset)}
price = {"Expensive":copy.deepcopy(reset), "Normal":copy.deepcopy(reset), "Cheap":copy.deepcopy(reset)}
music = {"Loud":copy.deepcopy(reset), "Quiet":copy.deepcopy(reset)}
location = {"Talpiot":copy.deepcopy(reset), "City-Center":copy.deepcopy(reset), "Mahane-Yehuda":copy.deepcopy(reset), "Ein-Karem":copy.deepcopy(reset), "German-Colony":copy.deepcopy(reset)}
VIP = {"Yes":copy.deepcopy(reset), "No":copy.deepcopy(reset)}
favorite_beer = {"Yes":copy.deepcopy(reset), "No":copy.deepcopy(reset)}

ruleset = []

valueset = {"size":copy.deepcopy(size), "occupied":copy.deepcopy(occupied), "price":copy.deepcopy(price), "music":copy.deepcopy(music), "location":copy.deepcopy(location), "VIP":copy.deepcopy(VIP), "favorite_beer":copy.deepcopy(favorite_beer)}
attributeset = ["size", "occupied", "price", "music", "location", "VIP", "favorite_beer"]
entropy = {"size":0, "occupied":0, "price":0, "music":0, "location":0, "VIP":0, "favorite_beer":0}

def calcEntropy(attributeref, valuesetref, entropyref, recordsref):
    finalentropy = 0
    recordno = 1
    reclength = len(recordsref)
    print "the records to act on :"
    for each in recordsref:
        print "The record is ",recordno,":",each
        recordno += 1
    for key in valueset[attributeref]:
        print "calculating entropy for :",key
        res = 0
        Y = valuesetref[attributeref][key]["Yes"]
        print "num of records with class Yes is:",Y
        N = valuesetref[attributeref][key]["No"]
        print "num of records with class No is:",N
        total = Y+N
        print "The total is :",total
        if Y != 0:
            print "contribution to individual entropy by value:",key," for class Yes is =",float("{0:.2f}".format((float(Y)/total)*math.log(float(total)/Y,2)))
            res += float("{0:.2f}".format((float(Y)/total)*math.log(float(total)/Y,2)))
        if N != 0:
            print "contribution to individual entropy by value:",key," for class No is =",float("{0:.2f}".format((float(N)/total)*math.log(float(total)/N,2)))
            res += float("{0:.2f}".format((float(N)/total)*math.log(float(total)/N,2)))
        print "entropy for value :",key," is :",(float(total)/reclength)*(res) 
        finalentropy += (float(total)/reclength)*(res)
    entropyref[attributeref] = float("{0:.2f}".format(finalentropy))
    print "final entropy for the attribute:",attributeref," is =",entropyref[attributeref]

def getEntropy(valuesetref, entropyref, recordsref, attributeref):
    indOfAttr = attributeset.index(attributeref)
    indOfClass = len(recordsref[0])-1
    for ele in recordsref:
        value = ele[indOfAttr]
        Class = ele[indOfClass]
        valuesetref[attributeref][value][Class] += 1
        if not valuesetref[attributeref][value].has_key(Class+"records"):
            valuesetref[attributeref][value][Class+"records"] = copy.deepcopy(recordsoriginal);
        valuesetref[attributeref][value][Class+"records"].append(ele)

def getLowest(ent):
    lowest = sys.float_info.max
    tiebreakerchoice = []
    lowestkey = None
    for key in ent:
        if ent[key] < lowest:
            lowest = ent[key]
    for key in ent:
        if ent[key] == lowest:
            tiebreakerchoice.append(key)
    if len(tiebreakerchoice) == 1:
        lowestkey = tiebreakerchoice[0]
    else:
        lowestkey = random.choice(tiebreakerchoice)
    return lowestkey

def makeDT(ro, en, va, at, re, ss, ParO, keyO, level, rule):
    global added 
    print "" 
    RO = None
    A = None
    V = None
    if keyO is not None and ParO is not None:                                                  #root, entropy, valueset, attributeset, records, setState
        print "The parent of this node is :",ParO
        print "The records to work on have the attribute: ",ParO," with attribute\'s value being: ",keyO
    print "no of records to work on?: ",len(re)
    overallY = 0
    overallN = 0
    if len(at) == 0:                                                                    #all attributes have been checked
        return                                                                          #so, you are ending the function control
    global recordsoriginal 
    Setstate = None                                                               #To set up a state for the next recursion call                                                   
    purity = []
    puritycount = None
    for ele in at:                                                                      #checking each attribute in attributeset
        print "The attribute being checked is",ele                                                                       #printing the element
        getEntropy(va, en, re, ele)         #setup required variables for calculating entropy  #valueset, entropy, records, element
        calcEntropy(ele, va, en, re)        #setup required variables for calculating entropy  #element, valueset, entropy, records
    print "Entropies are:",en                                #check out the entropies that have been been calculated 
    parentKey = getLowest(en)                                                           #get the attribute with the lowest entropy
    ro.attribute_name = parentKey                                             #set the root node with that lowest entropy attribute
    K = str(ro.attribute_name)
    if keyO is not None:
        print "the attribute with the highest info gain is :",parentKey," and we now create a subtree with ",parentKey," as root and ",keyO," as it's key"
    else:
        print "the attribute with the highest info gain is :",parentKey," and we now create a subtree with ",parentKey," as root"
    #print "the value of the Node is ",ro.attribute_name
    for k in va[parentKey].keys():
        RO = copy.deepcopy(rule)
        V = str(k)
        print "The key for which a subtree is being created is :",k                                                  #print the value of the attribute
        if 'Yesrecords' not in va[parentKey][k] and 'Norecords' in va[parentKey][k]:
            purity = va[parentKey][k]['Norecords']
            puritycount = va[parentKey][k]['No']
            overallN += puritycount
        elif 'Norecords' not in va[parentKey][k] and 'Yesrecords' in va[parentKey][k]:
            purity = va[parentKey][k]['Yesrecords']
            puritycount = va[parentKey][k]['Yes']
            overallY += puritycount
        elif 'Yesrecords' not in va[parentKey][k] and 'Norecords' not in va[parentKey][k]:
            purity = None
            puritycount = 0
        elif 'Yesrecords' in va[parentKey][k] and 'Norecords' in va[parentKey][k]:
            purity = va[parentKey][k]['Yesrecords']+va[parentKey][k]['Norecords']
            puritycount = va[parentKey][k]['Yes']+va[parentKey][k]['No'] 
            overallN += va[parentKey][k]['No']
            overallY += va[parentKey][k]['Yes']
        if purity is None:
            print "The length of purity is: ",0
        else:
            print "The length of purity is: ",len(purity)                           #print the number of associated records
        print "The Records associated with ",k," are : ",purity             #print the records associated with the attribute value          
        print "The number of Records associated with ",k," is :",puritycount
        if va[parentKey][k]['Yes'] == puritycount and purity is not None:                              #all records are of class 'Yes'
            ro.childNodes[k] = "Yes"
            RO += str(K+":"+V+"=Yes")
            ruleset.append(RO)
            print "Pure set at the value ",k," is ",ro.childNodes[k]            #child node with value is 'Yes'
            print "parent node and childnode with key: ", parentKey," ",k," has value: ",ro.childNodes[k]
        elif va[parentKey][k]['No'] == puritycount and purity is not None:                             #all records are of class 'No'
            ro.childNodes[k] = "No"                                             #child node with value is 'No'
            RO += str(K+":"+V+"=No")
            ruleset.append(RO)
            print "Pure set at the value ",k," is ",ro.childNodes[k]
            print "parent node and childnode with key: ", parentKey," ",k," has value: ",ro.childNodes[k]
        elif puritycount == 0 and purity is None:
            ro.childNodes[k] = "Unsure"
            RO += str(K+":"+V+"=Unsure")
            ruleset.append(RO)
            print "No set for the value ",k," is ",ro.childNodes[k]
            print "childnode with key: ",k," has value: ",ro.childNodes[k]
        else:
            RO += str(K+":"+V+";")
            ROcopy = copy.deepcopy(RO)
            print "childnode with key: ",k," has impure set, so building a subtree with to act on the partial set of records"
            Setstate = copy.deepcopy(ss)
            del Setstate["entO"][parentKey]
            enCopy = copy.deepcopy(Setstate["entO"])
            del Setstate["vaO"][parentKey]
            vaCopy = copy.deepcopy(Setstate["vaO"])
            keyindex = Setstate["attO"].index(parentKey)
            del Setstate["attO"][keyindex] 
            atCopy = copy.deepcopy(Setstate["attO"])
            reCopy = copy.deepcopy(recordsoriginal)
            ro.childNodes[k] = Node()           
            reCopy = copy.deepcopy(purity)
            if k is not None and ro.attribute_name is not None:
                print "going to the node whose key will be: ",k," and parent will be: ",ro.attribute_name
            makeDT(ro.childNodes[k], enCopy, vaCopy, atCopy, reCopy, Setstate, ro.attribute_name, k, level+1, ROcopy) 
            if keyO is not None and ParO is not None:
                print "going back to the node whose key: ",keyO," and parent is: ",ParO
            elif keyO is None and ParO is None:
                print "going back to the origin"
            print "-----------------------------------------------------"

def travel(traveller, testcase):
    result = None
    testattr = traveller.attribute_name
    print "the attribute being checked is : ",testattr
    testattrvalue = testcase[testattr]
    print "value of the attribute which acts as the key to the next node or the class: ",testattrvalue
    next = traveller.childNodes[testattrvalue]
    if isinstance(next, Node) == False:
        print "we have our answer, and it is : ",next
        result = next
        return result
    elif isinstance(next, Node) == True:
        print "we haven't found our answer yet"
        return travel(next, testcase)
        
records = []
recordsoriginal = copy.deepcopy(records)

lines = [line.rstrip('\n') for line in open("dt-data.txt")]
for i in range(2,len(lines)):
    prod = lines[i].split(':')[1]
    prod = prod.lstrip()
    prod = prod.rstrip()
    data = prod.split(', ')
    temp = data[len(data)-1]
    data[len(data)-1] = temp[0:len(temp)-1]
    records.append(data)

root = Node()
traverse = root

valuesetoriginal = copy.deepcopy(valueset)      
entropyoriginal = copy.deepcopy(entropy)
attributesetoriginal = copy.deepcopy(attributeset)
originals = {"vaO":valuesetoriginal, "entO":entropyoriginal, "attO":attributesetoriginal}
setState = copy.deepcopy(originals)
print ""
makeDT(root, entropy, valueset, attributeset, records, setState, None, None, 0, "")
print "=================================================================================="
for each in ruleset:
    print each
print "=================================================================================="
testcase = {"size":"Large", "occupied":"Moderate", "price":"Cheap", "music":"Loud", "location":"City-Center", "VIP":"No", "favorite_beer":"No"}
print testcase
travel(traverse, testcase)