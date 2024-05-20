# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 21:20:58 2024

@author: user
"""

locals().clear()

#BIBLIOTHEQUE
import os
import pandas as pd
from pathlib import Path
 
#CHEMIN D'ACCES
path = os.getcwd()
dir_output_data = os.path.join(path, "output_data")
excel_file_path = os.path.join(dir_output_data, "BFA_Harmonization.xlsx")
# IMPORTATION DES DONNEES
BFA_Harmonization_variables = pd.read_excel(excel_file_path, sheet_name="variables_harmonization")
BFA_Harmonization_description = pd.read_excel(excel_file_path, sheet_name="description")

dataframes = {}
lst_test = BFA_Harmonization_description["Name"]
for i in lst_test:
    i = i + ".dta"
    data = os.path.join(dir_output_data, i) 
    dataframes[i] = pd.read_stata(data, convert_categoricals=False)

Burkina_baseline_2018 = dataframes["Burkina_baseline_2018.dta"]
Burkina_pdm_2019 = dataframes["Burkina_pdm_2019.dta"]
Burkina_ea_2019 = dataframes["Burkina_ea_2019.dta"]
Burkina_ea_2020 = dataframes["Burkina_ea_2020.dta"]
Burkina_ea_2021 = dataframes["Burkina_ea_2021.dta"]
Burkina_pdm_2021 = dataframes["Burkina_pdm_2021.dta"]
Burkina_ea_2022 = dataframes["Burkina_ea_2022.dta"]

# Data consistency  Check
## Drop duplicated observations
Burkina_baseline_2018 = Burkina_baseline_2018[Burkina_baseline_2018['ADMIN1Name'] != None]  
Burkina_baseline_2018 = Burkina_baseline_2018.drop_duplicates()
Burkina_ea_2019 = Burkina_ea_2019[Burkina_ea_2019['ADMIN1Name'] != None]
Burkina_ea_2019 = Burkina_ea_2019.drop_duplicates()
Burkina_ea_2020 = Burkina_ea_2020[Burkina_ea_2020['ADMIN1Name'] != None] 
Burkina_ea_2020 = Burkina_ea_2020.drop_duplicates()
Burkina_ea_2021 = Burkina_ea_2021[Burkina_ea_2021['ADMIN1Name'] != None]  
Burkina_ea_2021 = Burkina_ea_2021.drop_duplicates()
Burkina_pdm_2021 = Burkina_pdm_2021[Burkina_pdm_2021['ADMIN1Name']!= None]  
Burkina_pdm_2021 = Burkina_pdm_2021.drop_duplicates()
Burkina_ea_2022 = Burkina_ea_2022[Burkina_ea_2022['ADMIN1Name'] != None]  
Burkina_ea_2022 = Burkina_ea_2022.drop_duplicates()

## Consent check

#Burkina_baseline_2018 = Burkina_baseline_2018[Burkina_baseline_2018['ADMIN1Name'] == 1]  NA
#Burkina_ea_2019 = Burkina_ea_2019[Burkina_ea_2019['ADMIN1Name'] == 1] NA
Burkina_ea_2020 = Burkina_ea_2020[Burkina_ea_2020['ADMIN1Name'] == 1]
Burkina_ea_2021 = Burkina_ea_2021[Burkina_ea_2021['ADMIN1Name'] == ""]
#Burkina_pdm_2021 = Burkina_pdm_2021[Burkina_pdm_2021['ADMIN1Name'] == ""]
#Burkina_pdm_2021 <- Burkina_pdm_2021  %>% filter(RESPConsent =="") NA
Burkina_ea_2022 = Burkina_ea_2022[Burkina_ea_2022['ADMIN1Name'] == ""]


## ID Check 
Burkina_baseline_2018 = Burkina_baseline_2018.drop_duplicates(subset=['ID'], keep='first')
Burkina_baseline_2018 = Burkina_baseline_2018[Burkina_baseline_2018['ID'] != None]
Burkina_ea_2019 = Burkina_ea_2019.drop_duplicates(subset=['ID'], keep='first')
Burkina_ea_2019 = Burkina_ea_2019[Burkina_ea_2019['ID'] != None]
Burkina_ea_2020 = Burkina_ea_2020.drop_duplicates(subset=['ID'], keep='first')
Burkina_ea_2020 = Burkina_ea_2020[Burkina_ea_2020['ID'] != None]
Burkina_ea_2021['ID'] = range(1, len(Burkina_ea_2021) + 1)
Burkina_pdm_2021 = Burkina_pdm_2021.drop_duplicates(subset=['ID'], keep='first')
Burkina_pdm_2021 = Burkina_pdm_2021[Burkina_pdm_2021['ID'].notna()]
Burkina_ea_2022 = Burkina_ea_2022.drop_duplicates(subset=['ID'], keep='first')
Burkina_ea_2022 = Burkina_ea_2022[Burkina_ea_2022['ID'].notna()]

# Administrative check

Burkina_ea_2022["YEAR"] = 2022
Burkina_ea_2022["SURVEY"] = "Enquête annuelle" 

Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(YEAR= "2022" %>% 
          structure(label = "Annee"))
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
    structure(label = "Nom du pays"))
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))
Burkina_ea_2022$ADMIN1Name<- as_character(Burkina_ea_2022$ADMIN1Name)
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(ADMIN1Name = case_when(
    ADMIN1Name == "CENTRE_NORD" ~  "Centre_Nord",
    ADMIN1Name == "EST" ~  "Est",
    ADMIN1Name == "NORD" ~  "Nord",
    ADMIN1Name == "SAHEL" ~  "Sahel",
    .default = as.character(ADMIN1Name)
  )%>%
structure(label = label(Burkina_ea_2022$ADMIN1Name)))
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(adm1_ocha=case_when(
    ADMIN1Name == "Est" ~  "BF52",
    ADMIN1Name == "Nord" ~ "BF54",
    ADMIN1Name == "Sahel" ~ "BF56",
    ADMIN1Name == "Centre_Nord" ~ "BF49",
    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = "Admin 1 ID"))

Burkina_ea_2022$ADMIN2Name<-as.character(Burkina_ea_2022$ADMIN2Name)
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(ADMIN2Name=case_when(
 ADMIN2Name  ==  "BAM" ~ "Bam",
  ADMIN2Name  ==  "GNAGNA" ~ "Gnagna",
  ADMIN2Name  ==  "GOURMA" ~ "Gourma",
  ADMIN2Name  ==  "NAMENTENGA" ~ "Namentenga",
  ADMIN2Name  ==  "PASSORE" ~ "Passore", 
  ADMIN2Name  ==  "SANMATENGA" ~ "Sanmatenga",
  ADMIN2Name  ==  "SENO" ~ "Seno",
  ADMIN2Name  ==  "YATENGA" ~ "Yatenga",
  ADMIN2Name  ==  "ZONDOMA" ~ "Zondoma",
  #.default = as.character(ADMIN2Name)
)%>%
  structure(label = label(Burkina_ea_2022$ADMIN2Name)))

Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Bam" ~ "BF4901",
  ADMIN2Name  ==  "Gnagna" ~ "BF5201", 
  ADMIN2Name  ==  "Gourma" ~ "BF5202",
  ADMIN2Name  ==  "Namentenga" ~ "BF4902",
  ADMIN2Name  ==  "Passore" ~ "BF5402",
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
  ADMIN2Name  ==  "Yatenga" ~ "BF5403",
  ADMIN2Name  ==  "Zondoma" ~ "BF5404",
    #TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = "Admin 2 ID"))
