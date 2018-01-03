#
# Submit batch as
#    R CMD BATCH --vanilla '--args 4 20' analysis.R &
#
#
# Initialize months 
#
   months = c("January","February","March","April","May","June","July",
              "August","September","October","November","December")

#  get arguments from command line and extract the two last entries
#
   args  <- commandArgs()
   n     <- length(args)
   nday  <- as.numeric(args[n])
   nmon  <- as.numeric(args[n-1])
#
   MO    <- months[nmon]

# -> Load libraries required for wav file manipulation

   library(sound)
   library(seewave)

#
# -> read the table of scintillator events 
#
   filesci <- paste(MO,"/","datasachem",toString(nday),".txt",sep="")
   tsci <- read.table(filesci)
   tsec <- tsci[,5]*60 + tsci[,6]
   totalpoints <- length(tsec)
   heure <- -1
   radar <- c(1,2)
#
#
   for ( n in 1:totalpoints)
   {
     if( tsci[n,4] > heure) # files are recorded on hourly basis
       {
         jour  <- toString(tsci[n,4])
         if (tsci[n,4] < 10) jour <- paste("0",jour,sep="")
         heure <- tsci[n,4]
         filename <- paste("/data/custer/",MO,"/",toString(tsci[n,3]),
                  "/WCU0804",toString(tsci[n,3]),jour,"U.wav",sep="")
         rm(radar)
         gc(TRUE)  # not sure if we need garbage collection
         radar <- loadSample(filename)
         rradar  <- rate(radar)
         rlength <- sampleLength(radar)
       }

     if(tsec[n] <= 3480) # files are 59 minutes long, protect for that
       {
        tlow  <-  tsec[n] - 0.5
        thig  <-  tsec[n] + 0.5
        nlow  <-  as.integer(tlow*rradar)
        nhig  <-  as.integer(thig*rradar)
        if ((nlow < nhig)&&(nlow>0)&&(nhig>0)&&(nhig<rlength) )  # only if within boundaries
           {
           wtemp <- radar[1+nlow:nhig]
           filen <-  paste(MO,"/",toString(nday),"/w",toString(n),".wav",sep="")
           saveSample(wtemp,filen,overwrite=TRUE)
           rm(wtemp)
           gc(TRUE)
           }
       }
   } #end of for loop for all scintillator events

# process each frame and produce summary file
# produce suggested list of hits

#
#  Get list of all files in the directory
#
   dirname <- paste("./",MO,"/",toString(nday),sep="")
   dirlist <- list.files(dirname) 
#
   timeaxis <- seq(1,1102)   # connected to msmooth so be carefull
   timeaxis <- (timeaxis*1/1102) - 0.5
#
#
   summary <- c()
   pdfname = paste(MO,"/","RadarCuts",toString(nday),".pdf",sep="")
   pdf(pdfname)
   par(mfrow=c(2,2))
   for( n in 1:length(dirlist))
   {
     radarfilename <- paste(MO,"/",toString(nday),"/",dirlist[n],sep="")
     radar <- loadSample(radarfilename)
     radarleft  <- left(radar)
     radarright <- right(radar)
#
     ampleft    <- env(radarleft,envt="abs",msmooth=c(20,0),plot=F)
     ampright   <- env(radarright,envt="abs",msmooth=c(20,0),plot=F)
#
     peakleft   <- max(ampleft)
     peakright  <- max(ampright)
     meanleft   <- mean(ampleft)
     sdleft     <- sd(ampleft)
     meanright  <- mean(ampright)
     sdright    <- sd(ampright)
     bitleft    <- ampleft>0.04
     bitright   <- ampright>0.04
     aboveleft  <- sum(bitleft)
     aboveright <- sum(bitright)
     sumleft    <- sum(bitleft*ampleft)
     sumright   <- sum(bitright*ampright)
     wavno      <- as.numeric(substr(radarfilename,11,(nchar(radarfilename)-4)))

     summary <- c(summary,peakleft,peakright,meanleft,sdleft,meanright,sdright,aboveleft,aboveright,sumleft,sumright,wavno)
#
     plot(timeaxis,ampleft,main=dirlist[n],ylim=c(0,0.1),type="s",xlab="t(s)")
     plot(timeaxis,ampright,main=dirlist[n],ylim=c(0,0.1),type="s",xlab="t(s)")
#
     rm(radar)
   }

   dev.off()
#
    sumfilename <- paste(MO,"/summary",toString(nday),".txt",sep="")
    table <- data.frame( matrix( summary, ncol=11, byrow=T ) )
    write.table(table,file=sumfilename,quote=FALSE,row.names=FALSE,col.names=FALSE)  
#
#
    table <- read.table(sumfilename)
    index  <- seq(1,length(table$V7))
    ind    <- index[(table$V1/table$V3)>6&table$V7<20]
    frames <- table$V11[(table$V1/table$V3)>6&table$V7<20]
#
#
    hits   <- c()
    for (k in 1:length(ind))
    {
       status <- "Bronze"
       nk     <-   ind[k]
       ni     <-   frames[k]
       ratio  <-   table[nk,1]/table[nk,3]
       print(ratio)
       if (ratio > 10 ) status = "Silver"
       if (ratio > 15 ) status = "Gold"
       hits <- c(hits,nk,ni,tsci[ni,1],tsci[ni,2],tsci[ni,3],tsci[ni,4],
                 tsci[ni,5],tsci[ni,6],ratio,status)
    }

    sfn <- paste(MO,"/shortlist",toString(nday),".txt",sep="")
    tabua <- data.frame( matrix( hits, ncol=10, byrow=T ) )
    write.table(tabua,file=sfn,quote=FALSE,row.names=FALSE,col.names=FALSE)  

#
#  If you get here, this is the [END]
#
