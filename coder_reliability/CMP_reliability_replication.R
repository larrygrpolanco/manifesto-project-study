####################################################################################
# Slava Mikhaylov, Kenneth Benoit, and Michael Laver
# "Coder Reliability and Misclassification in the Human Coding of Party Manifestos"
# Political Analysis replication materials
#
# Requires: mds2005f.dta (CMP dataset)
#           master-codersGB.txt
#           codes.log
#           master-coderNZ.txt
#           codesNZ.log
#
####################################################################################

graphics.off()

## load needed libraries
require(foreign)
require(Hmisc)
require(irr)
require(ade4)
require(boot)
require(psy)
require(simex)


######## READ IN AND PROCESS BRITAIN MANIFESTO ########

rawdata.gb <- rbind(read.delim("master-codersGB.txt", header=F, as.is=c(1:3,5:7)),
                    read.delim("codes.log", header=F, as.is=c(1:3,5:7))[,-116])
# assign column names
names(rawdata.gb)[1:8] <- c("ip", "date", "time", "id", "name", "email",
                       "insttn", "experience") 
# make row names the same as first part of e-mail
rawdata.gb$email[33] <- "goreckim2"
for (i in 1:nrow(rawdata.gb)) {
    atsign.position <- as.numeric(substring.location(rawdata.gb$email[i], "@")[1])
  if (atsign.position>0) {
    rownames(rawdata.gb)[i] <- substr(rawdata.gb$email[i], 1, atsign.position-1)
  } else {
    rownames(rawdata.gb)[i] <- rawdata.gb$email[i]
  }
}
# Can drop coders here
codershort <- rownames(rawdata.gb)
coders.to.drop.gb <- which(codershort=="doherta" |
                           codershort=="careydp" |
                           codershort=="doherta" |
                           codershort=="careydp" |
                           codershort=="njokur" |
                           codershort=="headonc" |
                           codershort=="rutherfc" |
                           codershort=="saula" |
                           codershort=="lukaszek" |
                           codershort=="campbeca" |
                           codershort=="ligita_sarkute" |
                           codershort=="daublert" |
                           codershort=="goreckim" |
                           codershort=="kbenoit" |
                           codershort=="mikhailv" |
                           codershort=="sudulicm" |
                           codershort=="fedoreae" )
selected.gb <- rawdata.gb[-coders.to.drop.gb,]
# transpose so that coders are in columns
codings.gb <- t(selected.gb[,9:ncol(selected.gb)])
rownames(codings.gb)[1:nrow(codings.gb)] <- paste("qs",1:nrow(codings.gb), sep="")

## CODER RELIABILITY SCORES VERSUS MASTER: BRITAIN
kappa.rater.gb <- data.frame(coder=names(as.data.frame(codings.gb))[2:ncol(codings.gb)],
                             kappa=matrix(NA, nrow=ncol(codings.gb)-1),
                             kappa.se=matrix(NA, nrow=ncol(codings.gb)-1))

## ckappa.boot <- function(data,x) {ckappa(data[x,])$kappa}
kappa2.boot <- function(data,x) {kappa2(data[x,])$value}

for (i in 2:ncol(codings.gb)) {
  # kappa.rater.gb$kappa[i-1] <- kappa2(codings.gb[,c(1,i)])$value
  res <- boot(codings.gb[,c(1,i)], kappa2.boot, 100)
  kappa.rater.gb$kappa[i-1] <- res$t0
  kappa.rater.gb$kappa.se[i-1] <- sd(res$t)  
}
kappa.rater.gb <- cbind(previous=rawdata.gb[c(-1,-coders.to.drop.gb),8], kappa.rater.gb)
# kappa.rater.gb[order(kappa.rater.gb$kappa, decreasing=T),]

## CODER RELIABILITY BY CATEGORY
#kappam.fleiss(codings.gb[,2:ncol(codings.gb)], detail=T)

fkappa.boot <- function(data,x) {kappam.fleiss(data[x,])$value}
res <- boot(codings.gb[,2:ncol(codings.gb)], fkappa.boot, 100)

quantile(res$t,c(0.025,0.5,0.975))


######## READ IN AND PROCESS NEW ZEALAND MANIFESTO ########

rawdata.nz <- rbind(read.delim("master-codersNZ.txt", header=F, as.is=c(1:3,5:7)),
                    read.delim("codesNZ.log", header=F, as.is=c(1:3,5:7))[,-81])
# assign column names
names(rawdata.nz)[1:8] <- c("ip", "date", "time", "id", "name", "email",
                       "insttn", "experience") 
# make row names the same as first part of e-mail
for (i in 1:nrow(rawdata.nz)) {
    atsign.position <- as.numeric(substring.location(rawdata.nz$email[i], "@")[1])
  if (atsign.position>0) {
    dimnames(rawdata.nz)[[1]][i] <- substr(rawdata.nz$email[i], 1, atsign.position-1)
  } else {
    dimnames(rawdata.nz)[[1]][i] <- rawdata.nz$email[i]
  }
}
rawdata.nz$email[rawdata.nz$email=="ligita_sarkute"] <- "ligita_sarkute.NZ"
rawdata.nz$email[rawdata.nz$email=="mikhailv"] <- "mikhailv.NZ"
# Can drop coders here
codershort <- rownames(rawdata.nz)
coders.to.drop.nz <- which(codershort=="sgilliga" |
                           codershort=="carroljm" |
                           codershort=="corleymi" |
                           codershort=="mcnamaco" |
                           codershort=="farrelsk" |
                           codershort=="mrwillia" |
                           codershort=="ligita_sarkute" |
                           codershort=="kenneth.mcdonagh" |
                           codershort=="martinh" |
                           codershort=="kbenoit" |
                           codershort=="mikhailv" |
                           codershort=="kaczmara" )
selected.nz <- rawdata.nz[-coders.to.drop.nz,]
# transpose so that coders are in columns
codings.nz <- t(selected.nz[,9:ncol(selected.nz)])
rownames(codings.nz)[1:nrow(codings.nz)] <- paste("qs",1:nrow(codings.nz), sep="")

## CODER RELIABILITY SCORES VERSUS MASTER: NEW ZEALAND
kappa.rater.nz <- data.frame(coder=names(as.data.frame(codings.nz))[2:ncol(codings.nz)],
                             kappa=matrix(NA, nrow=ncol(codings.nz)-1))
for (i in 2:ncol(codings.nz)) {
  kappa.rater.nz$kappa[i-1] <- kappa2(codings.nz[,c(1,i)])$value
}
kappa.rater.nz <- cbind(previous=rawdata.nz[c(-1,-coders.to.drop.nz),8], kappa.rater.nz)
#kappa.rater.nz[order(kappa.rater.nz$kappa, decreasing=T),]

## CODER RELIABILITY BY CATEGORY
#kappam.fleiss(codings.nz[,2:ncol(codings.nz)], detail=T)



########################################################
## FIGURE 1: PLOT HISTOGRAMS OF KAPPA CODERS V MASTER ##     
########################################################
nrow(kappa.rater.nz)
nrow(kappa.rater.gb)
quartz(width=10,height=5)
par(mfrow=c(1,2))
hist(kappa.rater.gb$kappa, breaks=10, xlim=c(0,1), col="gray70",
     xlab="Cohen's Kappa Tester v. Master (n=17)", main="Britain", cex.lab=1.2)
abline(v=.8, lty="dashed", col="red")
abline(v=median(kappa.rater.gb$kappa), lwd=2)
hist(kappa.rater.nz$kappa, breaks=10, xlim=c(0,1), col="gray70",
     xlab="Cohen's Kappa Tester v. Master (n=12)", main="New Zealand", cex.lab=1.2)
abline(v=.8, lty="dashed", col="red")
abline(v=median(kappa.rater.nz$kappa), lwd=2)
par(mfrow=c(1,1))



########  RESHAPE coding matrixes into long format, to be combined ##########

# new zealand
df.nz <- as.data.frame(codings.nz)
long.nz <- reshape(df.nz, idvar="qs.no", ids=translate(row.names(df.nz),"qs",""),
                   times=names(df.nz[,-1]), timevar="id.Tester",
                   varying=list(names(df.nz[,-1])), direction="long")
names(long.nz)[c(1,3)] <- c("code.MASTER", "code.Tester")
# britain
df.gb <- as.data.frame(codings.gb)
long.gb <- reshape(df.gb, idvar="qs.no", ids=translate(row.names(df.gb),"qs",""),
                   times=names(df.gb[,-1]), timevar="id.Tester",
                   varying=list(names(df.gb[,-1])), direction="long")
names(long.gb)[c(1,3)] <- c("code.MASTER", "code.Tester")

long.nz <- cbind(long.nz, data.frame(rep("nz",nrow(long.nz))))
names(long.nz)[5] <- "country"        
long.gb <- cbind(long.gb, data.frame(rep("gb",nrow(long.gb))))
names(long.gb)[5] <- "country"        


# Combine the two long format files to generate misclassification matrix
long.comb <- rbind(long.gb, long.nz)
# empirical misclassification matrix
mc.full <- table(long.comb$code.MASTER, long.comb$code.Tester)

# new varable: rilecat.* where 0=neither 1=left 2=right
rilecat.MASTER <- rilecat.Tester <- rep(0,nrow(long.comb))
1 -> rilecat.MASTER[long.comb$code.MASTER==103 |
                    long.comb$code.MASTER==105 |
                    long.comb$code.MASTER==106 |
                    long.comb$code.MASTER==107 |
                    long.comb$code.MASTER==202 |
                    long.comb$code.MASTER==403 |
                    long.comb$code.MASTER==404 |
                    long.comb$code.MASTER==406 |
                    long.comb$code.MASTER==412 |
                    long.comb$code.MASTER==413 |
                    long.comb$code.MASTER==504 |
                    long.comb$code.MASTER==506 |
                    long.comb$code.MASTER==701]
2 -> rilecat.MASTER[long.comb$code.MASTER==104 |
                    long.comb$code.MASTER==201 |
                    long.comb$code.MASTER==203 |
                    long.comb$code.MASTER==305 |
                    long.comb$code.MASTER==401 |
                    long.comb$code.MASTER==402 |
                    long.comb$code.MASTER==407 |
                    long.comb$code.MASTER==414 |
                    long.comb$code.MASTER==505 |
                    long.comb$code.MASTER==601 |
                    long.comb$code.MASTER==603 |
                    long.comb$code.MASTER==605 |
                    long.comb$code.MASTER==606]
1 -> rilecat.Tester[long.comb$code.Tester==103 |
                    long.comb$code.Tester==105 |
                    long.comb$code.Tester==106 |
                    long.comb$code.Tester==107 |
                    long.comb$code.Tester==202 |
                    long.comb$code.Tester==403 |
                    long.comb$code.Tester==404 |
                    long.comb$code.Tester==406 |
                    long.comb$code.Tester==412 |
                    long.comb$code.Tester==413 |
                    long.comb$code.Tester==504 |
                    long.comb$code.Tester==506 |
                    long.comb$code.Tester==701]
2 -> rilecat.Tester[long.comb$code.Tester==104 |
                    long.comb$code.Tester==201 |
                    long.comb$code.Tester==203 |
                    long.comb$code.Tester==305 |
                    long.comb$code.Tester==401 |
                    long.comb$code.Tester==402 |
                    long.comb$code.Tester==407 |
                    long.comb$code.Tester==414 |
                    long.comb$code.Tester==505 |
                    long.comb$code.Tester==601 |
                    long.comb$code.Tester==603 |
                    long.comb$code.Tester==605 |
                    long.comb$code.Tester==606]
long.comb2 <- data.frame(cbind(long.comb,
                               factor(rilecat.MASTER, labels=c("none","left","right")),
                               factor(rilecat.Tester, labels=c("none","left","right"))))
names(long.comb2)[6:7] <- c("rilecat.MASTER", "rilecat.Tester")


############################################
## TABLE 3: RILE MISCLASSIFICATION MATRIX ## 
############################################
(mc.lro <- table(long.comb2$rilecat.MASTER, long.comb2$rilecat.Tester))
prop.table(mc.lro, 1)


############################
## FIGURE 2: TERNARY PLOT ## 
############################
# TRIANGLE PLOT of l-r-o differences
quartz(width=8,height=8)
t <- data.frame(mc.lro[,c(2,1,3)])
row.names(t) <- c("LEFT","Other","RIGHT")
names(t) <- c("Coded Left", "Coded Other", "Coded Right")
tplot.lro <- triangle.plot(t, show.position=F, scale=F, cpoint=2)
text(c(-.13,.35,.05), c(-.28,-.22,.35), row.names(t),
     cex=1.2, col=c("darkred","gray40","darkblue"))

quartz(width=9,height=9)
t.left <- table(subset(long.comb2$code.MASTER,
                       long.comb2$rilecat.MASTER=="left"), 
                subset(long.comb2$rilecat.Tester,
                       long.comb2$rilecat.MASTER=="left"))
t.right <- table(subset(long.comb2$code.MASTER,
                        long.comb2$rilecat.MASTER=="right"), 
                 subset(long.comb2$rilecat.Tester,
                        long.comb2$rilecat.MASTER=="right"))
t.none <- table(subset(long.comb2$code.MASTER,
                       long.comb2$rilecat.MASTER=="none"), 
                subset(long.comb2$rilecat.Tester,
                       long.comb2$rilecat.MASTER=="none"))
dt <- data.frame(t.none[,c(2,1,3)])
names(dt) <- c("Coded\ as\ Left", "Coded\ as\ Other", "Coded\ as\ Right")                 

tplot.left <- triangle.plot(t.left[,c(2,1,3)], show.position=F, scale=F, cpoint=0)
tplot.right <- triangle.plot(t.right[,c(2,1,3)], show.position=F, scale=F, cpoint=0)
tplot.none <- triangle.plot(dt, show.position=FALSE, scale=FALSE, cpoint=0, draw.line=FALSE)
text(tplot.left+.02, paste("L",rownames(t.left),sep=""),  cex=1.1)
text(tplot.right, paste("r",rownames(t.right),sep=""), cex=1.1, font=2)
rownames(t.none)[1] <- "Uncoded"
text(tplot.none+.02, paste("",rownames(t.none),sep=""), col="gray40", cex=.95, font=3)
points(tplot.lro, pch=16, col=c("gray40","black","black"))
points(tplot.lro, pch=1, col=c("gray40","black","black"), cex=2.2)
text(tplot.lro + matrix(c(-.08,-.05,-.06,.03,.04,-.04), ncol=2), c("OTHER","LEFT","RIGHT"), col=c("gray40","black","black"),cex=.9)
                            


#########################
## TABLE 2 KAPPA STATS ##
#########################
## British manifesto by category
kappam.fleiss(codings.gb[,2:ncol(codings.gb)])
## NZ manifesto by category
kappam.fleiss(codings.nz[,2:ncol(codings.nz)])
## British manifesto by RILE
kappam.fleiss(subsample.gb[,5:ncol(subsample.gb)])
## NA manifesto by RILE
kappam.fleiss(subsample.nz[,5:ncol(subsample.nz)])


###########################################
## FIGURE 3: SIMULATED MISCLASSIFICATION ##  
###########################################
###### Prepare data for MATRIX METHOD TO UNDO MISCLASSIFICATION ######
###### Kuha and Skinner 1997 ######

mc.lro
cat("These are the true frequencies")
prop.table(apply(mc.lro,1,sum))
theta.lro <- t(as.matrix(prop.table(mc.lro,1)))

cat("These are the observed frequencies")
(pastar <- prop.table(apply(mc.lro,2,sum)))

cat("The identity yields the reverse:")
solve(theta.lro) %*% pastar

cmpdata <- read.dta("mds2005f.dta")
# convert missing data code to NA
cmpdata$peruncod[round(cmpdata$peruncod,2)==99.99] <- NA
cmpdata$total[round(cmpdata$total,0)==9999] <- NA
# drop all cases with missing TOTAl or PERUNCOD
cmpdata <- subset(cmpdata, !is.na(cmpdata$total) & !is.na(cmpdata$peruncod))
# select out cases which are extended cats
extendedcats <- apply(cmpdata[,86:139],1,sum)
sum(extendedcats>0)
cmpdata <- cmpdata[!extendedcats,]
rile.index.left <- names(cmpdata) %in%
      paste("per", c(103,105:107,202,403,404,406,412,413,504,506,701), sep="")
rile.index.right <- names(cmpdata) %in%
      paste("per", c(104,201,203,305,401,402,407,414,505,601,603,605,606), sep="")
rile.index.none <- ((which((names(cmpdata)!=""))>=30) &
                    !rile.index.right & !rile.index.left &
		    (which((names(cmpdata)!=""))<=85) | 
		    (names(cmpdata)=="peruncod"))
per.rile.right <- apply(cmpdata[,rile.index.right],1,sum)
per.rile.left <- apply(cmpdata[,rile.index.left],1,sum)
per.rile.none <- apply(cmpdata[,rile.index.none],1,sum)

per.rile.df <- data.frame(cmpdata[,c(1,6,9,141)], per.right = per.rile.right,
                          per.left = per.rile.left, per.none = per.rile.none)

plot(apply(per.rile.df[,5:7],1,sum))

per.rile.corrected <- solve(theta.lro) %*% t(per.rile.df[,5:7])
rile.corrected <- per.rile.corrected[1,] - per.rile.corrected[2,]

<require(simex)
i.rile <- seq(0,50,length.out=51)

quartz(width=12,height=18)
par(mfrow=c(2,2))
reps <- 8
jf <-.03
df <- data.frame(rile=seq(-50,50,2),
                 other=rep(50,51),
                 left=rev(i.rile),
                 right=i.rile)
for (i in 1:reps) df[,ncol(df)+1]<-rep(NA,51)
names(df)[5:(5+reps-1)] <- paste(rep("rep"),1:reps,sep=".")


######################################## NOW for .90 reliability
mc.lro.90 <- matrix(c(48,1,1,1,23,1,1,1,23), nrow=3, ncol=3,
                    dimnames=list(c("none","left","right"),
                      c("none","left","right")))
mean.kappa.overall <- rep(NA,51)
for (i in 1:51) {
  # create and fill the temporary category vector tmp.x
  tmp.x <- factor(rep(1:3,length.out=100), labels=c("none","left","right"))
  tmp.x[1:50] <- "none"
  if (df$left[i] != 0) tmp.x[51:(51+df$left[i])] <- "left"
  if (df$right[i] != 0)
    tmp.x[(51+df$left[i]):(51+df$left[i]+df$right[i])] <- "right"
  
  # apply the misclassification 10 times to each rile setting 
  mean.kappa <- rep(NA,reps)
  for (j in 1:reps) {
    tmp.df <- misclass(data.frame(x=tmp.x), list(x=mc.lro.90), 1)
    mean.kappa[j] <- kappa2(cbind(tmp.x,tmp.df$x))$value
    df[i,4+j] <- as.numeric(table(tmp.df)[3] - table(tmp.df)[2])
  }
  mean.kappa.overall[i] <- mean(mean.kappa)
#  cat("Rile = ", df[i,1], ", Mean kappa = ", mean(mean.kappa), "\n")
}
summary(mean.kappa.overall)
# reshape the wide matrix to long format
df.long <- reshape(df, idvar=c("rile"), varying=list(5:(5+reps-1)),
               v.names="rep", direction="long")
#### PLOT the simulated misclassified versus the "true" rile
par(mar=c(5,5.5,2,2)+0.1)
plot(jitter(df.long$rile), df.long$rep,
     xlab="True \"rile\" score",
     ylab="\"rile\" score with misclassification", cex.lab=1.3,
     xlim=c(-50,50), ylim=c(-50,50), type="n",
     main="Reliability of kappa=.90, symmetric errors")
abline(v=0, h=0, col="gray90")
points(jitter(df.long$rile,jf), df.long$rep)
abline(0,1, lty="dashed", lwd=1.5)
abline(lm(df.long$rep~df.long$rile), col="darkred")
abline(v=0, h=0, col="gray90")


######################################## NOW for .70 reliability
mc.lro.90 <- matrix(c(44,3,3,3,19,3,3,3,19), nrow=3, ncol=3,
                    dimnames=list(c("none","left","right"),
                      c("none","left","right")))
mean.kappa.overall <- rep(NA,51)
for (i in 1:51) {
  # create and fill the temporary category vector tmp.x
  tmp.x <- factor(rep(1:3,length.out=100), labels=c("none","left","right"))
  tmp.x[1:50] <- "none"
  if (df$left[i] != 0) tmp.x[51:(51+df$left[i])] <- "left"
  if (df$right[i] != 0)
    tmp.x[(51+df$left[i]):(51+df$left[i]+df$right[i])] <- "right"
  
  # apply the misclassification reps times to each rile setting 
  mean.kappa <- rep(NA,reps)
  for (j in 1:reps) {
    tmp.df <- misclass(data.frame(x=tmp.x), list(x=mc.lro.90), 1)
    mean.kappa[j] <- kappa2(cbind(tmp.x,tmp.df$x))$value
    df[i,4+j] <- as.numeric(table(tmp.df)[3] - table(tmp.df)[2])
  }
  mean.kappa.overall[i] <- mean(mean.kappa)
#  cat("Rile = ", df[i,1], ", Mean kappa = ", mean(mean.kappa), "\n")
}
summary(mean.kappa.overall)
# reshape the wide matrix to long format
df.long <- reshape(df, idvar=c("rile"), varying=list(5:(5+reps-1)),
               v.names="rep", direction="long")
#### PLOT the simulated misclassified versus the "true" rile
par(mar=c(5,5.5,2,2)+0.1)
plot(jitter(df.long$rile), df.long$rep,
     xlab="True \"rile\" score",
     ylab="\"rile\" score with misclassification", cex.lab=1.3,
     xlim=c(-50,50), ylim=c(-50,50), type="n",
     main="Reliability of kappa=.70, symmetric errors")
abline(v=0, h=0, col="gray90")
points(jitter(df.long$rile,jf), df.long$rep)
abline(0,1, lty="dashed", lwd=1.5)
abline(lm(df.long$rep~df.long$rile), col="darkred")
abline(v=0, h=0, col="gray90")



######################################## NOW for .50 reliability
mc.lro.90 <- matrix(c(0.820,0.19,0.19,0.09,0.62,0.19,0.09,0.19,0.62), nrow=3, ncol=3,
                    dimnames=list(c("none","left","right"),
                      c("none","left","right")))
    
mean.kappa.overall <- rep(NA,51)
for (i in 1:51) {
  # create and fill the temporary category vector tmp.x
  tmp.x <- factor(rep(1:3,length.out=100), labels=c("none","left","right"))
  tmp.x[1:50] <- "none"
  if (df$left[i] != 0) tmp.x[51:(51+df$left[i])] <- "left"
  if (df$right[i] != 0)
    tmp.x[(51+df$left[i]):(51+df$left[i]+df$right[i])] <- "right"
  
  # apply the misclassification reps times to each rile setting 
  mean.kappa <- rep(NA,reps)
  for (j in 1:reps) {
    tmp.df <- misclass(data.frame(x=tmp.x), list(x=mc.lro.90), 1)
    mean.kappa[j] <- kappa2(cbind(tmp.x,tmp.df$x))$value
    df[i,4+j] <- as.numeric(table(tmp.df)[3] - table(tmp.df)[2])
  }
  mean.kappa.overall[i] <- mean(mean.kappa)
#  cat("Rile = ", df[i,1], ", Mean kappa = ", mean(mean.kappa), "\n")
}
summary(mean.kappa.overall)
# reshape the wide matrix to long format
df.long <- reshape(df, idvar=c("rile"), varying=list(5:(5+reps-1)),
               v.names="rep", direction="long")
#### PLOT the simulated misclassified versus the "true" rile
par(mar=c(5,5.5,2,2)+0.1)
plot(jitter(df.long$rile), df.long$rep,
     xlab="True \"rile\" score",
     ylab="\"rile\" score with misclassification", cex.lab=1.3,
     xlim=c(-50,50), ylim=c(-50,50), type="n",
     main="Reliability of kappa=.50, symmetric errors")
abline(v=0, h=0, col="gray90")
points(jitter(df.long$rile,jf), df.long$rep)
abline(0,1, lty="dashed", lwd=1.5)
abline(lm(df.long$rep~df.long$rile), col="darkred")
abline(v=0, h=0, col="gray90")


######################################## NOW for Empirical reliability
mean.kappa.overall <- rep(NA,51)
for (i in 1:51) {
  # create and fill the temporary category vector tmp.x
  tmp.x <- factor(rep(1:3,length.out=100), labels=c("none","left","right"))
  tmp.x[1:50] <- "none"
  if (df$left[i] != 0) tmp.x[51:(51+df$left[i])] <- "left"
  if (df$right[i] != 0)
    tmp.x[(51+df$left[i]):(51+df$left[i]+df$right[i])] <- "right"
  
  # apply the misclassification reps times to each rile setting 
  mean.kappa <- rep(NA,reps)
  for (j in 1:reps) {
    tmp.df <- misclass(data.frame(x=tmp.x), list(x=mc.lro), 1)
    mean.kappa[j] <- kappa2(cbind(tmp.x,tmp.df$x))$value
    df[i,4+j] <- as.numeric(table(tmp.df)[3] - table(tmp.df)[2])
  }
  mean.kappa.overall[i] <- mean(mean.kappa)
  # cat("Rile = ", df[i,1], ", Mean kappa = ", mean(mean.kappa), "\n")
}
summary(mean.kappa.overall)

# reshape the wide matrix to long format
df.long <- reshape(df, idvar=c("rile"), varying=list(5:(5+reps-1)),
               v.names="rep", direction="long")
#### PLOT the simulated misclassified versus the "true" rile
plot(jitter(df.long$rile,jf), df.long$rep,
     xlab="True \"rile\" score",
     ylab="\"rile\" score with misclassification", cex.lab=1.3,
     xlim=c(-50,50), ylim=c(-50,50), type="n",
     main="Test Reliability of kappa=.47, asymmetric errors")
abline(v=0, h=0, col="gray90")
points(jitter(df.long$rile), df.long$rep)
abline(0,1, lty="dashed", lwd=1.5)
abline(lm(df.long$rep~df.long$rile), col="darkred")
abline(v=0, h=0, col="gray90")

