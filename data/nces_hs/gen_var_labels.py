import re

ccd = """
VALUE $fipsf
    '01'='Alabama'           '02'='Alaska'          '04'='Arizona'         '05'='Arkansas'
    '06'='California'        '08'='Colorado'        '09'='Connecticut'     '10'='Delaware'
    '11'='District of Columbia'                     '12'='Florida'         '13'='Georgia'
    '15'='Hawaii'            '16'='Idaho'           '17'='Illinois'        '18'='Indiana'
    '19'='Iowa'              '20'='Kansas'          '21'='Kentucky'        '22'='Louisiana'
    '23'='Maine'             '24'='Maryland'        '25'='Massachusetts'   '26'='Michigan'
    '27'='Minnesota'         '28'='Mississippi'     '29'='Missouri'        '30'='Montana'
    '31'='Nebraska'          '32'='Nevada'          '33'='New Hampshire'   '34'='New Jersey'
    '35'='New Mexico'        '36'='New York'        '37'='North Carolina'  '38'='North Dakota'
    '39'='Ohio'              '40'='Oklahoma'        '41'='Oregon'          '42'='Pennsylvania'
    '43'='Puerto Rico'       '44'='Rhode Island'    '45'='South Carolina'  '46'='South Dakota'
    '47'='Tennessee'         '48'='Texas'           '49'='Utah'            '50'='Vermont'
    '51'='Virginia'          '53'='Washington'      '54'='West Virginia'   '55'='Wisconsin'
    '56'='Wyoming'           '59'='Bureau of Indian Education'             '60'='American Samoa'
    '63'='Department of Defense Education Activity' '66'='Guam'            '69'='Northern Marianas'
    '72'='Puerto Rico'       '78'='U.S. Virgin Islands' 
    'M'='Missing'            'N'='Not Applicable';

VALUE $stabrf
    'AL'='Alabama'        'AK'='Alaska'          'AZ'='Arizona'        'AR'='Arkansas'    'CA'='California'
    'CO'='Colorado'       'CT'='Connecticut'     'DE'='Delaware'       'DC'='District of Columbia'
    'FL'='Florida'        'GA'='Georgia'         'HI'='Hawaii'         'ID'='Idaho'       'IL'='Illinois'
    'IN'='Indiana'        'IA'='Iowa'            'KS'='Kansas'         'KY'='Kentucky'    'LA'='Louisiana'
    'ME'='Maine'          'MD'='Maryland'        'MA'='Massachusetts'  'MI'='Michigan'    'MN'='Minnesota'
    'MS'='Mississippi'    'MO'='Missouri'        'MT'='Montana'        'NE'='Nebraska'    'NV'='Nevada'
    'NH'='New Hampshire'  'NJ'='New Jersey'      'NM'='New Mexico'     'NY'='New York'    'NC'='North Carolina'
    'ND'='North Dakota'   'OH'='Ohio'            'OK'='Oklahoma'       'OR'='Oregon'      'PA'='Pennsylvania'
    'RI'='Rhode Island'   'SC'='South Carolina'  'SD'='South Dakota'   'TN'='Tennessee'   'TX'='Texas'
    'UT'='Utah'           'VT'='Vermont'         'VA'='Virginia'       'WA'='Washington'  'WV'='West Virginia'
    'WI'='Wisconsin'      'WY'='Wyoming'
    'DD'='Department of Defense Education Activity'
    'BI'='Bureau of Indian Education'
    'AS'='American Samoa'
    'GU'='Guam'
    'MP'='Northern Marianas'
    'PR'='Puerto Rico'
    'VI'='U.S. Virgin Islands'
    'AS'='American Samoa'
    'MP'='Northern Marianas'
    'M'='Missing'
    'N'='Not Applicable';

VALUE $stypef
    '1'='Regular School'
    '2'='Special Education School'
    '3'='Vocational Education School'
    '4'='Alternative Education School'
    '5'='Reportable program'
    'M'='Missing'
    'N'='Not applicable';

VALUE $Gslof
    '01'='1st grade students'
    '02'='2nd grade students'
    '03'='3rd grade students'
    '04'='4th grade students'
    '05'='5th grade students'
    '06'='6th grade students'
    '07'='7th grade students'
    '08'='8th grade students'
    '09'='9th grade students'
    '10'='10th grade students'
    '11'='11th grade students'
    '12'='12th grade students'
    '13'='13th grade students'
    'AE'='Total adult education students'
    'KG'='Kindergarten students'
    'PK'='Prekindergarten students'
    'UG'='Students in ungraded classes'
    'M'='Missing'
    'N'='Not applicable';

VALUE $Gshif
    '01'='1st grade students'
    '02'='2nd grade students'
    '03'='3rd grade students'
    '04'='4th grade students'
    '05'='5th grade students'
    '06'='6th grade students'
    '07'='7th grade students'
    '08'='8th grade students'
    '09'='9th grade students'
    '10'='10th grade students'
    '11'='11th grade students'
    '12'='12th grade students'
    '13'='13th grade students'
    'AE'='Total adult education students'
    'KG'='Kindergarten students'
    'PK'='Prekindergarten students'
    'UG'='Students in ungraded classes'
    'M'='Missing'
    'N'='Not applicable';

VALUE $levelf
    '1'='Primary (low grade=PK through 03; high grade=PK through 08)'
    '2'='Middle (low grade=04 through 07; high grade=04 through 09)'
    '3'='High (low grade=07 through 12; high grade=12 only)'
    '4'='Other (any other configuration not falling within the above three categories, including ungraded)'
    'N'='Not applicable';

VALUE $Systaf  
    '1'='Open'
    '2'='Closed'
    '3'='New'
    '4'='Added'
    '5'='Changed Agency'
    '6'='Inactive'
    '7'='Future School'
    '8'='Reopened';

VALUE $Upstaf  
    '1'='Open'
    '2'='Closed'
    '3'='New'
    '4'='Added'
    '5'='Changed Agency'
    '6'='Inactive'
    '7'='Future School'
    '8'='Reopened';

VALUE $igoffrf
    'A'='Adjustment'
    'R'='As reported by the state';

VALUE $TitleIstaf
    '1'='Title I targeted assistance eligible school-No program'
    '2'='Title I targeted assistance school'
    '3'='Title I schoolwide eligible-Title I targeted assistance program'
    '4'='Title I schoolwide eligible school-No program'
    '5'='Title I schoolwide school'
    '6'='Not a Title I school'
    '-9'='Suppressed'
    'M'='Missing';

VALUE $TitleIf
    'Yes'='Yes'
    'No'='No'
    'Missing'='Missing'
    'Not Applicable'='Not Applicable'
    '-9'='Suppressed';

VALUE $StitlIf
    'Yes'='Yes'
    'No'='No'
    'Missing'='Missing'
    'Not Applicable'='Not Applicable'
    '-9'='Suppressed';

VALUE $NSLPSTATUSf
    'CEO'='Yes, under Community Eligibility Option (CEO)'
    'NO'='No'
    'NP'='Yes, participating without using any Provision or the CEO'
    'P1'='Yes, under Provision 1'
    'P2'='Yes, under Provision 2'
    'P3'='Yes, under Provision 3'
    'M'='MISSING';
"""

ccd_conversion = {
    '$fipsf': 'FIPST',
    '$stabrf': 'STABR',
    '$stypef': 'SCH_TYPE',
    '$Gslof': 'GSLO',
    '$Gshif': 'GSHI',
    '$levelf': 'LEVEL',
    '$Systaf': 'SY_STATUS',
    '$Upstaf': 'UPDATED_STATUS',
    '$igoffrf': 'IGOFFERED',
    '$TitleIstaf': 'TITLEI_STATUS',
    '$TitleIf': 'TITLEI',
    '$StitlIf': 'STITLEI',
    '$NSLPSTATUSf': 'NSLPSTATUS_CODE'
}

pss = """
value CSOURCE
  1='Mail'
  2='Internet'
  3='Regional Office follow-up'
  4='CATI (computer-assisted telephone interview)' ;
value P135F
  1='Yes'
  2='No' ;
value P145F
  1='Yes'
  2='No' ;
value P155F
  1='Yes'
  2='No' ;
value P165F
  1='Yes'
  2='No' ;
value P175F
  1='Yes'
  2='No' ;
value P185F
  1='Yes'
  2='No' ;
value P195F
  1='Yes'
  2='No' ;
value P205F
  1='Yes'
  2='No' ;
value P215F
  1='Yes'
  2='No' ;
value P225F
  1='Yes'
  2='No' ;
value P235F
  1='Yes'
  2='No' ;
value P245F
  1='Yes'
  2='No' ;
value P255F
  1='Yes'
  2='No' ;
value P265F
  1='Yes'
  2='No' ;
value P275F
  1='Yes'
  2='No' ;
value P285F
  1='Yes'
  2='No' ;
value P295F
  1='Yes'
  2='No' ;
value P335F
  1='Yes'
  2='No, it is an all-female school'
  3='No, it is an all-male school' ;
value P345F
  1='Yes'
  2='No' ;
value P365F
  0='School/program does not offer kindergarten, transitional kindergarten, or transitional first grade'
  1='Full day'
  2='Half day'
  3='Both offered' ;
value P415F
  1='Regular elementary or secondary'
  2='Montessori'
  3='Special program emphasis'
  4='Special education'
  5='Career/technical/vocational'
  6='Alternative/other'
  7='Early childhood program or day care center' ;
value P420F
  1='Yes'
  2='No' ;
value P425F
  1='Yes'
  2='No' ;
value P430F
  1='Yes'
  2='No' ;
value P435F
  1='Yes'
  2='No' ;
value P440F
  1='Roman Catholic'
  2='African Methodist Episcopal'
  3='Amish'
  4='Assembly of God'
  5='Baptist06'
  7='Calvinist'
  8='Christian (no specific denomination)'
  9='Church of Christ'
  10='Church of God'
  11='Church of God in Christ'
  12='Church of the Nazarene'
  13='Disciples of Christ'
  14='Episcopal'
  15='Friends'
  16='Greek Orthodox'
  17='Islamic'
  18='Jewish'
  19='Latter Day Saints'
  20='Lutheran Church - Missouri Synod'
  21='Evangelical Lutheran Church in America'
  22='Wisconsin Evangelical Lutheran Synod'
  23='Other Lutheran'
  24='Mennonite'
  25='Methodist'
  26='Pentecostal'
  27='Presbyterian'
  28='Seventh-Day Adventist'
  29='Other' ;
value P445F
  1='Parochial'
  2='Diocesan'
  3='Private' ;
value P450F
  1='This school/program does NOT belong to ANY associations or organizations.' ;
value P455F
  0='Does not belong to the Accelerated Christian Education (or School of Tomorrow)'
  1='Accelerated Christian Education (or School of Tomorrow)' ;
value P460F
  0='Does not belong to the American Association of Christian Schools'
  1='American Association of Christian Schools' ;
value P465F
  0='Does not belong to the Association of Christian Schools International'
  1='Association of Christian Schools International' ;
value P467F
  0='Does not belong to the Association of Christian Teachers and Schools'
  1='Association of Christian Teachers and Schools' ;
value P468F
  0='Does not belong to the Association of Classical and Christian Schools'
  1='Association of Classical and Christian Schools' ;
value P470F
  0='Does not belong to the Christian Schools International'
  1='Christian Schools International' ;
value P480F
  0='Does not belong to the Evangelical Lutheran Education Association'
  1='Evangelical Lutheran Education Association' ;
value P485F
  0='Does not belong to the Friends Council on Education'
  1='Friends Council on Education' ;
value P490F
  0='Does not belong to the General Conference of the Seventh-Day Adventist Church'
  1='General Conference of the Seventh-Day Adventist Church' ;
value P492F
  0='Does not belong to the Islamic School League of America'
  1='Islamic School League of America' ;
value P495F
  0='Does not belong to the Jesuit Secondary Education Association'
  1='Jesuit Secondary Education Association' ;
value P500F
  0='Does not belong to the National Association of Episcopal Schools'
  1='National Association of Episcopal Schools' ;
value P505F
  0='Does not belong to the National Catholic Educational Association'
  1='National Catholic Educational Association' ;
value P510F
  0='Does not belong to the National Christian School Association'
  1='National Christian School Association' ;
value P515F
  0='Does not belong to the National Society of Hebrew Day Schools'
  1='National Society of Hebrew Day Schools' ;
value P520F
  0='Does not belong to the Oral Roberts University Educational Fellowship'
  1='Oral Roberts University Educational Fellowship' ;
value P522F
  0='Does not belong to the Jewish Community Day School Association'
  1='The Jewish Community Day School Association' ;
value P525F
  0='Does not belong to the Solomon Schechter Day School Association'
  1='Solomon Schechter Day School Association' ;
value P530F
  0='Does not belong to the Southern Baptist Association of Christian Schools'
  1='Southern Baptist Association of Christian Schools' ;
value P535F
  0='Does not belong to other religious school associations'
  1='Other religious school associations' ;
value P540F
  0='Does not belong to the American Montessori Society'
  1='American Montessori Society' ;
value P542F
  0='Does not belong to the Association Montessori International'
  1='Association Montessori International' ;
value P545F
  0='Does not belong to other Montessori associations'
  1='Other Montessori associations' ;
value P550F
  0='Does not belong to the Association of Military Colleges and Schools'
  1='Association of Military Colleges and Schools' ;
value P555F
  0='Does not belong to the Association of Waldorf Schools of North America'
  1='Association of Waldorf Schools of North America' ;
value P575F
  0='Does not belong to the Private Special Education Centers'
  1='National Association of Private Special Education Centers' ;
value P580F
  0='Does not belong to other associations for exceptional children'
  1='Other associations for exceptional children' ;
value P585F
  0='Does not belong to the European Council for International Schools'
  1='European Council for International Schools' ;
value P590F
  0='Does not belong to the National Association for the Education of Young Children'
  1='National Association for the Education of Young Children' ;
value P600F
  0='Does not belong to the National Association of Laboratory Schools'
  1='National Association of Laboratory Schools' ;
value P602F
  0='Does not belong to the National Coalition of Girls'' Schools'
  1='National Coalition of Girls'' Schools' ;
value P605F
  0='Does not belong to other special emphasis associations'
  1='Other special emphasis associations' ;
value P610F
  0='Does not belong to the Alternative School Network'
  1='Alternative School Network' ;
value P620F
  0='Does not belong to the National Association of Independent Schools'
  1='National Association of Independent Schools' ;
value P622F
  0='Does not belong to state or regional independent school association'
  1='State or regional independent school association' ;
value P630F
  0='Does not belong to the National Independent Private School Association'
  1='National Independent Private School Association' ;
value P635F
  0='Does not belong to The Association of Boarding Schools'
  1='The Association of Boarding Schools' ;
value P640F
  0='Does not belong to other school associations'
  1='All other school associations' ;
value P660F
  1='Yes'
  2='No' ;
value P661F
  1='Yes'
  2='No' ;
value P663F
  1='Yes'
  2='No' ;
value P664F
  0='No K-12 students'
  1='All K-12 students';
value REGION
  1='Northeast (CT, ME, MA, NH, NJ, NY, PA, RI, VT)'
  2='Midwest (IL, IN, IA, KS, MI, MN, MO, NE, ND, OH, SD, WI)'
  3='South (AL, AR, DE, DC, FL, GA, KY, LA, MD, MS, NC, OK, SC, TN, TX, VA, WV)'
  4='West (AK, AZ, CA, CO, HI, ID, MT, NV, NM, OR, UT, WA, WY)' ;
value PSTANSI
  1='ALABAMA'
  2='ALASKA'
  4='ARIZONA'
  5='ARKANSAS'
  6='CALIFORNIA'
  8='COLORADO'
  9='CONNECTICUT'
  10='DELAWARE'
  11='DISTRICT OF COLUMBIA'
  12='FLORIDA'
  13='GEORGIA'
  15='HAWAII'
  16='IDAHO'
  17='ILLINOIS'
  18='INDIANA'
  19='IOWA'
  20='KANSAS'
  21='KENTUCKY'
  22='LOUISIANA'
  23='MAINE'
  24='MARYLAND'
  25='MASSACHUSETTS'
  26='MICHIGAN'
  27='MINNESOTA'
  28='MISSISSIPPI'
  29='MISSOURI'
  30='MONTANA'
  31='NEBRASKA'
  32='NEVADA'
  33='NEW HAMPSHIRE'
  34='NEW JERSEY'
  35='NEW MEXICO'
  36='NEW YORK'
  37='NORTH CAROLINA'
  38='NORTH DAKOTA'
  39='OHIO'
  40='OKLAHOMA'
  41='OREGON'
  42='PENNSYLVANIA'
  44='RHODE ISLAND'
  45='SOUTH CAROLINA'
  46='SOUTH DAKOTA'
  47='TENNESSEE'
  48='TEXAS'
  49='UTAH'
  50='VERMONT'
  51='VIRGINIA'
  53='WASHINGTON'
  54='WEST VIRGINIA'
  55='WISCONSIN'
  56='WYOMING' ;
value ULOCALE1F
  11='City, Large: Territory inside an urbanized area and inside a principal city with population of 250,000 or more.'
  12='City, Midsize: Territory inside an urbanized area and inside a principal city with population less than 250,000 and grea'
  13='City, Small: Territory inside an urbanized area and inside a principal city with population less than 100,000.'
  21='Suburb, Large: Territory outside a principal city and inside an urbanized area with population of 250,000 or more.'
  22='Suburb, Midsize: Territory outside a principal city and inside an urbanized area with population less than 250,000 and g'
  23='Suburb, Small: Territory outside a principal city and inside an urbanized area with population less than 100,000.'
  31='Town, Fringe: Territory inside an urban cluster that is less than or equal to 10 miles from an urbanized area.'
  32='Town, Distant: Territory inside an urban cluster that is more than 10 miles and less than or equal to 35 miles from an u'
  33='Town, Remote: Territory inside an urban cluster that is more than 35 miles of an urbanized area.'
  41='Rural, Fringe: Census-defined rural territory that is less than or equal to 5 miles from an urbanized area, as well as r'
  42='Rural, Distant: Census-defined rural territory that is more than 5 miles but less than or equal to 25 miles from an urba'
  43='Rural, Remote: Census-defined rural territory that is more than 25 miles from an urbanized area and is also more than 10' ;
value LOGR2016F
  1='All Ungraded'
  2='Lowest grade in school is prekindergarten'
  3='Lowest grade in school is kindergarten'
  4='Lowest grade in school is transitional kindergarten'
  5='Lowest grade in school is transitional first grade'
  6='Lowest grade in school is 1st grade'
  7='Lowest grade in school is 2nd grade'
  8='Lowest grade in school is 3rd grade'
  9='Lowest grade in school is 4th grade'
  10='Lowest grade in school is 5th grade'
  11='Lowest grade in school is 6th grade'
  12='Lowest grade in school is 7th grade'
  13='Lowest grade in school is 8th grade'
  14='Lowest grade in school is 9th grade'
  15='Lowest grade in school is 10th grade'
  16='Lowest grade in school is 11th grade'
  17='Lowest grade in school is 12th grade' ;
value HIGR2016F
  1='All Ungraded'
  2='Highest grade in school is prekindergarten'
  3='Highest grade in school is kindergarten'
  4='Highest grade in school is transitional kindergarten'
  5='Highest grade in school is transitional first grade'
  6='Highest grade in school is 1st grade'
  7='Highest grade in school is 2nd grade'
  8='Highest grade in school is 3rd grade'
  9='Highest grade in school is 4th grade'
  10='Highest grade in school is 5th grade'
  11='Highest grade in school is 6th grade'
  12='Highest grade in school is 7th grade'
  13='Highest grade in school is 8th grade'
  14='Highest grade in school is 9th grade'
  15='Highest grade in school is 10th grade'
  16='Highest grade in school is 11th grade'
  17='Highest grade in school is 12th grade' ;
value TABFLAG
  1='Schools offering ungraded or grade 1 or above'
  2='Schools offering no grade higher than kindergarten' ;
value TYPOLOGY
  1='Catholic, parochial (Relig=1 and P445=1)'
  2='Catholic, diocesan (Relig=1 and P445=2)'
  3='Catholic, private (Relig=1 and P445=3)'
  4='Other religious, conservative Christian'
  5='Other religious, affiliated with an established religious group or denomination'
  6='Other religious, not affiliated with any established religious group or denomination'
  7='Nonsectarian, regular school (Relig=3 and P415=1 or 7)'
  8='Nonsectarian, special program (Relig=3 and P415=2, 3, 5, 6)'
  9='Nonsectarian, special education (Relig=3 and P415=4)' ;
value RELIG
  1='Catholic (P430=1 and P440=1)'
  2='Other religious (P430=1 and P440 ne 1)'
  3='Nonsectarian (P430=2)' ;
value ORIENT
  1='Roman Catholic'
  2='African Methodist Episcopal'
  3='Amish'
  4='Assembly of God'
  5='Baptist'
  6='Brethren'
  7='Calvinist'
  8='Christian (no specific denomination)'
  9='Church of Christ'
  10='Church of God'
  11='Church of God in Christ'
  12='Church of the Nazarene'
  13='Disciples of Christ'
  14='Episcopal'
  15='Friends'
  16='Greek Orthodox'
  17='Islamic'
  18='Jewish'
  19='Latter Day Saints'
  20='Lutheran Church - Missouri Synod'
  21='Evangelical Lutheran Church in America'
  22='Wisconsin Evangelical Lutheran Synod'
  23='Other Lutheran'
  24='Mennonite'
  25='Methodist'
  26='Pentecostal'
  27='Presbyterian'
  28='Seventh-Day Adventist'
  29='Other'
  30='Nonsectarian' ;
value DIOCESE
  101='Diocese of Birmingham, AL'
  102='Diocese of Mobile, AL'
  201='Archdiocese of Anchorage, AK'
  202='Diocese of Fairbanks, AK'
  203='Diocese of Juneau, AK'
  401='Diocese of Phoenix, AZ'
  402='Diocese of Tucson, AZ'
  501='Diocese of Little Rock, AR'
  601='Archdiocese of Los Angeles, CA'
  602='Archdiocese of San Francisco, CA'
  603='Diocese of Fresno, CA'
  604='Diocese of Monterey, CA'
  605='Diocese of Oakland, CA'
  606='Diocese of Orange, CA'
  607='Diocese of Sacramento, CA'
  608='Diocese of San Bernardino, CA'
  609='Diocese of San Diego, CA'
  610='Diocese of San Jose, CA'
  611='Diocese of Santa Rosa, CA'
  612='Diocese of Stockton, CA'
  801='Archdiocese of Denver, CO'
  802='Diocese of Colorado Springs, CO'
  803='Diocese of Pueblo, CO'
  901='Archdiocese of Hartford, CT'
  902='Diocese of Bridgeport, CT'
  903='Diocese of Norwich, CT'
  1001='Diocese of Wilmington, DE'
  1101='Archdiocese of Washington, DC'
  1201='Archdiocese of Miami, FL'
  1202='Diocese of Pensacola-Tallahassee, FL'
  1203='Diocese of Orlando, FL'
  1204='Diocese of Palm Beach, FL'
  1205='Diocese of St. Augustine, FL'
  1206='Diocese of St. Petersburg, FL'
  1207='Diocese of Venice, FL'
  1301='Archdiocese of Atlanta, GA'
  1302='Diocese of Savannah, GA'
  1501='Diocese of Honolulu, HI'
  1601='Diocese of Boise, ID'
  1701='Archdiocese of Chicago, IL'
  1702='Diocese of Belleville, IL'
  1703='Diocese of Joliet, IL'
  1704='Diocese of Peoria, IL'
  1705='Diocese of Rockford, IL'
  1706='Diocese of Springfield, IL'
  1801='Archdiocese of Indianapolis, IN'
  1802='Diocese of Evansville, IN'
  1803='Diocese of Ft. Wayne-South Bend, IN'
  1804='Diocese of Gary, IN'
  1805='Diocese of Lafayette, IN'
  1901='Archdiocese of Dubuque, IA'
  1902='Diocese of Davenport, IA'
  1903='Diocese of Des Moines, IA'
  1904='Diocese of Sioux City, IA'
  2001='Archdiocese of Kansas City, KS'
  2002='Diocese of Dodge City, KS'
  2003='Diocese of Salina, KS'
  2004='Diocese of Wichita, KS'
  2101='Archdiocese of Louisville, KY'
  2102='Diocese of Covington, KY'
  2103='Diocese of Lexington, KY'
  2104='Diocese of Owensboro, KY'
  2201='Archdiocese of New Orleans, LA'
  2202='Diocese of Alexandria, LA'
  2203='Diocese of Baton Rouge, LA'
  2204='Diocese of Houma-Thibodaux, LA'
  2205='Diocese of Lafayette, LA'
  2206='Diocese of Lake Charles, LA'
  2207='Diocese of Shreveport, LA'
  2301='Diocese of Portland, ME'
  2401='Archdiocese of Baltimore, MD'
  2501='Archdiocese of Boston, MA'
  2502='Diocese of Fall River, MA'
  2503='Diocese of Springfield, MA'
  2504='Diocese of Worcester, MA'
  2601='Archdiocese of Detroit, MI'
  2602='Diocese of Grand Rapids, MI'
  2603='Diocese of Gaylord, MI'
  2604='Diocese of Kalamazoo, MI'
  2605='Diocese of Lansing, MI'
  2606='Diocese of Marquette, MI'
  2607='Diocese of Saginaw, MI'
  2701='Archdiocese of St. Paul-Minneapolis, MN'
  2702='Diocese of Crookston, MN'
  2703='Diocese of Duluth, MN'
  2704='Diocese of New Ulm, MN'
  2705='Diocese of St. Cloud, MN'
  2706='Diocese of Winona, MN'
  2801='Diocese of Biloxi, MS'
  2802='Diocese of Jackson, MS'
  2901='Archdiocese of St. Louis, MO'
  2902='Diocese of Jefferson City, MO'
  2903='Diocese of Kansas City-St. Joseph, MO'
  2904='Diocese of Springfield-Cape Girardeau, MO'
  3001='Diocese of Great Falls-Billings, MT'
  3002='Diocese of Helena, MT'
  3101='Archdiocese of Omaha, NE'
  3102='Diocese of Grand Island, NE'
  3103='Diocese of Lincoln, NE'
  3201='Diocese of Las Vegas, NV'
  3202='Diocese of Reno, NV'
  3301='Diocese of Manchester, NH'
  3401='Archdiocese of Newark, NJ'
  3402='Diocese of Camden, NJ'
  3403='Diocese of Metuchen, NJ'
  3404='Diocese of Paterson, NJ'
  3405='Diocese of Trenton, NJ'
  3501='Archdiocese of Santa Fe, NM'
  3502='Diocese of Gallup, NM'
  3503='Diocese of Las Cruces, NM'
  3601='Archdiocese of New York, NY'
  3602='Diocese of Albany, NY'
  3603='Diocese of Brooklyn, NY'
  3604='Diocese of Buffalo, NY'
  3605='Diocese of Ogdensburg, NY'
  3606='Diocese of Rochester, NY'
  3607='Diocese of Rockville Centre, NY'
  3608='Diocese of Syracuse, NY'
  3701='Diocese of Charlotte, NC'
  3702='Diocese of Raleigh, NC'
  3801='Diocese of Bismarck, ND'
  3802='Diocese of Fargo, ND'
  3901='Archdiocese of Cincinnati, OH'
  3902='Diocese of Cleveland, OH'
  3903='Diocese of Columbus, OH'
  3904='Diocese of Steubenville, OH'
  3905='Diocese of Toledo, OH'
  3906='Diocese of Youngstown, OH'
  4001='Archdiocese of Oklahoma City, OK'
  4002='Diocese of Tulsa, OK'
  4101='Archdiocese of Portland, OR'
  4102='Diocese of Baker, OR'
  4201='Archdiocese of Philadelphia, PA'
  4202='Diocese of Allentown, PA'
  4203='Diocese of Altoona-Johnstown, PA'
  4204='Diocese of Erie, PA'
  4205='Diocese of Greensburg, PA'
  4206='Diocese of Harrisburg, PA'
  4207='Diocese of Pittsburgh, PA'
  4208='Diocese of Scranton, PA'
  4401='Diocese of Providence, RI'
  4501='Diocese of Charleston, SC'
  4601='Diocese of Rapid City, SD'
  4602='Diocese of Sioux Falls, SD'
  4701='Diocese of Knoxville, TN'
  4702='Diocese of Memphis, TN'
  4703='Diocese of Nashville, TN'
  4801='Archdiocese of San Antonio, TX'
  4802='Diocese of Amarillo, TX'
  4803='Diocese of Austin, TX'
  4804='Diocese of Beaumont, TX'
  4805='Diocese of Brownsville, TX'
  4806='Diocese of Corpus Christi, TX'
  4807='Diocese of Dallas, TX'
  4808='Diocese of El Paso, TX'
  4809='Diocese of Ft. Worth, TX'
  4810='Diocese of Galveston-Houston, TX'
  4811='Diocese of Lubbock, TX'
  4812='Diocese of San Angelo, TX'
  4813='Diocese of Tyler, TX'
  4814='Diocese of Victoria, TX'
  4815='Diocese of Laredo, TX'
  4901='Diocese of Salt Lake, UT'
  5001='Diocese of Burlington, VT'
  5101='Diocese of Arlington, VA'
  5102='Diocese of Richmond, VA'
  5301='Archdiocese of Seattle, WA'
  5302='Diocese of Spokane, WA'
  5303='Diocese of Yakima, WA'
  5401='Diocese of Wheeling-Charleston, WV'
  5501='Archdiocese of Milwaukee, WI'
  5502='Diocese of Green Bay, WI'
  5503='Diocese of La Crosse, WI'
  5504='Diocese of Madison, WI'
  5505='Diocese of Superior, WI'
  5601='Diocese of Cheyenne, WY' ;
value LEVEL
  1='Elementary (Students reported in grades prekindergarten through 6 and no students in grades 9 through 12)'
  2='Secondary (Students reported in grades 7 through 12 and no students in grades prekindergarten through 6)'
  3='Combined elementary and secondary (All students ungraded or students reported in grades 6 or below and 9 or above)' ;
value SIZE
  1='Less than 50 students'
  2='50-149 students'
  3='150-299 students'
  4='300-499 students'
  5='500-749 students'
  6='750 students or more' ;
value UCOMMTYP
  1='City (Ulocale12=11, 12, 13)'
  2='Suburb (Ulocale12=21, 22, 23)'
  3='Town (Ulocale12=31, 32, 33)'
  4='Rural (Ulocale12=41, 42, 43)' ;
value F_P135F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P140F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P145F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P150F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P155F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P160F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P165F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P170F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P175F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P180F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P185F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P190F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P195F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P200F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P205F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P210F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P215F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P220F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P225F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P230F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P235F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P240F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P245F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P250F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P255F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P260F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P265F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P270F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P275F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P280F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P285F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P290F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P295F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P300F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P305F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P320F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P330F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P325F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P316F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P318F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P310F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P332F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P335F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P340F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P345F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P350F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P360F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P365F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P370F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P385F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P390F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P395F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P400F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P405F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P410F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P415F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P420F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P425F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P430F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P435F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P440F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P445F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P450F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P455F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P460F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P465F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P467F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P468F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P470F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P480F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P485F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P490F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P492F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P495F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P500F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P505F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P510F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P515F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P520F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P522F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P525F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P530F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P535F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P540F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P542F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P545F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P550F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P555F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P575F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P580F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P585F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P590F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P600F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P602F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P605F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P610F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P620F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P622F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P630F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P635F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P640F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P645F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P650F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P655F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P660F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P661F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P662F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P663F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P664F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
value F_P665F
  0='Not imputed (original data)'
  4='Imputed using donor value from another record on 2015-16 PSS file or using data from the school''s 2013-14 PSS record'
  5='Data adjusted by analyst during review' ;
"""

pss_format = """
format   CSOURCE CSOURCE.;
format      P135 P135F.;
format      P145 P145F.;
format      P155 P155F.;
format      P165 P165F.;
format      P175 P175F.;
format      P185 P185F.;
format      P195 P195F.;
format      P205 P205F.;
format      P215 P215F.;
format      P225 P225F.;
format      P235 P235F.;
format      P245 P245F.;
format      P255 P255F.;
format      P265 P265F.;
format      P275 P275F.;
format      P285 P285F.;
format      P295 P295F.;
format      P335 P335F.;
format      P345 P345F.;
format      P365 P365F.;
format      P415 P415F.;
format      P420 P420F.;
format      P425 P425F.;
format      P430 P430F.;
format      P435 P435F.;
format      P440 P440F.;
format      P445 P445F.;
format      P450 P450F.;
format      P455 P455F.;
format      P460 P460F.;
format      P465 P465F.;
format      P467 P467F.;
format      P468 P468F.;
format      P470 P470F.;
format      P480 P480F.;
format      P485 P485F.;
format      P490 P490F.;
format      P492 P492F.;
format      P495 P495F.;
format      P500 P500F.;
format      P505 P505F.;
format      P510 P510F.;
format      P515 P515F.;
format      P520 P520F.;
format      P522 P522F.;
format      P525 P525F.;
format      P530 P530F.;
format      P535 P535F.;
format      P540 P540F.;
format      P542 P542F.;
format      P545 P545F.;
format      P550 P550F.;
format      P555 P555F.;
format      P575 P575F.;
format      P580 P580F.;
format      P585 P585F.;
format      P590 P590F.;
format      P600 P600F.;
format      P602 P602F.;
format      P605 P605F.;
format      P610 P610F.;
format      P620 P620F.;
format      P622 P622F.;
format      P630 P630F.;
format      P635 P635F.;
format      P640 P640F.;
format      P660 P660F.;
format      P661 P661F.;
format      P663 P663F.;
format      P664 P664F.;
format    REGION REGION.;
format   PSTANSI PSTANSI.;
format ULOCALE16 ULOCALE1F.;
format  LOGR2016 LOGR2016F.;
format  HIGR2016 HIGR2016F.;
format   TABFLAG TABFLAG.;
format  TYPOLOGY TYPOLOGY.;
format     RELIG RELIG.;
format    ORIENT ORIENT.;
format   DIOCESE DIOCESE.;
format     LEVEL LEVEL.;
format      SIZE SIZE.;
format  UCOMMTYP UCOMMTYP.;
format    F_P135 F_P135F.;
format    F_P140 F_P140F.;
format    F_P145 F_P145F.;
format    F_P150 F_P150F.;
format    F_P155 F_P155F.;
format    F_P160 F_P160F.;
format    F_P165 F_P165F.;
format    F_P170 F_P170F.;
format    F_P175 F_P175F.;
format    F_P180 F_P180F.;
format    F_P185 F_P185F.;
format    F_P190 F_P190F.;
format    F_P195 F_P195F.;
format    F_P200 F_P200F.;
format    F_P205 F_P205F.;
format    F_P210 F_P210F.;
format    F_P215 F_P215F.;
format    F_P220 F_P220F.;
format    F_P225 F_P225F.;
format    F_P230 F_P230F.;
format    F_P235 F_P235F.;
format    F_P240 F_P240F.;
format    F_P245 F_P245F.;
format    F_P250 F_P250F.;
format    F_P255 F_P255F.;
format    F_P260 F_P260F.;
format    F_P265 F_P265F.;
format    F_P270 F_P270F.;
format    F_P275 F_P275F.;
format    F_P280 F_P280F.;
format    F_P285 F_P285F.;
format    F_P290 F_P290F.;
format    F_P295 F_P295F.;
format    F_P300 F_P300F.;
format    F_P305 F_P305F.;
format    F_P320 F_P320F.;
format    F_P330 F_P330F.;
format    F_P325 F_P325F.;
format    F_P316 F_P316F.;
format    F_P318 F_P318F.;
format    F_P310 F_P310F.;
format    F_P332 F_P332F.;
format    F_P335 F_P335F.;
format    F_P340 F_P340F.;
format    F_P345 F_P345F.;
format    F_P350 F_P350F.;
format    F_P360 F_P360F.;
format    F_P365 F_P365F.;
format    F_P370 F_P370F.;
format    F_P385 F_P385F.;
format    F_P390 F_P390F.;
format    F_P395 F_P395F.;
format    F_P400 F_P400F.;
format    F_P405 F_P405F.;
format    F_P410 F_P410F.;
format    F_P415 F_P415F.;
format    F_P420 F_P420F.;
format    F_P425 F_P425F.;
format    F_P430 F_P430F.;
format    F_P435 F_P435F.;
format    F_P440 F_P440F.;
format    F_P445 F_P445F.;
format    F_P450 F_P450F.;
format    F_P455 F_P455F.;
format    F_P460 F_P460F.;
format    F_P465 F_P465F.;
format    F_P467 F_P467F.;
format    F_P468 F_P468F.;
format    F_P470 F_P470F.;
format    F_P480 F_P480F.;
format    F_P485 F_P485F.;
format    F_P490 F_P490F.;
format    F_P492 F_P492F.;
format    F_P495 F_P495F.;
format    F_P500 F_P500F.;
format    F_P505 F_P505F.;
format    F_P510 F_P510F.;
format    F_P515 F_P515F.;
format    F_P520 F_P520F.;
format    F_P522 F_P522F.;
format    F_P525 F_P525F.;
format    F_P530 F_P530F.;
format    F_P535 F_P535F.;
format    F_P540 F_P540F.;
format    F_P542 F_P542F.;
format    F_P545 F_P545F.;
format    F_P550 F_P550F.;
format    F_P555 F_P555F.;
format    F_P575 F_P575F.;
format    F_P580 F_P580F.;
format    F_P585 F_P585F.;
format    F_P590 F_P590F.;
format    F_P600 F_P600F.;
format    F_P602 F_P602F.;
format    F_P605 F_P605F.;
format    F_P610 F_P610F.;
format    F_P620 F_P620F.;
format    F_P622 F_P622F.;
format    F_P630 F_P630F.;
format    F_P635 F_P635F.;
format    F_P640 F_P640F.;
format    F_P645 F_P645F.;
format    F_P650 F_P650F.;
format    F_P655 F_P655F.;
format    F_P660 F_P660F.;
format    F_P661 F_P661F.;
format    F_P662 F_P662F.;
format    F_P663 F_P663F.;
format    F_P664 F_P664F.;
format    F_P665 F_P665F.;
"""

pss_conversion = {f.split()[1]: f.split()[0].lower() for f in re.findall('format\s+(.+?)\.?;', pss_format)}

dataset = {
    'ccd': ccd,
    'pss': pss
}

conversion = {
    'ccd': ccd_conversion,
    'pss': pss_conversion
}


def get_labels(sch_type):
    data = dataset[sch_type]
    values = re.findall("(?:VALUE|value)([\s\S]+?(?=;\s?\n))", data)
    print('Found {} values for {}.'.format(len(values), sch_type))

    r = ''
    for value in values:
        h = conversion[sch_type][value.split('\n')[0].strip()]
        labels = re.findall("\s*(['\w -]+='[^']+')", value)

        if len(labels) != value.count('=\''):
            print('CHECK', labels)

        c = ''
        for label in labels:
            l = label.split('=\'')
            c += '\'{}={},'.format(l[1].strip(), l[0].strip())

        c = c[:-1]
        r += "{0}[['{1}']] <- labelled({0}[['{1}']], c({2}))\n".format(sch_type, h, c)

    return r

ccd_R = get_labels('ccd')
pss_R = get_labels('pss')

# python3 data/nces_hs/gen_var_labels.py
with open('data/nces_hs/rclass_issue_13.txt', 'w') as file:
    file.write(ccd_R)
    file.write(pss_R)
