
outputFile=open("label_data.json",'w+')
inputFile=open("jsonIntersecionData.json",'r+').readlines()

lanesData = inputFile[1:-1]

for n,line in enumerate(lanesData):
    formattedLine = line.replace("\t", "").replace(" ", "").replace("},", "}").replace("^\s","")
    if formattedLine.startswith("{"):
       lanesData[n] = "\n"+formattedLine.rstrip()	
    else:
       lanesData[n]=formattedLine.rstrip()

data = "".join(lanesData)
outputFile.writelines(data)

