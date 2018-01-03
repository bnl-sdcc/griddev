mexample <- function(arg="") {
  cat("This runs a test using data files distributed with the archive\n")
  cat("It process sample files counts-20080303.txt and weather-20080303.txt,\n")
  cat("produce corresponding 30min average CSV files and the combined table CSV file.\n")
  cat("Look at code of the test (first function in manalysis.R) to see how it does that\n\n")

  cat("Reading counts file, producing counts_avg-20080303.csv...\n")
  mavgcounts("counts-20080303.txt","counts_avg-20080303.csv") # specifying time interval is optional
  cat("Reading weather file, producing weather_avg-20080303.csv...\n\n")
  mavgweather("weather-20080303.txt","weather_avg-20080303.csv")

  cat("Combining ct0, wt0 tables, producing couwea_avg-20080303.csv...\n\n")
  cwt1 <- mtbcomb2(ct0,wt0)
  mtbwrite(cwt1,"couwea_avg-20080303.csv")

  cat("Here are samples of produced ct1, wt1, cwt1 (combined) tables:\n")
  print(ct1[1:2,])
  print(wt1[1:2,])
  print(cwt1[1:2,])
  
}



mavgcounts <- function(file="data.dat",ofile="counts_avg.csv",interval=30) {
  ct0 <<- mreadcounts(file)
  ct1 <<- mtbcomb(ct0,interval) # by 30 min by default
  mtbwrite(ct1,ofile)
# mtbwrite(tb1,sub("\\..*","-av.txt",file))
# return(list(tb1,tb2))
}

mavgweather <- function(file="wdata.dat",ofile="weather_avg.csv",interval=30) {
  wt0 <<- mreadweather(file)
  wt1 <<- mtbcomb(wt0,interval) # by 30 min by default
  mtbwrite(wt1,ofile)
}


mtbwrite <- function(tab,file="mariachi.csv") {
  con <- file(file,open="wt")
  write.csv(tab,con,row.names=FALSE)
  close(con)
}

mreadcounts <- function(file) {
  colClas = "character"
  tab<-read.csv(file,header=FALSE,colClasses=colClas,nrows=10)

  if(tab[1,1] == "cts1.0") {
    #cat("counts file is recognized\n")
    colClas <- c("NULL","character","character",rep("integer",11))
    tab<-read.csv(file,header=FALSE,colClasses=colClas)
    tb1<-data.frame(date=ISOdatetime(substr(tab[,"V2"],1,4),substr(tab[,"V2"],5,6),substr(tab[,"V2"],7,8),
		    substr(tab[,"V3"],1,2),substr(tab[,"V3"],3,4),substr(tab[,"V3"],5,13),tz="GMT"),
		    tab[,3:13])    
  } else {
    #cat("John's web counts format is recognized\n")
    colClas <- c("character",rep("integer",11))
    tab<-read.csv(file,header=FALSE,colClasses=colClas)
    tb1<-data.frame(date=as.POSIXct(strptime(tab[,"V1"],"%F %H:%M:%OS",tz="GMT")),tab[2:12])
  }

  attr(tb1,"names") <- c("date","d1","d2","d3","d4","d5","c2","c3.1","c3.2","c3.3","c4.a","c5")
  return(tb1)

}

mreadweather <- function(file) {

# Skip the beginning ?

  colClas = "character"
  tab<-read.csv(file,strip.white=TRUE,header=FALSE,colClasses=colClas,blank.lines.skip=FALSE,nrows=10)
  nsk=0
  for(i in 1:ncol(tab)) {
    if(length(grep("^200.+",tab[i,1]))) {
    	nsk=i-1
        break
    }
  }

  cat("lines skiped: ",nsk,"\n")

# Reads all

  colClas <- c("character",rep(NA,13),"NULL")
  tab <- read.csv(file,skip=nsk,strip.white=TRUE,header=FALSE,comment.char="<",colClasses=colClas)
  #tim <- as.POSIXct(strptime(tab[,"V1"],"%F %H:%M:%OS",tz="")); attr(tim,"tzone") <- "GMT"
  tim <- as.POSIXct(strptime(tab[,"V1"],"%F %H:%M:%OS",tz=""))
  tb1 <- data.frame(date=tim,tab[2:ncol(tab)])
  attr(tb1,"names") <- c("date","TempF","DewpointF","PressIn","WindDir","WindDirDeg","WindSpMPH",
                         "WindSpGustMPH","Humi","HourlyPrecip","Conditions","Clouds","dailyrain","Software")

# Suppress not numeric columns

  tb2 <- data.frame(date=tb1[,"date"])
  for(i in 2:ncol(tb1)) {
    cls = class(tb1[1,i])
    nam = attr(tb1,"names")[i]
    if(cls =="numeric" | cls == "integer") {
	tb2 <- data.frame(tb2,tb1[,i])
	attr(tb2,"names")[ncol(tb2)] <- nam
    }
  }

  return(tb2)
}


mtbcomb <- function(tab,td=30) {

	dt = td*60 # averaging interval in seconds


	# find the start of an hour
	
	t0 <- tab$date[1]
	t1 <- as.POSIXlt(t0)
	t1$min <- 0
	t1$sec <- 0
	t1 <- as.POSIXct(t1)
	
	# what interval (from the beginning of an hour) we should start with
	
	frac <- (as.numeric(t0)-as.numeric(t1))/dt
	nf   <- round(frac) + 1
	
	# last interval
	
	t2   <- tab$date[nrow(tab)]
	frac <- (as.numeric(t2)-as.numeric(t1))/dt
	nl   <- round(frac)
	
	#print("nfirst, nlast")
	#print(c(nf,nl,t1,t2,t0,dt))
	#print(c(t1,t2,t0))
	
	tbn <- tab[FALSE,]
	if (nf<=nl) {
		for (i in nf:nl) {
		    b1 = t1 + (i-1)*dt
		    b2 = b1 + dt
		#    print(i)
		#    print(c(b1,b2))
		#    print(tab[b1<=tab$date & tab$date<b2,1:2])
		    tba <- data.frame(b1+dt/2,rbind(apply(tab[(b1<=tab$date)&(tab$date<b2),2:ncol(tab)],2,mean)))
		    attr(tba,"names") <- attr(tbn,"names")
		    tbn <- rbind(tbn,tba)
	  	}
	}
	return(tbn)

}


mtbcomb2 <- function(tab,wtb,td=30) {
	dt = td*60 # averaging interval in seconds
	
	# find the start of an hour
	t0 <- tab$date[1]
	t1 <- as.POSIXlt(t0)
	t1$min <- 0
	t1$sec <- 0
	t1 <- as.POSIXct(t1)
	
	# what interval (from the beginning of an hour) we should start with
	frac <- (as.numeric(t0)-as.numeric(t1))/dt
	nf   <- round(frac) + 1
	
	# last interval
	
	t2   <- tab$date[nrow(tab)]
	frac <- (as.numeric(t2)-as.numeric(t1))/dt
	nl   <- round(frac)
	
	tbn <- data.frame(tab[FALSE,],wtb[FALSE,2:ncol(wtb)])
	if (nf<=nl) {
	  for (i in nf:nl) {
	    b1 = t1 + (i-1)*dt
	    b2 = b1 + dt
	
	    tba <- data.frame(b1+dt/2,rbind(apply(tab[(b1<=tab$date)&(tab$date<b2),2:ncol(tab)],2,mean)),
	                              rbind(apply(wtb[(b1<=wtb$date)&(wtb$date<b2),2:ncol(wtb)],2,mean)))
	    attr(tba,"names") <- attr(tbn,"names")
	    tbn <- rbind(tbn,tba)
	    
	  }
	}
	return(tbn)
}

mavgboth <- function(cfile="data.dat",wfile="wdata.dat",ofile="mariachi.csv",td=30) {
	tb1 <- mreadcounts(cfile)
	tb2 <- mreadweather(wfile)
	tbres <- mtbcomb2(tb1, tb2, td)
	mtbwrite(tbres,ofile)	
}


# "Experimental" functions

mreadstd <- function() {
    colClas <- c("NULL","character","character",rep("integer",11))
    tab<-read.csv(stdin(),header=FALSE,colClasses=colClas)
    write.csv(tab[1:10,],"a.csv",row.names=FALSE)
}


