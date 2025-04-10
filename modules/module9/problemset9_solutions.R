#=======================================================================================================================================================
#PROBLEM SET #7
#NAME
#=======================================================================================================================================================

#Grade: /20

#=======================================================================================================================================================
#RUN ALL THIS CODE, YOU WILL START AT LINE XXXX
#=======================================================================================================================================================


#=======================================================================================================================================================
#LOAD LIBRARIES
#options(max.print=999999)
library(tidyverse)
library(haven)
library(labelled)
#=======================================================================================================================================================


#=======================================================================================================================================================
#LOAD RECRUITING/ZIP/HS DATA

#getwd()

rm(list = ls()) # remove all objects

events <- read_csv(file="https://github.com/ozanj/rclass/raw/master/data/recruiting/events_data_dp.csv",
                  col_types =
                    cols(
                      univ_id = col_integer(), 
                      pid = col_integer(),
                      school_id = col_character(),
                      determined_zip = col_character(),
                      categorized_event_type = col_factor(NULL),
                      categorized_location_type = col_factor(NULL),
                      event_date = col_date(format = ""),      
                      event_address = col_character(),
                      event_name = col_character(),
                      event_location_name = col_character(),
                      event_state = col_character(),
                      event_city = col_character(),
                      ipeds_id = col_integer(),      
                      latitude = col_double(),
                      longitude = col_double(),
                      sector = col_factor(NULL)
                    )
) %>% mutate(event_state = gsub('\\s+', '', event_state)) %>% #fix state whitespace formatting
  select(univ_id, pid, school_id, determined_zip, contains("categorized"), event_date, 
         contains("event"),school_id,ipeds_id,latitude,longitude,sector,-contains("datetime"))

#INVESTIGATE
names(events) # 16 variables
str(events)

events %>% count(sector) #Higher Ed institution
events %>% filter(length(school_id) <= 8) %>% count() #No private high schools
events %>% filter(length(school_id) > 8) %>% count() #All public high schools?

events %>% filter(is.na(school_id)) %>% count()
events %>% filter(is.na(ipeds_id)) %>% count()

events %>% filter(is.na(ipeds_id) & is.na(school_id)) %>% count()


#CLEAN DATA
events <- events %>%
  mutate(sector = to_labelled(sector))  # convert sector variable from factor to labelled
  
events %>% count(sector) 

events <- events %>%
  rename(zip = determined_zip) %>% # rename zip code
  select(-contains("categorized")) %>% # drop vars categorized event type and location type
  mutate( # create event type variable
    event_type = case_when(
      nchar(as.character(school_id))>8 ~ 1, # public hs
      nchar(as.character(school_id))<= 8 ~ 2, # private hs
      sector %in% c(1,4) ~ 3, # public cc
      sector %in% c(2,3,5,6,7,8,9) ~ 4, # other postsecondary
      is.na(school_id) & is.na(ipeds_id) ~ 5 # other
    )
  ) %>% # convert event_type to labelled and assign value labels
  set_value_labels(
    event_type = c(
      "public hs" = 1,
      "private hs" = 2,
      "public cc" = 3,
      "other postsecondary" = 4,
      "other" = 5
    )
  ) %>%
  set_variable_labels(
    univ_id = "ipeds id (unitid) of university making recruiting visits",
    pid = "unique id assigned to each recruiting event",
    school_id = "NCES K-12 school id",
    zip = "zip code of event",
    event_date = "event date",
    event_address = "event address",
    event_name = "name of event",   
    event_location_name = "name of event location",
    event_state = "state event took place in",
    event_city = "event city",
    ipeds_id = "ipeds id (unitid) if recruiting event occurs at a postsecondary institution",
    latitude = "latitude of event",
    longitude = "longitude of event",
    sector = "sector of postsecondary institution if event occurs at postsecondary institution",
    event_type = "category of recruiting event"
  )  

#Investigate data structure of events object
names(events)
str(events)
glimpse(events)
events %>% var_label()
events %>% val_labels()

#Investigate particular variables
options(tibble.print_min=60)

events %>% count(event_state)

events %>% count(sector)
events %>% count(sector) %>% as_factor()

str(events$event_type)
events %>% count(event_type)
events %>% count(event_type) %>% as_factor()


#Assert that there is one observation per event id
events %>% # start with data frame object
  group_by(pid) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group


#keep only visits to public high schools
events %>% count(event_type) %>% as_factor()
events <- events %>% filter(event_type == 1) %>% select(-sector,-ipeds_id)

###keep only one obs per univ_id school_id

#count the number of obs per high school
events %>% # start with data frame object
  group_by(univ_id,school_id) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group


events %>%
  group_by(univ_id, school_id) %>%
  summarise(n_per_group = n()) %>%
  ungroup %>%
  count(n_per_group) %>%
  filter(n_per_group > 1)


#keep only one obs per univ_id school_id  

events_per_pubschool <- events %>% group_by(univ_id, event_type, school_id) %>%
  summarise(
    num_events = n(),
    zip = first(zip),
    event_state = first(event_state),
    event_city = first(event_city),
    event_name = first(event_name),
    latitude = first(latitude),
    longtitude = first(longitude)
    
  )

events_per_pubschool %>%
  count(num_events)

names(events_per_pubschool)
names(events)
#=======================================================================================================================================================

  
#=======================================================================================================================================================
#LOAD DATA ON CHARACTERISTICS OF PUBLIC UNIVERSITIES DOING THE RECRUITING (IPEDS) 
getwd()

ipeds <- read.csv(file="https://github.com/ozanj/rclass/raw/master/data/ipeds/ic/meta_university_dp.csv", 
                       na.strings=c("","NA"), colClasses=c("univ_name"="character"), encoding="UTF-8") %>%
  select(univ_id, univ_name) %>%
  set_variable_labels(
    univ_id = "ipeds id (unitid) of university making recruiting visits",
    univ_name = "institution name of university doing the recruiting")

names(ipeds)
str(ipeds)
ipeds %>% var_label()
ipeds %>% val_labels() # none  

#assert one obs per unitid
ipeds %>% # start with data frame object
  group_by(univ_id) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group


#left merge between events_per_pubschool and ipeds
#outer merge (left) merge 
events_per_pubschool <- events_per_pubschool %>% 
  left_join(ipeds, by = "univ_id")

#number of obs that don't merge between events_per_pubschool and ipeds
events_per_pubschool %>% 
  anti_join(ipeds, by = "univ_id") %>% count() # all obs merge

names(events_per_pubschool)
names(ipeds)
events_per_pubschool %>% count(univ_name)
#=======================================================================================================================================================
 
  
#=======================================================================================================================================================
#LOAD ACS (ZIP LEVEL) DATA 

zip_data <- read.csv('https://github.com/ozanj/rclass/raw/master/data/acs/zip_to_state.csv', na.strings=c('','NA'),colClasses=c("zip_code"="character"))


zip_data %>% val_labels()

#Check if race/ethnicity variables add up to race total "pop_total"
zip_data %>%
  select(pop_total, pop_white, pop_black, pop_amerindian, pop_asian, pop_nativehawaii, pop_otherrace, pop_tworaces, pop_hispanic) %>%
  mutate(pop_totalv2 = pop_white + pop_black + pop_amerindian + pop_asian + pop_nativehawaii + pop_otherrace + pop_tworaces + pop_hispanic) %>%
  filter(pop_totalv2 == pop_total) %>%
  count()


#CHANGE VARIABLE LABELS
#LABEL VARIABLES [THIS CODE IS BASE R APPROACH]

# B03002: Hispanic or Latino Origin by Race
var_label(zip_data[['pop_total']]) <- 'Race total'
var_label(zip_data[['pop_white']]) <- 'White [Not Hispanic or Latino] '
var_label(zip_data[['pop_black']]) <- 'Black or African American'
var_label(zip_data[['pop_amerindian']]) <- 'American Indian and Alaska Native'
var_label(zip_data[['pop_asian']]) <- 'Asian'
var_label(zip_data[['pop_nativehawaii']]) <- 'Native Hawaiian and Other Pacific Islander'
var_label(zip_data[['pop_otherrace']]) <- 'Some Other Race'
var_label(zip_data[['pop_tworaces']]) <- 'Two or More Races'
var_label(zip_data[['pop_hispanic']]) <- 'Hispanic or Latino'

# B15003: Educational Attainment for the Population 25 Years and Over
var_label(zip_data[['pop_total_25plus']]) <- 'Educational Attainment for the Population 25 Years and Over [Total]'
var_label(zip_data[['pop_edu_hs']]) <- 'Educational Attainment for the Population 25 Years and Over [Regular High School Diploma]'
var_label(zip_data[['pop_edu_GED']]) <- 'Educational Attainment for the Population 25 Years and Over [GED or Alternative Credential]'
var_label(zip_data[['pop_edu_somecollege_under1yr']]) <- 'Educational Attainment for the Population 25 Years and Over [Some College, Less than 1 Year]'
var_label(zip_data[['pop_edu_somecollege_1plusyrs']]) <- 'Educational Attainment for the Population 25 Years and Over [Some College, 1 or More Years, No Degree]'
var_label(zip_data[['pop_edu_attain_assoc']]) <- 'Educational Attainment for the Population 25 Years and Over [Associate\'s Degree]'
var_label(zip_data[['pop_edu_attain_bach']]) <- 'Educational Attainment for the Population 25 Years and Over [Bachelor\'s Degree]'
var_label(zip_data[['pop_edu_attain_master']]) <- 'Educational Attainment for the Population 25 Years and Over [Master\'s Degree]'
var_label(zip_data[['pop_edu_attain_prof']]) <- 'Educational Attainment for the Population 25 Years and Over [Professional School Degree]'
var_label(zip_data[['pop_edu_attain_doct']]) <- 'Educational Attainment for the Population 25 Years and Over [Doctorate Degree]'

# B19049: Median Household Income in the Past 12 Months (In 2016 Inflation-Adjusted Dollars) by Age of Householder
var_label(zip_data[['median_household_income']]) <- 'Median Household Income in the Past 12 Months (In 2016 Inflation-Adjusted Dollars) by Age of Householder [Total]'
var_label(zip_data[['median_inc_2544']]) <- 'Median Household Income in the Past 12 Months (In 2016 Inflation-Adjusted Dollars) by Age of Householder [Householder 25 to 44 Years]'
var_label(zip_data[['median_inc_4564']]) <- 'Median Household Income in the Past 12 Months (In 2016 Inflation-Adjusted Dollars) by Age of Householder [Householder 45 to 64 Years]'
var_label(zip_data[['avgmedian_inc_2564']]) <- 'Median Household Income in the Past 12 Months (In 2016 Inflation-Adjusted Dollars) by Age of Householder [Householder 25 to 64 Years]'

# Other
var_label(zip_data[['zip_code']]) <- 'Zip Code'
var_label(zip_data[['zip_name']]) <- 'Zip Name'
var_label(zip_data[['state_code']]) <- 'State Code'
var_label(zip_data[['state_fips']]) <- 'State Fips Code'

#DROP VARIABLES YOU DON'T WANT
names(zip_data)
zip_data <- zip_data %>% select(-starts_with("house"),-zip_code.2.,-starts_with("t_households"))
names(zip_data)


#INVESTIGATE OBJECT

names(zip_data)
zip_data %>% var_label()
zip %>% val_labels()

###create racial composition of zipcode 
racevars <- function(df,new_col,pop_subgroup,pop_total){
  print(summary(df[[pop_subgroup]]))
  print(summary(df[[pop_total]]))
  df[[new_col]] <- (df[[pop_subgroup]] / df[[pop_total]])*100
  df[[new_col]][is.na(df[[new_col]])] <- 0
  print(summary(df[[new_col]]))
  return(df)
}


zip_data<-racevars(zip_data,"pct_popam","pop_amerindian","pop_total")
zip_data<-racevars(zip_data,"pct_popas","pop_asian","pop_total")
zip_data<-racevars(zip_data,"pct_pophi","pop_hispanic","pop_total")
zip_data<-racevars(zip_data,"pct_popbl","pop_black","pop_total")
zip_data<-racevars(zip_data,"pct_popwh","pop_white","pop_total")
zip_data<-racevars(zip_data,"pct_pophp","pop_nativehawaii","pop_total")
zip_data<-racevars(zip_data,"pct_poptr","pop_tworaces","pop_total")
zip_data<-racevars(zip_data,"pct_popothr","pop_otherrace","pop_total")


#create var for POC [everyone except White]
zip_data$pocrace<-rowSums(zip_data[,c("pct_poptr", "pct_pophp", "pct_popbl", "pct_pophi", "pct_popas", "pct_popam")], na.rm = TRUE) #sumrows equals zero if all columns are NA
#zip[is.na(zip$mbl_nummthprof) & is.na(zip$mhi_nummthprof) & is.na(zip$mas_nummthprof) & is.na(zip$mam_nummthprof), "soc_nummthprof"] <- NA #code to missing
summary(zip_data$pocrace) 

names(zip_data)
#=======================================================================================================================================================


#=======================================================================================================================================================
#LOAD COMMON CORE DATA
#rm(list = ls()) # remove all objects
#getwd()

load(url("https://github.com/ozanj/rclass/raw/master/data/nces_hs/nces_hs_data.RData"))

#Investigate ccd
names(ccd)
names(ccd) <- tolower(names(ccd)) #lower case var names
names(ccd)
glimpse(ccd)
str(ccd)

str(ccd$titlei_status)
attributes(ccd$titlei_status)

ccd[1:50] %>% var_label() #too many vars need to view a fewa at a time
ccd[51:100] %>% var_label()
ccd[101:150] %>% var_label()
ccd[151:200] %>% var_label()
ccd[201:250] %>% var_label()
ccd[251:300] %>% var_label()
ccd[301:357] %>% var_label()


#Subsetting data
ccd <- ccd %>%
  select(survyear, fipst, schid, sch_type, g12offered, g12, virtual, updated_status, ncessch,
         sch_name, titlei_status, lstreet1, lcity, lstate, lzip, level, totfrl, frelch, redlch,
         am, as, hi, bl, wh, hp, tr)


#Rename race/ethnicity variables
ccd <- ccd %>%
  rename( native_am_stu = am,
          asian_stu = as,
          latinx_stu = hi,
          black_stu = bl,
          white_stu = wh,
          native_hi_pi_stu = hp,
          two_or_more_stu = tr)


#Remove objects folks don't need to complete problem set
rm(list = c('pss', 'events', 'ipeds'))
#=======================================================================================================================================================



#=======================================================================================================================================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> YOUR CODE STARTS HERE. FOLLOW THE INSTRUCTIONS FROM PDF >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#=======================================================================================================================================================

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Preliminary investigation of three data sets (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Filter for obs that meet public hs criteria listed in the instructions
#Investigate variables for criteria for public high schools
ccd %>%
  select(g12offered) %>%
  var_label() 

ccd %>%
  count(g12offered) %>%
  as_factor() #"yes"


ccd %>%
  select(g12) %>%
  var_label() #at least 10


ccd %>%
  count(g12) %>%
  as_factor() #at least 10

ccd %>%
  select(virtual) %>%
  var_label() 

ccd %>%
  count(virtual)%>%
  as_factor() #no"

ccd %>%
  count(fipst) %>%
  as_factor() #<=52


ccd %>%
  count(sch_type) %>%
  as_factor() #1,3 


ccd %>%
  select(updated_status) %>%
  var_label() #1, 3, 8 

ccd %>%
  count(updated_status) %>%
  as_factor() #1, 3, 8 

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Create an object based on ccd and following criteria (/4)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Filter for hs criteria
ccd_hs <- ccd %>%
  filter(g12offered == "Yes", g12 > 10, virtual == "No", fipst <= 56, sch_type %in% c(1,3), updated_status %in% c(1,3,8))  

#Run some quick  checks
ccd_hs %>%
  count(sch_type) %>%
  as_factor()

ccd_hs %>%
  filter(fipst > 56) 

ccd_hs %>%
  count(fipst) %>% as_factor()

val_labels(ccd_hs$fipst)


ccd_hs %>%
  count(virtual) %>%
  as_factor()

ccd_hs %>%
  count(updated_status) %>%
  as_factor()

colSums(is.na(ccd_hs)) #get the sum of missing values for every column 


ccd_hs %>% # start with data frame object
  group_by(ncessch) %>% # group by ncessch id 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group)


ccd_hs %>%
  count(ncessch)

ccd_hs %>%
  count(schid)


#names(ccd_hs)

#Census level data
zip_data %>% # start with data frame object
  group_by(zip_code) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group

ccd_hs %>%
  count(lzip)

zip_data %>%
  count(zip_code)

#Check lzip and zip_code 
#names(zip_data)
ccd_hs %>%
  filter(lzip == "01247") %>%
  select(sch_name, lstreet1, lcity, lstate, lzip)

zip_data %>%
  filter(zip_code == "01247") %>%
  select(state_code)


ccd_hs %>%
  filter(lzip == "01040") %>%
  select(sch_name, lstreet1, lcity, lstate, lzip)


zip_data %>%
  filter(zip_code == "01040") %>%
  select(state_code)


ccd_hs %>%
  filter(lzip == "01453") %>%
  select(sch_name, lstreet1, lcity, lstate, lzip)


zip_data %>%
  filter(zip_code == "01453") %>%
  select(state_code)


names(ccd_hs)
#Drop some variables 
ccd_hs <- ccd_hs %>%
  select(survyear, fipst, sch_type, ncessch, sch_name, titlei_status, lstreet1, lcity, lstate, lzip, totfrl, frelch, redlch,
         native_am_stu, asian_stu, latinx_stu, black_stu, white_stu, native_hi_pi_stu, two_or_more_stu)


#Check variable labels
ccd_hs %>%
  var_label()


ccd_hs %>%
  select(sch_type, titlei_status) %>%
  val_labels()



#Rename zip_code variable for merge
names(ccd_hs)
ccd_hs <- ccd_hs %>% rename(zip_code = lzip)
names(ccd_hs)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Using ccd_hs as the x table zip_data as your y table, perform a left_join() (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Merge between nces public high school data (ccd_hs) and census level data (zip_data)
#outer merge (left) merge 
ccd_hs_zip <- ccd_hs %>% 
  left_join(zip_data, by = "zip_code")  

#number of obs that don't merge between ccd_hs and zip_data
anti_ccd_hs   <- ccd_hs %>% 
  anti_join(zip_data, by = "zip_code") 

#Do some investigations

anti_ccd_hs %>%
  select(ncessch, sch_name, lstreet1, lstate, zip_code)

names(ccd_hs_zip)  



colSums(is.na(ccd_hs_zip)) #89  missing for ccd dataset


ccd_hs_zip%>%
  filter(is.na(pop_total)) %>%
  select(survyear, sch_type, sch_name, titlei_status, lstreet1, lcity, lstate) #schools not visited


#Drop some variables 
#names(ccd_hs_zip)
ccd_hs_zip <- ccd_hs_zip %>%
  select(-state_code, -state_fips, -zip_name)
#names(ccd_hs_zip)

#=======================================================================================================================================================
#Investigate the object “events_per_pubschool”

names(events_per_pubschool)
str(events_per_pubschool)
#count the number of obs per high school
events_per_pubschool %>% # start with data frame object
  group_by(univ_id,school_id) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Keep only observations for one university (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Filter to one university [Could be any]

#events_per_pubschool
#names(events_per_pubschool)


#Selecting University of South Carolina-Columbia (218663)
events_carolina <-  events_per_pubschool %>%
  filter(univ_id == 218663)  


#Investigate object you created of only one university  
names(events_carolina)  

events_carolina %>% 
  select(univ_id, univ_name, school_id, event_name, event_state)

colSums(is.na(events_carolina)) #get the sum of missing values for every column 

events_carolina %>%
  filter(univ_id != 218663) #only one university 


#=======================================================================================================================================================

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Using ccd_hs_zip as your x table and events_nameofinstitution as your y table, perform a left_join() (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#Merge between nces zip data object and events data

#Investigate data structure of zip object
ccd_hs_zip %>% filter(is.na(zip_code)) %>% count(zip_code) # count number of obs with missing zip code

#Assert that there is one observation per high school
#names(ccd_hs_zip)

ccd_hs_zip %>%
  select(pop_total, 4:8, zip_code)

ccd_hs_zip %>%
  filter(is.na(pop_total))


ccd_hs_zip %>% # start with data frame object
  group_by(ncessch) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group


#Check events carolina to make sure uniquely identified by school_id
events_carolina %>% # start with data frame object
  group_by(school_id) %>% # group by 
  summarise(n_per_group=n()) %>% # create measure of number of obs per group
  ungroup %>% # ungroup (otherwise frequency table [next step] created) separately for each group (i.e., separate frequency table for each value of unitid)
  count(n_per_group) # frequency of number of observations per group

#rename school_id to ncessch
events_carolina <- events_carolina %>% rename(ncessch = school_id)

#outer merge (left) merge nces zip object and events object
str(events_carolina$ncessch)  
str(ccd_hs_zip$ncessch)  
ccd_hs_zip_events <- ccd_hs_zip %>% 
  left_join(events_carolina, by = "ncessch")


#investigate obs that don't merge
#create object of obs that didn't merge
anti_ccd_hs_zip_events<- ccd_hs_zip %>% anti_join(events_carolina, by = "ncessch") 


names(anti_ccd_hs_zip_events)
options(tibble.print_min=90) 

anti_ccd_hs_zip_events %>%
  count(lstate, ncessch) %>% as_factor()


#names(anti_ccd_hs_zip_events)

anti_ccd_hs_zip_events %>%
  select(sch_name, lstate, ncessch)

anti_ccd_hs_zip_events %>% count(lstate, lcity, ncessch)

anti_ccd_hs_zip_events %>% group_by(ncessch) %>%
  summarise(by_school_id = n()) %>%
  ungroup() %>%
  count(by_school_id)



colSums(is.na(ccd_hs_zip_events)) 

ccd_hs_zip_events %>%
  filter(!is.na(event_name)) %>%
  select(ncessch, sch_name, event_name, univ_name)


#Could drop zip event_state event_city
ccd_hs_zip_events %>%
  select(zip_code, zip, lstate, event_state, lcity, event_city)

ccd_hs_zip_events %>%
  filter(!is.na(event_name)) %>%
  select(zip_code, zip, lstate, event_state, lcity, event_city)

ccd_hs_zip_events <- ccd_hs_zip_events %>%
  select(-zip, -event_state, -event_city)


ccd_hs_zip_events %>%
  filter(!is.na(event_name)) %>%
  select(zip_code, lstate, lcity)
  
#Reorganize columns
#=======================================================================================================================================================

#Check obs that didn't merge for num_events
ccd_hs_zip_events %>%
  count(num_events)


ccd_hs_zip_events %>%
  filter(is.na(num_events))

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Create a variable called num_visits (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------


#Recode so that NA is 0 for num_events since those schools were not visited  
ccd_hs_zip_events <- ccd_hs_zip_events %>%
  mutate(num_visits = ifelse(is.na(num_events), 0,num_events)) 

#Check
ccd_hs_zip_events %>%
  group_by(num_events) %>%
  count(num_visits)

#Could drop num_events
ccd_hs_zip_events <- ccd_hs_zip_events %>%
  select(-num_events) 

names(ccd_hs_zip_events)   

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Create a 0/1 variable got_visit (/2)

#-------------------------------------------------------------------------------------------------------------------------------------------------------


#Create 0/1 indicator variable if school got a visit
ccd_hs_zip_events <- ccd_hs_zip_events %>%
  mutate(got_visit = ifelse(num_visits >= 1,1,0))

ccd_hs_zip_events %>%
  group_by(num_visits) %>%
  count(got_visit)

ccd_hs_zip_events %>%
  count(got_visit)
#=======================================================================================================================================================
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Perform exploratory data analysis (/4)

#-------------------------------------------------------------------------------------------------------------------------------------------------------


#Exploratory Analysis

