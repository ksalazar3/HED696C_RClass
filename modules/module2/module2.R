# Module 2

# LOGISTICS

    # Settings
    rm(list = ls()) #removes all objects from your working environment
    
    # Load libraries
      #install.packages("tidyverse") 
      library(tidyverse)
    
    # Load dataframes used today
      #load dataset with one obs per recruiting event
      load(url("https://github.com/ksalazar3/HED696C_RClass/raw/master/data/recruiting/recruit_event_somevars.RData"))

      #load dataset with one obs per high school
      load(url("https://github.com/ksalazar3/HED696C_RClass/raw/master/data/recruiting/recruit_school_somevars.RData"))

# INVESTIGATING DF OBJECTS
      
      #type of object
      typeof(df_event)
      
      #length of object
      length(df_event)
      
      #columns and rows
      ncol(df_event)
      nrow(df_event)
      dim(df_event) #shows rows by columns
      
      #prints compact info on df
      str(df_event)
      
      #variable names
      names(df_event)
      
      #variable types
      typeof(df_event$instnm)
      typeof(df_event$med_inc)
      
# VIEW AND PRINT DATA
      
      #simply print object name
      df_event
      
      #use View()
      View(df_event) # data browser will pop-up
      
      #use head()
      head(df_event)
      
      #printing specific rows and columns
      df_event[1:5, 1:3] #print first five rows and first three columns

      #print specific elements
      df_event$zip #not very helpful
      df_event$event_state[1:10] #print elements 1-10 of event_state vector
      
      #print multiple elements using c()
      c(df_event$event_state[1:5],df_event$event_type[1:5])
      
      #check which variables have missing values
      str(df_event)
      
# FIRST STUDENT EXERCISE (write your answers here)
      
      

      
# SECOND STUDENT EXERCISE (write your answers here)
      