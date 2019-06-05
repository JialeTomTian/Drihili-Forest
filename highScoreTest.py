path = 'highScore.txt'

def highScore(path):
    def readsortScore(path):
        output = {}
        scoreFile = open(path, 'r')
        allScore = scoreFile.read()
        allScore = allScore.split(" ")
        counter = 0
        for value in allScore:
            if counter == 0:
                tempValue = value
                counter += 1
            elif counter == 1:
                output[tempValue] = int(value)
                counter = 0
                tempValue = ""
            #end of if   
        #end of for
        scoreFile.close()
        return(output)
    #end of readsortScore

    currentHighScore = readsortScore(path)
    currentScore = 6

    def sortHighScore(currentHighScore, currentScore):
        currentValues = list(currentHighScore.values())
        if currentScore > currentValues [2] and currentScore < currentValues[1]:
            currentValues[2] = currentScore
        elif currentScore > currentValues[1] and currentScore < currentValues[0]:
            currentValues[2] = currentValues[1]
            currentValues[1] = currentScore
        elif currentScore > currentValues[0]:
            currentValues[2] = currentValues[1]
            currentValues[1] = currentValues[0]
            currentValues[0] = currentScore
         #end of if
        return(currentValues)
    #end of sortHighScore


    currentValues = sortHighScore(currentHighScore, currentScore)

    def writeHighScore(currentValues, currentHighScore):
        scoreFile = open(path, 'w')
        scoreFile.truncate(0)
        currentKeys = list(currentHighScore.keys())
        for counter in range(3):
            scoreFile.write(str(currentKeys[counter]) + " ")
            scoreFile.write(str(currentValues[counter]) + " ")
        #end of for
        scoreFile.close()
    #end of def

    writeHighScore(currentValues, currentHighScore)
    
    return(list(currentHighScore.keys()), currentValues)
#end of highScore


player, score = (highScore(path))
