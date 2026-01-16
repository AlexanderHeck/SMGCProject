#Script: TableAnalysis.R

#This is an script for the analysis of the results table of the count of secondary metabolite gene
#clusters

#first load all required libraries

library(MASS)        
library(ggplot2)
library(dplyr)
library(readxl)
library(emmeans)
library(ggsignif)

#import Dataset
SecondMetaProjectsResults <- read_excel("SecondMetaProjectsResults.xlsx")

#exlcude all rows where no genome was found
SecondMetaProjectsResults<-SecondMetaProjectsResults[SecondMetaProjectsResults$Total_Clusters!=0,]

# explore the data using histograms
ggplot(SecondMetaProjectsResults, aes(x = Total_Clusters)) + geom_histogram(binwidth=1) + labs(title="Total clusters")
ggplot(SecondMetaProjectsResults, aes(x = Terpene)) + geom_histogram(binwidth=1) + labs(title="Terpenes")
ggplot(SecondMetaProjectsResults, aes(x = NRPS)) + geom_histogram(binwidth=1) + labs(title="NRPSs")
ggplot(SecondMetaProjectsResults, aes(x = PKS)) + geom_histogram(binwidth=1) + labs(title="PKSs")


### In the following all statistical tests can be found ###

## Total number of clusters dependent on genome size ##

mTotalpersize<- glm(Total_Clusters ~ size_Mb, family = poisson(link="log"), data = SecondMetaProjectsResults)
summary(mTotalpersize) #slightly overdispersed
mnbTotalpersize<- glm.nb( Total_Clusters ~ size_Mb, data = SecondMetaProjectsResults)
summary(mnbTotalpersize) #slightly overdispersed
hist(residuals(mnbTotalpersize))

# create sequence of x values for a smooth curve
simdat <- data.frame(size_Mb = seq(min(SecondMetaProjectsResults$size_Mb),max(SecondMetaProjectsResults$size_Mb),length.out = 200))

# predicted mean on original scale (log link → exp)
simdat$pred <- predict(mnbTotalpersize, newdata = simdat, type = "response")

# create final plot
ggplot(SecondMetaProjectsResults, aes(x = size_Mb, y = Total_Clusters, colour = Decay_type)) +
  geom_point() +
  geom_line(data = simdat, aes(x = size_Mb, y = pred), color = "black", linewidth = 0.5) +
  labs(x='Genome Size [Mb]', y='Total Number of Clusters', title = 'Total Number of Clusters dependent on Genome Size', color = 'Decay type') +
  theme_light()
  

## Number of clusters dependent on decay type ##

# Total SMGCs per decay type
mTotal <- glm( Total_Clusters ~ Decay_type, family = poisson(link="log"), data = SecondMetaProjectsResults)
summary(mTotal)
hist(residuals(mTotal))
mnbTotal<- glm.nb(Total_Clusters ~ Decay_type ,data = SecondMetaProjectsResults)
summary(mnbTotal)
hist(residuals(mnbTotal))
ggplot(SecondMetaProjectsResults, aes(x = Decay_type, y = Total_Clusters))+
  geom_boxplot()

# Terpenes per decay type
mTerpene <- glm( Terpene ~ Decay_type, family = poisson(link="log"), data = SecondMetaProjectsResults)
summary(mTerpene)
hist(residuals(mTerpene))
mnbTerpene<- glm.nb(Terpene ~ Decay_type ,data = SecondMetaProjectsResults)
summary(mnbTerpene)
hist(residuals(mnbTerpene))
ggplot(SecondMetaProjectsResults, aes(x=Decay_type, y=Terpene))+
  geom_boxplot()


# NRPS per decay type
mNRPS <- glm( NRPS ~ Decay_type, family = poisson(link="log"), data = SecondMetaProjectsResults)
summary(mNRPS)
hist(residuals(mNRPS))
mnbNRPS<- glm.nb(NRPS ~ Decay_type ,data = SecondMetaProjectsResults)
summary(mnbNRPS)
hist(residuals(mnbPKS))
ggplot(SecondMetaProjectsResults, aes(x=Decay_type, y=NRPS))+
  geom_boxplot()


# PKS per decay type
mPKS <- glm( PKS ~ Decay_type, family = poisson(link="log"), data = SecondMetaProjectsResults)
summary(mPKS)
hist(residuals(mPKS))
mnbPKS<- glm.nb(PKS ~ Decay_type ,data = SecondMetaProjectsResults)
summary(mnbPKS)
hist(residuals(mnbPKS))
emm <- emmeans(mnbPKS, ~ Decay_type)
pairs(emm) # statistical significance found between BR and WR

# Create a plot of the number of PKS clusters dependent on decay type

ggplot(SecondMetaProjectsResults, aes(x=Decay_type, y=PKS, fill=Decay_type))+
  geom_boxplot()+
  geom_signif(
    comparisons = list(c("BR", "WR")),
    annotations = "*",
    map_signif_level = TRUE, textsize = 6
  )+
  ylim(NA, 11)+
  labs(x='Decay Type', y='Number of PKS Clusters', title = 'Number of PKS Clusters dependent on Decay Type') +
  theme_light()
