#!/usr/bin/env Rscript
library(doParallel)
library(caret)
library(survival)
library(plyr)
library(splines)
library(rjson)

# get location of SETTINGS.json
curDir = getwd()
parts = strsplit(curDir,"/")
parentDir = paste(parts[[1]][1:(length(parts[[1]])-1)],collapse="/")

# read in SETINGS.json: contains ROOT folder of repo
PATHS = fromJSON(paste(readLines(paste(parentDir,"SETTINGS.json",sep="/")), collapse=""))
print("Importing PATH Variables from SETTINGS.json...")

# build path to blocks folder
blockfolder = paste(PATHS$ROOT,"Features","blocks",sep="/")
# convert to platform independent path by replacing backslashes
blockfolder = gsub("\\\\","/",blockfolder)

#### main code ####

# it uses Tai's feature matricies created by Scott's code in blocks
# we only want to get to create by breakup_inputFile_3.py (which start with telematics)
drivers = list.files(paste(blockfolder,"features",sep="/"),pattern="^telematics")

allDrivers <- do.call("rbind", lapply(drivers, read.csv, header = TRUE))
allDrivers$DR <- NULL
registerDoParallel(4,cores=4)
for(i in 1:3700){
  tryCatch({
    print(paste("Driver",i))
    driver <- allDrivers[allDrivers$Driver==i,]
    driver$Driver <- "one"
    driver$trip <- NULL
    driver$Driver <- as.factor(driver$Driver)
    theRest <- allDrivers[allDrivers$Driver!=i,]
    theRest$Driver <- "zero"
    theRest$trip <- NULL
    theRest$Driver <- as.factor(theRest$Driver)
    inTraining <- createDataPartition(theRest$Driver, p = .005, list = FALSE)
    training <- rbind(driver, theRest[ inTraining,])
    #str(driver)
    set.seed(998)
    fitControl <- trainControl(## 10-fold CV
      method = "repeatedcv",
      number = 10,
      ## repeated three times
      repeats = 3)
    set.seed(825)
    gbmFit1 <- train(Driver ~ ., data = training,
                     method = "gbm",
                     trControl = fitControl,
                     ## This last option is actually one
                     ## for gbm() that passes through
                     verbose = FALSE)
    gbmFit1
    res <- predict(gbmFit1, newdata = driver, type = "prob")
    write.csv(res, file = paste(blockfolder,"results",i,".csv", sep=""))
  }, error = function(e) {
    print(e)
  }, finally = {} )
  
print("GBM in R completed...")
}