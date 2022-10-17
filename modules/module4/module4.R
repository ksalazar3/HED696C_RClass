# Module 4

# LOGISTICS

    # Settings
    rm(list = ls()) #removes all objects from your working environment
    
    # Load libraries
      #install.packages("tidyverse") 
      library(tidyverse)
    
    # Load dataframe used today
      
      #load student list dataset for Western Wash Univ
      load(url("https://github.com/ksalazar3/HED696C_RClass/raw/master/data/prospect_list/wwlist_merged.RData"))
      
      #load dataset with one obs per recruiting event
      load(url("https://github.com/ksalazar3/HED696C_RClass/raw/master/data/recruiting/recruit_event_somevars.RData"))
      
      #load dataset with one obs per high school
      load(url("https://github.com/ksalazar3/HED696C_RClass/raw/master/data/recruiting/recruit_school_allvars.RData"))
      
      #create new version of df_school_all with new variable names
      school_v2 <- df_school_all %>% 
        select(-contains("inst_")) %>% # remove vars that start with "inst_"
        rename(
          visits_by_berkeley = visits_by_110635,
          visits_by_boulder = visits_by_126614,
          visits_by_bama = visits_by_100751,
          visits_by_stonybrook = visits_by_196097,
          visits_by_rutgers = visits_by_186380,
          visits_by_pitt = visits_by_215293,
          visits_by_cinci = visits_by_201885,
          visits_by_nebraska = visits_by_181464,
          visits_by_georgia = visits_by_139959,
          visits_by_scarolina = visits_by_218663,
          visits_by_ncstate = visits_by_199193,
          visits_by_irvine = visits_by_110653,
          visits_by_kansas = visits_by_155317,
          visits_by_arkansas = visits_by_106397,
          visits_by_sillinois = visits_by_149222,
          visits_by_umass = visits_by_166629,
          num_took_read = num_took_rla,
          num_prof_read = num_prof_rla,
          med_inc = avgmedian_inc_2564)
      
      
      
# Student Exercises with Pipes
      
      
      #write your code here
      

# Student Exercises using mutate()
      
      
      #write your code here      
      
      
# Student Exercises using ifelse()
      
      
      #write your code here  
      

# Student Exercises using mutate()
      
      
      #write your code here
      
      
# Student Exercises using case_when()
      
      
      #write your code here