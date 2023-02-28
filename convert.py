with open('./dataset.txt') as myFile:
  text = myFile.read()
result = text.split('#')
result2 = text.split('/')

for i in range(0,2):
    if(result2[i].find("#") !=-1):
        print("----------")
    print(result2[i])
    print("--")
