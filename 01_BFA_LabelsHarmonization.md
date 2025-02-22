---
title: "WFP datasets wrangling - BFA : Labels harmonization"
author: "Groupe 1"
date: "2024-05-21"
output:
  html_document:
    toc: true
    toc_depth: 3
    toc_float: true
    number_sections: true
    code_folding: show
    keep_md: true

---




```r
library(haven)
library(labelled) # for general functions to work with labelled data
library(tidyverse) # general wrangling
library(dplyr)
library(Hmisc)
library(gtsummary) # to demonstrate automatic use of variable labels in summary tables
library(readxl)
library(foreign)
library(sjPlot)
library(sjmisc)
library(sjlabelled) # for example efc data set with variable labels
library(stringr)
```




```r
rm(list = ls())
```


```r
path = here::here()
dir_input_data = paste0(path, "/output_data")
dir_output_data = paste0(path, "/output_data/Common labels data")
```


```r
BFA_Harmonization_variables <- read_excel(paste0(dir_input_data,"/BFA_Harmonization.xlsx"), 
    sheet = "variables_harmonization")

BFA_Harmonization_description <- read_excel(paste0(dir_input_data,"/BFA_Harmonization.xlsx"), 
    sheet = "description")
```


```r
lst_test = BFA_Harmonization_description$Name

for(i in 1:length(lst_test)) {                              # Head of for-loop
  assign(lst_test[i],                                   # Read and store data frames
         read_dta(paste0(dir_input_data,"/",lst_test[i],".dta")))
}
```


# Data consistency  Check

## Drop duplicated observations


```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))

#Base non disponible
#Burkina_pdm_2019 <- Burkina_pdm_2019 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))

Burkina_ea_2019 <- Burkina_ea_2019 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))
Burkina_ea_2020 <- Burkina_ea_2020 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))
Burkina_ea_2021 <- Burkina_ea_2021 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))
Burkina_ea_2021 <- mutate_all(Burkina_ea_2021, as.character)
Burkina_ea_2021 <- Burkina_ea_2021 %>% filter(ADMIN1Name != "")
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))
Burkina_pdm_2021 <- mutate_all(Burkina_pdm_2021, as.character)
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% filter(ADMIN1Name != "")
Burkina_ea_2022 <- Burkina_ea_2022 %>% dplyr::distinct() %>% dplyr::filter(!is.na(ADMIN1Name))
```

## Consent check


```r
#Burkina_baseline_2018 <- Burkina_baseline_2018  %>% filter(RESPConsent == 1)   NA

#Base non disponible 
#Burkina_pdm_2019 <- Burkina_pdm_2019  %>% filter(RESPConsent == "Oui")

#Burkina_ea_2019 <- Burkina_ea_2019  %>% filter(RESPConsent == 1) NA
Burkina_ea_2020 <- Burkina_ea_2020  %>% filter(RESPConsent ==1)
Burkina_ea_2021 <- Burkina_ea_2021 %>% filter(RESPConsent == "")
#Burkina_pdm_2021 <- Burkina_pdm_2021  %>% filter(RESPConsent =="") NA
Burkina_ea_2022 <- Burkina_ea_2022  %>% filter(RESPConsent == 1)
```

## ID Check 


```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID))
Burkina_pdm_2019 <- Burkina_pdm_2019 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID))
Burkina_ea_2019 <- Burkina_ea_2019 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID))
Burkina_ea_2020 <- Burkina_ea_2020 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID)) 
Burkina_ea_2022 <- Burkina_ea_2022 %>% dplyr::distinct(ID,.keep_all = TRUE) %>% dplyr::filter(!is.na(ID)) 
#Burkina_ea_2021_with_ID <- Burkina_ea_2021 %>% dplyr::distinct(ID) %>% dplyr::filter(!is.na(ID)) 
Burkina_ea_2021$ID <- 1:nrow(Burkina_ea_2021)
Burkina_ea_2021_with_ID <- Burkina_ea_2021
colonnes_caracteres <- sapply(Burkina_ea_2021_with_ID, function(x) !is.numeric(x))
Burkina_ea_2021_with_ID[colonnes_caracteres] <- lapply(Burkina_ea_2021_with_ID[colonnes_caracteres], to_factor)
Burkina_ea_2021_with_ID <- labelled::to_factor(Burkina_ea_2021_with_ID)
write_dta(Burkina_ea_2021_with_ID,"Burkina_ea_2021_with_ID.dta")
```

# Administrative check

```r
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(YEAR= "2022" %>% 
          structure(label = "Annee"))

Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(SURVEY= "Enquête annuelle" %>% 
                  structure(label = "Type d'enquête"))
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
    structure(label = "Nom du pays"))
Burkina_ea_2022 = Burkina_ea_2022 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))
Burkina_ea_2022$ADMIN1Name<- as.character(Burkina_ea_2022$ADMIN1Name)
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
```


```r
Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(YEAR= "2021" %>% 
                  structure(label = "Annee"))

Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(SURVEY= "Enquête annuelle" %>% 
                  structure(label = "Type d'enquête"))
Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
    structure(label = "Nom du pays"))
Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))
# Burkina_ea_2021 = Burkina_ea_2021 %>%
#   dplyr::mutate(ADMIN1Name = case_when(
# 
#     .default = as.character(ADMIN1Name)
#   )%>% 
#   structure(label = label(Burkina_ea_2021$ADMIN1Name)))
Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(adm1_ocha=case_when(
    ADMIN1Name == "Est" ~  "BF52",
    ADMIN1Name == "Nord" ~ "BF54",
    ADMIN1Name == "Sahel" ~ "BF56",
    ADMIN1Name == "Centre_Nord" ~ "BF49",

    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = "Admin 1 ID"))


Burkina_ea_2021$ADMIN2Name<-as.character(Burkina_ea_2021$ADMIN2Name)
# Burkina_ea_2021 = Burkina_ea_2021 %>%
#   dplyr::mutate(ADMIN2Name=case_when(
# 
#   TRUE ~ as.character(ADMIN2Name)
# )%>% 
#   structure(label = label(Burkina_ea_2021$ADMIN2Name)))

Burkina_ea_2021 = Burkina_ea_2021 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Gnagna" ~ "BF5201", 
  ADMIN2Name  ==  "Gourma" ~ "BF5202",
  ADMIN2Name  ==  "Namentenga" ~ "BF4902",
  ADMIN2Name  ==  "Passore" ~ "BF5402",
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
  ADMIN2Name  ==  "Yatenga" ~ "BF5403",
  ADMIN2Name  ==  "Zondoma" ~ "BF5404",
    TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = "Admin 2 ID"))
```



```r
Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(YEAR= "2021" %>% 
                  structure(label = "Annee"))

Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(SURVEY= "PDM" %>% 
                  structure(label = "Type d'enquête"))
Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
    structure(label = "Nom du pays"))
Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))


################# admin1 codification
Burkina_pdm_2021$ADMIN1Name<-as.character(Burkina_pdm_2021$ADMIN1Name)
# Burkina_pdm_2021 = Burkina_pdm_2021 %>%
#   dplyr::mutate(ADMIN1Name=case_when(
#  
#   TRUE ~ as.character(ADMIN1Name)
# )%>% 
#   structure(label = label(Burkina_pdm_2021$ADMIN1Name)))

Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(adm1_ocha=case_when(
    ADMIN1Name == "Est" ~  "BF52",
    ADMIN1Name == "Nord" ~ "BF54",
    ADMIN1Name == "Sahel" ~ "BF56",
    ADMIN1Name == "Centre_Nord" ~ "BF49",
    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = "Admin 1 ID"))



##
Burkina_pdm_2021$ADMIN2Name<-as.character(Burkina_pdm_2021$ADMIN2Name)
# Burkina_pdm_2021 = Burkina_pdm_2021 %>%
#   dplyr::mutate(ADMIN2Name=case_when(
#     
#   TRUE ~ as.character(ADMIN2Name)
# )%>% 
#   structure(label = label(Burkina_pdm_2021$ADMIN2Name)))


Burkina_pdm_2021 = Burkina_pdm_2021 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Gnagna" ~ "BF5201", 
  ADMIN2Name  ==  "Passore" ~ "BF5402",
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
  ADMIN2Name  ==  "Yatenga" ~ "BF5403",
  ADMIN2Name  ==  "Zondoma" ~ "BF5404",
    TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = "Admin 2 ID"))
```



```r
Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(YEAR= "2020" %>% 
                  structure(label = "Annee"))

Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(SURVEY= "Enquête annuelle" %>% 
                  structure(label = "Type d'enquête"))
Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
    structure(label = "Nom du pays"))
Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))


################# admin1 codification
Burkina_ea_2020$ADMIN1Name<-as.character(Burkina_ea_2020$ADMIN1Name)

# Burkina_ea_2020 = Burkina_ea_2020 %>%
#   dplyr::mutate(ADMIN1Name=case_when(
# 
#     TRUE ~ as.character(ADMIN1Name)
#   )%>% 
#     structure(label = label(Burkina_ea_2020$ADMIN1Name)))

Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(adm1_ocha=case_when(
    ADMIN1Name == "Est" ~  "BF52",
    ADMIN1Name == "Nord" ~ "BF54",
    ADMIN1Name == "Sahel" ~ "BF56",
    ADMIN1Name == "Centre_Nord" ~ "BF49",
    
    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = "Admin 1 ID"))


Burkina_ea_2020$ADMIN2Name<-as.character(Burkina_ea_2020$ADMIN2Name)
# Burkina_ea_2020 = Burkina_ea_2020 %>%
#   dplyr::mutate(ADMIN2Name=case_when(
# 
#     TRUE ~ as.character(ADMIN2Name)
#   )%>% 
#     structure(label = label(Burkina_ea_2020$ADMIN2Name)))

Burkina_ea_2020 = Burkina_ea_2020 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Gnagna" ~ "BF5201", 
  ADMIN2Name  ==  "Namentenga" ~ "BF4902",
  ADMIN2Name  ==  "Passore" ~ "BF5402",
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
  ADMIN2Name  ==  "Yatenga" ~ "BF5403",
  ADMIN2Name  ==  "Zondoma" ~ "BF5404",
    TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = "Admin 2 ID"))
```



```r
Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(YEAR= "2019" %>%
                  structure(label = "Annee"))

Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(SURVEY= "Enquête annuelle" %>%
                  structure(label = "Type d'enquête"))
Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>%
                  structure(label = "Nom du pays"))
Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(adm0_ocha= "BF" %>%
                  structure(label = "Admin 0 ID"))


################# admin1 codification
Burkina_ea_2019$ADMIN1Name<-as.character(Burkina_ea_2019$ADMIN1Name)
Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(ADMIN1Name=case_when(
    ADMIN1Name == "CENTRE-NORD" ~  "Centre_Nord",
    ADMIN1Name == "SAHEL" ~ "Sahel",
    TRUE ~ as.character(ADMIN1Name)
  )%>%
    structure(label = label(Burkina_ea_2019$ADMIN1Name)))


Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(adm1_ocha=case_when(
  ADMIN1Name == "Sahel" ~ "BF56",
  ADMIN1Name == "Centre_Nord" ~ "BF49",
    TRUE ~ as.character(ADMIN1Name)
  )%>%
    structure(label = "Admin 1 ID"))



##
Burkina_ea_2019$ADMIN2Name<-as.character(Burkina_ea_2019$ADMIN2Name)
Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(ADMIN2Name=case_when(
  ADMIN2Name  ==  "SAMANTENGA" ~ "Sanmatenga",
  ADMIN2Name  == "SENO" ~ "Seno" ,
    TRUE ~ as.character(ADMIN2Name)
  )%>%
    structure(label = label(Burkina_ea_2019$ADMIN2Name)))


Burkina_ea_2019 = Burkina_ea_2019 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
    TRUE ~ as.character(ADMIN2Name)
  )%>%
    structure(label = "Admin 2 ID"))
```



```r
# Base non disponible


# Burkina_pdm_2019 = Burkina_pdm_2019 %>%
#   dplyr::mutate(YEAR= "2019" %>% 
#                   structure(label = "Annee"))
# 
# Burkina_pdm_2019 = Burkina_pdm_2019 %>%
#   dplyr::mutate(SURVEY= "PDM" %>% 
#                   structure(label = "Type d'enquête"))
# Burkina_pdm_2019 = Burkina_pdm_2019 %>%
#   dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
#                   structure(label = "Nom du pays"))
# Burkina_pdm_2019 = Burkina_pdm_2019 %>%
#   dplyr::mutate(adm0_ocha= "BF" %>% 
#                   structure(label = "Admin 0 ID"))
# 
# 
# ################# admin1 codification
# Burkina_pdm_2019$ADMIN1Name<-as.character(Burkina_pdm_2019$ADMIN1Name)
# 
# Burkina_pdm_2019 = Burkina_pdm_2019 %>%
#   dplyr::mutate(ADMIN1Name=case_when(
# 
#     TRUE ~ as.character(ADMIN1Name)
#   )%>% 
#     structure(label = label(Burkina_pdm_2019$ADMIN1Name)))
# 
# 
# BFA_pdm_2020 = BFA_pdm_2020 %>%
#   dplyr::mutate(adm1_ocha=case_when(
# 
#     TRUE ~ as.character(ADMIN1Name)
#   )%>% 
#     structure(label = "Admin 1 ID"))
# 
```



```r
#Burkina_baseline_2018 <- mutate_all(Burkina_baseline_2018, as.character)

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(YEAR= "2018" %>% 
                  structure(label = "Annee"))

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(SURVEY= "Baseline" %>% 
                  structure(label = "Type d'enquête"))

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(ADMIN0Name= "Burkina Faso" %>% 
                  structure(label = "Nom du pays"))

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(adm0_ocha= "BF" %>% 
                  structure(label = "Admin 0 ID"))

Burkina_baseline_2018$ADMIN1Name<- as.character(Burkina_baseline_2018$ADMIN1Name)

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(ADMIN1Name=case_when(
    ADMIN1Name == "centrnord" ~  "Centre_Nord",
    ADMIN1Name == "sahel" ~ "Sahel",
    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = label(Burkina_baseline_2018$ADMIN1Name)))


Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(adm1_ocha=case_when(
  ADMIN1Name == "Sahel" ~ "BF56",
  ADMIN1Name == "Centre_Nord" ~ "BF49",
    TRUE ~ as.character(ADMIN1Name)
  )%>% 
    structure(label = "Admin 1 ID"))
 
Burkina_baseline_2018$ADMIN2Name<- as.character(Burkina_baseline_2018$ADMIN2Name)

Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(ADMIN2Name=case_when(
  ADMIN2Name  ==  "sanemntenga" ~ "Sanmatenga",
  ADMIN2Name  == "seno" ~ "Seno" ,
    TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = label(Burkina_baseline_2018$ADMIN2Name)))


Burkina_baseline_2018 = Burkina_baseline_2018 %>%
  dplyr::mutate(adm2_ocha=case_when(
  ADMIN2Name  ==  "Sanmatenga" ~ "BF4903",
  ADMIN2Name  ==  "Seno" ~ "BF5602",
    TRUE ~ as.character(ADMIN2Name)
  )%>% 
    structure(label = "Admin 2 ID"))
```


# Indicator checks

## Food consumption score

The Food consumption Score (FCS) is an index that aggregates household-level data on the diversity and frequency of food groups consumed over the last 7 days. It is then weighted according to the relative nutritional value of the consumed food groups. Food groups containing nutritionally dense foods (e.g. animal based products) are given greater weight than those containing less nutritional value (e.g. tubers) as follows: (main staples:2, pulses:3, vegetables:1, fruit:1, meat or fish:4, milk:4, sugar:0.5, oil:0.5).

### FCS : Céréales et tubercules


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-1.png)<!-- -->

```r
# Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
  
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple-6.png)<!-- -->


### FCS : Céréales et tubercules - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSStap = recode(FCSStap,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSStap <- replace(Burkina_baseline_2018$FCSStap, is.na(Burkina_baseline_2018$FCSStap), 0)

Burkina_baseline_2018$FCSStap <- as.numeric(Burkina_baseline_2018$FCSStap)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS FCSStap  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSStap"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2019$FCSStap <- replace(Burkina_ea_2019$FCSStap, is.na(Burkina_ea_2019$FCSStap), 0)

Burkina_ea_2019$FCSStap <- as.numeric(Burkina_ea_2019$FCSStap)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS FCSStap  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSStap"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2020$FCSStap <- replace(Burkina_ea_2020$FCSStap, is.na(Burkina_ea_2020$FCSStap), 0)
Burkina_ea_2020$FCSStap <- as.numeric(Burkina_ea_2020$FCSStap)

#Plot
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS FCSStap  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSStap <- replace(Burkina_ea_2021$FCSStap, is.na(Burkina_ea_2021$FCSStap), 0)
Burkina_ea_2021$FCSStap <- as.numeric(Burkina_ea_2021$FCSStap)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS FCSStap  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSStap <- replace(Burkina_ea_2022$FCSStap, is.na(Burkina_ea_2022$FCSStap), 0)
Burkina_ea_2022$FCSStap <- as.numeric(Burkina_ea_2022$FCSStap)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSStap,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS FCSStap  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
 #Variable FCSStap doesn't exist
Burkina_pdm_2021$FCSStap <- replace(Burkina_pdm_2021$FCSStap, is.na(Burkina_pdm_2021$FCSStap), 0)
Burkina_pdm_2021$FCSStap <- as.numeric(Burkina_pdm_2021$FCSStap)
```



### FCS : Céréales et tubercules - Sources


```r
# Codes d’acquisition des aliments 
# 1 = Production propre (récoltes, élevage) ; 2 = Pêche / Chasse ; 3 = Cueillette ; 4 = Prêts ; 5 = Marché (achat avec des espèces) ; 6 = Marché (achat à crédit) ;
# 7 = Mendicité ; 8 = Troc travail ou biens contre des aliments ; 9 = Dons (aliments) de membres de la famille ou d’amis ; 10 = Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc.
```



```r
expss::val_lab(Burkina_baseline_2018$FCSStapSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-1.png)<!-- -->

```r
Burkina_baseline_2018 <-
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSStapSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8,"8"=9, "9" = 10, "88" = NA_real_)

Burkina_baseline_2018$FCSStapSRf <- labelled::labelled(Burkina_baseline_2018$FCSStapSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSStapSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$FCSStapSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-3.png)<!-- -->

```r
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSStapSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=2,"6"=4,"7"=7,"8"=9, "9" = 10, "88" = NA_real_)

Burkina_ea_2019$FCSStapSRf <- labelled::labelled(Burkina_ea_2019$FCSStapSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSStapSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSStapSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-5.png)<!-- -->

```r
Burkina_ea_2020 <-
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSStapSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4, "9" = 2, "10" = 9, "11"= 9)

Burkina_ea_2020$FCSStapSRf <- labelled::labelled(Burkina_ea_2020$FCSStapSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2020$FCSStapSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSStapSRf)
```

```
## NULL
```

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-7.png)<!-- -->

```r
Burkina_ea_2021 <-
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSStapSRf"),recode,"100"=1,"200"=2,"300"=3, "400"=4,"500"=5,"600"=6, "700"= 7,"800"=8, "900" = 9, "1000" = 10)
Burkina_ea_2021$FCSStapSRf <- labelled::labelled(Burkina_ea_2021$FCSStapSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSStapSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-8.png)<!-- -->

```r
#Pas de variable FCSStapSRf
expss::val_lab(Burkina_pdm_2021$FCSStapSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021$FCSStapSRf <- as.factor(Burkina_pdm_2021$FCSStapSRf)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSStapSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-10.png)<!-- -->

```r
Burkina_ea_2022 <-
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSStapSRf"),recode,"100"=1,"200"=2,"400"=4,"500"=5,"600"=6, "700"= 7,"800"=8, "900" = 9, "1000" = 10)
Burkina_ea_2022$FCSStapSRf <- labelled::labelled(Burkina_ea_2022$FCSStapSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSStapSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSStapSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Staple Source-11.png)<!-- -->



### FCS : Légumineuses


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses-6.png)<!-- -->



### FCS : Légumineuses - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSPulse = recode(FCSPulse,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSPulse <- replace(Burkina_baseline_2018$FCSPulse, is.na(Burkina_baseline_2018$FCSPulse), 0)

Burkina_baseline_2018$FCSPulse <- as.numeric(Burkina_baseline_2018$FCSPulse)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPulse"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2019$FCSPulse <- replace(Burkina_ea_2019$FCSPulse, is.na(Burkina_ea_2019$FCSPulse), 0)
Burkina_ea_2019$FCSPulse <- as.numeric(Burkina_ea_2019$FCSPulse)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSPulse"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2020$FCSPulse <- replace(Burkina_ea_2020$FCSPulse, is.na(Burkina_ea_2020$FCSPulse), 0)
Burkina_ea_2020$FCSPulse <- as.numeric(Burkina_ea_2020$FCSPulse)

#Plot
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSPulse <- replace(Burkina_ea_2021$FCSPulse, is.na(Burkina_ea_2021$FCSPulse), 0)
Burkina_ea_2021$FCSPulse <- as.numeric(Burkina_ea_2021$FCSPulse)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPulse <- replace(Burkina_ea_2022$FCSPulse, is.na(Burkina_ea_2022$FCSPulse), 0)
Burkina_ea_2022$FCSPulse <- as.numeric(Burkina_ea_2022$FCSPulse)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSPulse <- replace(Burkina_pdm_2021$FCSPulse, is.na(Burkina_pdm_2021$FCSPulse), 0)
Burkina_pdm_2021$FCSPulse <- as.numeric(Burkina_pdm_2021$FCSPulse)
#Plot
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPulse,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPulse Nombre de jours ref-6.png)<!-- -->


### FCS : Légumineuses - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSPulseSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8,"8"=9, "9"=10, "88" =NA_real_)
Burkina_baseline_2018$FCSPulseSRf <- labelled::labelled(Burkina_baseline_2018$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-2.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)


expss::val_lab(Burkina_ea_2019$FCSPulseSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=2,"6"=4,"7"=7,"8"=9, "9"=10, "88" =NA_real_)
Burkina_ea_2019$FCSPulseSRf <- labelled::labelled(Burkina_ea_2019$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSPulseSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-5.png)<!-- -->

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6, "6"=8,"10"=8,"11"=8, "7"=9,"8"=4,"9"=2)
Burkina_ea_2020$FCSPulseSRf <- labelled::labelled(Burkina_ea_2020$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2020$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSPulseSRf)
```

```
## NULL
```

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-7.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"100"=1,"200"=2,"300"=3,"400"=4,"500"=5, "600"=6,"700"=7,"800"=8, "900"=9,"1000"=10)
Burkina_ea_2021$FCSPulseSRf <- labelled::labelled(Burkina_ea_2021$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette` = 3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7,`Dons (aliments) de membres de la famille ou d’amis`=9,`Troc travail ou biens contre des aliments`=8,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-8.png)<!-- -->

```r
expss::val_lab(Burkina_pdm_2021$FCSPulseSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021%>% 
 plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-9.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"1"=1,"4"=5,"5"=9, .default=NA_real_)
Burkina_pdm_2021$FCSPulseSRf <- labelled::labelled(Burkina_pdm_2021$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_pdm_2021$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021%>% 
 plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSPulseSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-11.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSPulseSRf"),recode,"100"=1,"400"=4,"500"=5, "600"=6,"700"=7,"900"=9)
Burkina_ea_2022$FCSPulseSRf <- labelled::labelled(Burkina_ea_2022$FCSPulseSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSPulseSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPulseSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Pulses Sources-12.png)<!-- -->


### FCS : Lait et produits laitiers


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy-6.png)<!-- -->


### FCS : Lait et produits laitiers - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSDairy = recode(FCSDairy,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSDairy <- replace(Burkina_baseline_2018$FCSDairy, is.na(Burkina_baseline_2018$FCSDairy), 0)

Burkina_baseline_2018$FCSDairy <- as.numeric(Burkina_baseline_2018$FCSDairy)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSDairy"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2019$FCSDairy <- replace(Burkina_ea_2019$FCSDairy, is.na(Burkina_ea_2019$FCSDairy), 0)
Burkina_ea_2019$FCSDairy <- as.numeric(Burkina_ea_2019$FCSDairy)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSDairy"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2020$FCSDairy <- replace(Burkina_ea_2020$FCSDairy, is.na(Burkina_ea_2020$FCSDairy), 0)
Burkina_ea_2020$FCSDairy <- as.numeric(Burkina_ea_2020$FCSDairy)

#Plot
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSDairy <- replace(Burkina_ea_2021$FCSDairy, is.na(Burkina_ea_2021$FCSDairy), 0)
Burkina_ea_2021$FCSDairy <- as.numeric(Burkina_ea_2021$FCSDairy)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSDairy <- replace(Burkina_ea_2022$FCSDairy, is.na(Burkina_ea_2022$FCSDairy), 0)
Burkina_ea_2022$FCSDairy <- as.numeric(Burkina_ea_2022$FCSDairy)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSDairy <- replace(Burkina_pdm_2021$FCSDairy, is.na(Burkina_pdm_2021$FCSDairy), 0)
Burkina_pdm_2021$FCSDairy <- as.numeric(Burkina_pdm_2021$FCSDairy)
#Plot
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSDairy,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSDairy Nombre de jours ref-6.png)<!-- -->

### FCS : Lait et produits laitiers - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSDairySRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8,"8"= 9, "9"=10, "88" =NA_real_)
Burkina_baseline_2018$FCSDairySRf <- labelled::labelled(Burkina_baseline_2018$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-2.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)

expss::val_lab(Burkina_ea_2019$FCSDairySRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=2,"6"=4,"7"=7,"8"= 9, "9"=10, "88" =NA_real_)
Burkina_ea_2019$FCSDairySRf <- labelled::labelled(Burkina_ea_2019$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSDairySRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-5.png)<!-- -->

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"= 4, "9"=2,"10"=8, "11"=8)
Burkina_ea_2020$FCSDairySRf <- labelled::labelled(Burkina_ea_2020$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2020$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSDairySRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-7.png)<!-- -->

```r
Burkina_ea_2021 <- 
   Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"100"=1,"200"=2,"300"=3,"400"=4,"500"=5, "600"=6,"700"=7,"800"=8, "900"=9,"1000"=10)
Burkina_ea_2021$FCSDairySRf <- labelled::labelled(Burkina_ea_2021$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-8.png)<!-- -->

```r
#A revoir Burkina_pdm_2021

expss::val_lab(Burkina_pdm_2021$FCSDairySRf)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-9.png)<!-- -->

```r
Burkina_pdm_2021 <-
   Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"1"=1,"3"=1,"4"=5, "7"=9,.default
                                         = NA_real_)
Burkina_pdm_2021$FCSDairySRf <- labelled::labelled(Burkina_pdm_2021$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_pdm_2021$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021 %>%
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSDairySRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
  sjPlot::plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-11.png)<!-- -->

```r
Burkina_ea_2022 <-
   Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSDairySRf"),recode,"100"=1,"300"=3,"400"=4,"500"=5, "600"=6,"900"=9)
Burkina_ea_2022$FCSDairySRf <- labelled::labelled(Burkina_ea_2022$FCSDairySRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSDairySRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,FCSDairySRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS Dairy Sources-12.png)<!-- -->


### FCS: Viande, poisson et oeufs


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr-6.png)<!-- -->


### FCS : Viande, poisson et oeufs - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018$FCSPr <- replace(Burkina_baseline_2018$FCSPr, is.na(Burkina_baseline_2018$FCSPr), 0)
Burkina_baseline_2018$FCSPr <- as.numeric(Burkina_baseline_2018$FCSPr)

##### Burkina_ea_2019
Burkina_ea_2019$FCSPr <- replace(Burkina_ea_2019$FCSPr, is.na(Burkina_ea_2019$FCSPr), 0)
Burkina_ea_2019$FCSPr <- as.numeric(Burkina_ea_2019$FCSPr)

##### Burkina_ea_2020
Burkina_ea_2020$FCSPr <- replace(Burkina_ea_2020$FCSPr, is.na(Burkina_ea_2020$FCSPr), 0)
Burkina_ea_2020$FCSPr <- as.numeric(Burkina_ea_2020$FCSPr)

#Plot
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPr Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSPr <- replace(Burkina_ea_2021$FCSPr, is.na(Burkina_ea_2021$FCSPr), 0)
Burkina_ea_2021$FCSPr <- as.numeric(Burkina_ea_2021$FCSPr)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPr Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPr <- replace(Burkina_ea_2022$FCSPr, is.na(Burkina_ea_2022$FCSPr), 0)
Burkina_ea_2022$FCSPr <- as.numeric(Burkina_ea_2022$FCSPr)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPr,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPr Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSPr <- replace(Burkina_pdm_2021$FCSPr, is.na(Burkina_pdm_2021$FCSPr), 0)
Burkina_ea_2022$FCSPr <- as.numeric(Burkina_ea_2022$FCSPr)
```


### FCS: Viande, poisson et oeufs - Sources


```r
#Variable inéxistante
expss::val_lab(Burkina_baseline_2018$FCSPrSRf)
```

```
## NULL
```

```r
Burkina_baseline_2018$FCSPrSRf<- as.factor(Burkina_baseline_2018$FCSPrSRf)
Burkina_baseline_2018 %>% 
   sjPlot::plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-1.png)<!-- -->

```r
# expss::val_lab(Burkina_pdm_2019$FCSPrSRf)
# Burkina_pdm_2019%>% 
#   sjPlot::plot_frq(coord.flip =T,FCSPrSRf,show.na = T)


#Variable inéxistante
expss::val_lab(Burkina_ea_2020$FCSPrSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020$FCSPrSRf <- as.factor(Burkina_ea_2020$FCSPrSRf)
Burkina_ea_2020%>%
  sjPlot::plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-2.png)<!-- -->

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSPrSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4, "9"=2,"10"=8, "11"=8)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSPrSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-4.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSPrSRf"),recode,"100"=1,"200"=2,"400"=4,"500"=5,"600"=6,"900"=9)

Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-5.png)<!-- -->

```r
#Variable inexistente
expss::val_lab(Burkina_pdm_2021$FCSPrSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021$FCSPrSRf <- as.factor(Burkina_pdm_2021$FCSPrSRf)
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-6.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSPrSRf"),recode,"100"=1,"200"=2,"400"=4,"500"=5,"600"=6,"800"=8, "900"=9, "1000"=10)

Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources-7.png)<!-- -->




### FCS : Chair/viande rouge


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatF-6.png)<!-- -->


### FCS : Chair/viande rouge - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSPrMeatF = recode(FCSPrMeatF,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSPrMeatF <- replace(Burkina_baseline_2018$FCSPrMeatF, is.na(Burkina_baseline_2018$FCSPrMeatF), 0)

Burkina_baseline_2018$FCSPrMeatF <- as.numeric(Burkina_baseline_2018$FCSPrMeatF)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatF Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPrMeatF"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)
Burkina_ea_2019$FCSPrMeatF <- replace(Burkina_ea_2019$FCSPrMeatF, is.na(Burkina_ea_2019$FCSPrMeatF), 0)
Burkina_ea_2019$FCSPrMeatF <- as.numeric(Burkina_ea_2019$FCSPrMeatF)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatF Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSPrMeatF <- replace(Burkina_ea_2020$FCSPrMeatF, is.na(Burkina_ea_2020$FCSPrMeatF), 0)
Burkina_ea_2020$FCSPrMeatF <- as.numeric(Burkina_ea_2020$FCSPrMeatF)

##### Burkina_ea_2021
Burkina_ea_2021$FCSPrMeatF <- replace(Burkina_ea_2021$FCSPrMeatF, is.na(Burkina_ea_2021$FCSPrMeatF), 0)
Burkina_ea_2021$FCSPrMeatF <- as.numeric(Burkina_ea_2021$FCSPrMeatF)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatF Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPrMeatF <- replace(Burkina_ea_2022$FCSPrMeatF, is.na(Burkina_ea_2022$FCSPrMeatF), 0)

Burkina_ea_2022$FCSPrMeatF <- as.numeric(Burkina_ea_2022$FCSPrMeatF)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatF Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSPrMeatF <- replace(Burkina_pdm_2021$FCSPrMeatF, is.na(Burkina_pdm_2021$FCSPrMeatF), 0)
Burkina_pdm_2021$FCSPrMeatF <- as.numeric(Burkina_pdm_2021$FCSPrMeatF)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPrMeatF,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatF Nombre de jours ref-5.png)<!-- -->

### FCS : Viande d'organe, telle que: (foie, reins, coeur et / ou autres abats) 



```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrMeatO-6.png)<!-- -->

### FCS : Poissons et coquillage, tels que: (poissons, y compris le thon en conserve, les escargots et / ou d'autres fruits de mer remplacer par des exemples localement pertinents  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSPrMeatO = recode(FCSPrMeatO,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          .default = 0))
Burkina_baseline_2018$FCSPrMeatO <- replace(Burkina_baseline_2018$FCSPrMeatO, is.na(Burkina_baseline_2018$FCSPrMeatO), 0)

Burkina_baseline_2018$FCSPrMeatO <- as.numeric(Burkina_baseline_2018$FCSPrMeatO)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatO Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPrMeatO"),recode,"1 jour"=1,"2 jours"=2,"Pas mangé"=0)
Burkina_ea_2019$FCSPrMeatO <- replace(Burkina_ea_2019$FCSPrMeatO, is.na(Burkina_ea_2019$FCSPrMeatO), 0)
Burkina_ea_2019$FCSPrMeatO <- as.numeric(Burkina_ea_2019$FCSPrMeatO)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatO Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSPrMeatO <- replace(Burkina_ea_2020$FCSPrMeatO, is.na(Burkina_ea_2020$FCSPrMeatO), 0)
  #Not problem

##### Burkina_ea_2021

Burkina_ea_2021$FCSPrMeatO <- replace(Burkina_ea_2021$FCSPrMeatO, is.na(Burkina_ea_2021$FCSPrMeatO), 0)

Burkina_ea_2021$FCSPrMeatO <- as.numeric(Burkina_ea_2021$FCSPrMeatO)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatO Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPrMeatO <- replace(Burkina_ea_2022$FCSPrMeatO, is.na(Burkina_ea_2022$FCSPrMeatO), 0)

Burkina_ea_2022$FCSPrMeatO <- as.numeric(Burkina_ea_2022$FCSPrMeatO)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatO Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSPrMeatO <- replace(Burkina_pdm_2021$FCSPrMeatO, is.na(Burkina_pdm_2021$FCSPrMeatO), 0)
Burkina_pdm_2021$FCSPrMeatO <- as.numeric(Burkina_pdm_2021$FCSPrMeatO)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPrMeatO,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrMeatO Nombre de jours ref-5.png)<!-- -->

### FCS : Poissons et coquillage, tels que: (poissons, y compris le thon en conserve, les escargots et / ou d'autres fruits de mer remplacer par des exemples localement pertinents )



```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS PrFish-6.png)<!-- -->


### FCS : Poissons et coquillage, tels que: (poissons, y compris le thon en conserve, les escargots et / ou d'autres fruits de mer remplacer par des exemples localement pertinents  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSPrFish = recode(FCSPrFish,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          "-3" = 3,
                          .default = 0))
Burkina_baseline_2018$FCSPrFish <- replace(Burkina_baseline_2018$FCSPrFish, is.na(Burkina_baseline_2018$FCSPrFish), 0)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrFish Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPrFish"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"Pas mangé"=0)
Burkina_ea_2019$FCSPrFish <- replace(Burkina_ea_2019$FCSPrFish, is.na(Burkina_ea_2019$FCSPrFish), 0)
Burkina_ea_2019$FCSPrFish <- as.numeric(Burkina_ea_2019$FCSPrFish)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrFish Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSPrFish <- replace(Burkina_ea_2020$FCSPrFish, is.na(Burkina_ea_2020$FCSPrFish), 0)
  #Not problem


##### Burkina_ea_2021

Burkina_ea_2021$FCSPrFish <- replace(Burkina_ea_2021$FCSPrFish, is.na(Burkina_ea_2021$FCSPrFish), 0)

Burkina_ea_2021$FCSPrFish <- as.numeric(Burkina_ea_2021$FCSPrFish)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrFish Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPrFish <- replace(Burkina_ea_2022$FCSPrFish, is.na(Burkina_ea_2022$FCSPrFish), 0)

Burkina_ea_2022$FCSPrFish <- as.numeric(Burkina_ea_2022$FCSPrFish)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrFish Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSPrFish <- replace(Burkina_pdm_2021$FCSPrFish, is.na(Burkina_pdm_2021$FCSPrFish), 0)
Burkina_pdm_2021$FCSPrFish <- as.numeric(Burkina_pdm_2021$FCSPrFish)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPrFish,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrFish Nombre de jours ref-5.png)<!-- -->


### FCS : Oeufs


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-4-6.png)<!-- -->


### FCS : Oeufs - Nombre de jours


```r
##### Burkina_baseline_2018

Burkina_baseline_2018$FCSPrEgg <- replace(Burkina_baseline_2018$FCSPrEgg, is.na(Burkina_baseline_2018$FCSPrEgg), 0)

Burkina_baseline_2018$FCSPrEgg <- as.numeric(Burkina_baseline_2018$FCSPrEgg)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrEgg Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSPrEgg"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"Pas mangé"=0)

Burkina_ea_2019$FCSPrEgg <- as.numeric(Burkina_ea_2019$FCSPrEgg)

#Plot
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrEgg Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
  #Not problem

##### Burkina_ea_2021

Burkina_ea_2021$FCSPrEgg <- replace(Burkina_ea_2021$FCSPrEgg, is.na(Burkina_ea_2021$FCSPrEgg), 0)

Burkina_ea_2021$FCSPrEgg <- as.numeric(Burkina_ea_2021$FCSPrEgg)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrEgg Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSPrEgg <- replace(Burkina_ea_2022$FCSPrEgg, is.na(Burkina_ea_2022$FCSPrEgg), 0)

Burkina_ea_2022$FCSPrEgg <- as.numeric(Burkina_ea_2022$FCSPrEgg)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrEgg Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021

Burkina_pdm_2021$FCSPrEgg <- as.numeric(Burkina_pdm_2021$FCSPrEgg)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSPrEgg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSPrEgg Nombre de jours ref-5.png)<!-- -->


### FCS : Légumes et feuilles , tels que : (épinards, oignons, tomates, carottes, poivrons, haricots verts, laitue, etc)


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg-6.png)<!-- -->

### FCS : Légumes et feuilles , tels que : (épinards, oignons, tomates, carottes, poivrons, haricots verts, laitue, etc)  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSVeg = recode(FCSVeg,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSVeg <- replace(Burkina_baseline_2018$FCSVeg, is.na(Burkina_baseline_2018$FCSVeg), 0)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVeg Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019$FCSVeg <- replace(Burkina_ea_2019$FCSVeg, is.na(Burkina_ea_2019$FCSVeg), 0)
Burkina_ea_2019$FCSVeg <- as.numeric(Burkina_ea_2019$FCSVeg)


##### Burkina_ea_2020
Burkina_ea_2020$FCSVeg <- replace(Burkina_ea_2020$FCSVeg, is.na(Burkina_ea_2020$FCSVeg), 0)
  #Not problem


##### Burkina_ea_2021
Burkina_ea_2021$FCSVeg <- replace(Burkina_ea_2021$FCSVeg, is.na(Burkina_ea_2021$FCSVeg), 0)
Burkina_ea_2021$FCSVeg <- as.numeric(Burkina_ea_2021$FCSVeg)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVeg Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSVeg <- replace(Burkina_ea_2022$FCSVeg, is.na(Burkina_ea_2022$FCSVeg), 0)
Burkina_ea_2022$FCSVeg <- as.numeric(Burkina_ea_2022$FCSVeg)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVeg Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSVeg <- replace(Burkina_pdm_2021$FCSVeg, is.na(Burkina_pdm_2021$FCSVeg), 0)
Burkina_pdm_2021$FCSVeg <- as.numeric(Burkina_pdm_2021$FCSVeg)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSVeg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVeg Nombre de jours ref-4.png)<!-- -->



### FCS : Légumes et feuilles , tels que : (épinards, oignons, tomates, carottes, poivrons, haricots verts, laitue, etc) - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSVegSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSVegSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=6,"7"=8,"8"=9, "9" = 10, "88"=NA_real_)
Burkina_baseline_2018$FCSVegSRf <- labelled::labelled(Burkina_baseline_2018$FCSVegSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSVegSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-2.png)<!-- -->

```r
#expss::val_lab(Burkina_pdm_2019$FCSVegSRf)
#Burkina_pdm_2019 %>% 
  #sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)

#variable non disponible
expss::val_lab(Burkina_ea_2019$FCSVegSRf)
```

```
## NULL
```

```r
Burkina_ea_2019$FCSVegSRf <- as.factor(Burkina_ea_2019$FCSVegSRf)
Burkina_ea_2019 %>%
sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSVegSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020 %>%
sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-4.png)<!-- -->

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate_at(c("FCSVegSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4, "9" = 2,"10"=8,"11"=8)
Burkina_ea_2020$FCSVegSRf <- labelled::labelled(Burkina_ea_2020$FCSVegSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2020$FCSVegSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSVegSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>%
sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-6.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSVegSRf"),recode,"100"=1,"300"=3,"400"=4,"500"=5,"600"=6,"800"=8,"900"=9,"1000"=10)
Burkina_ea_2021$FCSVegSRf <- labelled::labelled(Burkina_ea_2021$FCSVegSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSVegSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-7.png)<!-- -->

```r
#A revoir Burkina_pdm_2021

expss::val_lab(Burkina_pdm_2021$FCSVegSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-8.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSVegSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=10,"6"=8, "7"=9, "8"=4, "9"=2, "10"=8, .default=NA_real_)
Burkina_pdm_2021$FCSVegSRf <- labelled::labelled(Burkina_pdm_2021$FCSVegSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_pdm_2021$FCSVegSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSVegSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
sjPlot::plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-10.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSVegSRf"),recode,"100"=1,"300"=3,"500"=5,"600"=6,"800"=8,"900"=9)
Burkina_ea_2022$FCSVegSRf <- labelled::labelled(Burkina_ea_2022$FCSVegSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSVegSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSVegSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVeg Sources-11.png)<!-- -->


### FCS : Légumes oranges (légumes riches en Vitamine A)


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-5.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegOrg-6.png)<!-- -->


### FCS : Légumes oranges (légumes riches en Vitamine A)  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSVegOrg = recode(FCSVegOrg,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "5" = 5))
Burkina_baseline_2018$FCSVegOrg <- replace(Burkina_baseline_2018$FCSVegOrg, is.na(Burkina_baseline_2018$FCSVegOrg), 0)

#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegOrg Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSVegOrg"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"Pas mangé"=0)
Burkina_ea_2019$FCSVegOrg <- replace(Burkina_ea_2019$FCSVegOrg, is.na(Burkina_ea_2019$FCSVegOrg), 0)
Burkina_ea_2019$FCSVegOrg <- as.numeric(Burkina_ea_2019$FCSVegOrg)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegOrg Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSVegOrg <- replace(Burkina_ea_2020$FCSVegOrg, is.na(Burkina_ea_2020$FCSVegOrg), 0)
Burkina_ea_2020$FCSVegOrg <- as.numeric(Burkina_ea_2020$FCSVegOrg)

##### Burkina_ea_2021
Burkina_ea_2021$FCSVegOrg <- replace(Burkina_ea_2021$FCSVegOrg, is.na(Burkina_ea_2021$FCSVegOrg), 0)

Burkina_ea_2021$FCSVegOrg <- as.numeric(Burkina_ea_2021$FCSVegOrg)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegOrg Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSVegOrg <- replace(Burkina_ea_2022$FCSVegOrg, is.na(Burkina_ea_2022$FCSVegOrg), 0)

Burkina_ea_2022$FCSVegOrg <- as.numeric(Burkina_ea_2022$FCSVegOrg)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegOrg Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSVegOrg <- replace(Burkina_pdm_2021$FCSVegOrg, is.na(Burkina_pdm_2021$FCSVegOrg), 0)
Burkina_pdm_2021$FCSVegOrg <- as.numeric(Burkina_pdm_2021$FCSVegOrg)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSVegOrg,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegOrg Nombre de jours ref-5.png)<!-- -->


### FCS : Légumes à feuilles vertes,,  tels que : ( épinards, brocoli, amarante et/ou autres feuilles vert foncé , feuilles de manioc )


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-5.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSVegGre-6.png)<!-- -->



### FCS : Légumes à feuilles vertes,,  tels que : ( épinards, brocoli, amarante et/ou autres feuilles vert foncé , feuilles de manioc )  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSVegGre = recode(FCSVegGre,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSVegGre <- replace(Burkina_baseline_2018$FCSVegGre, is.na(Burkina_baseline_2018$FCSVegGre), 0)

Burkina_baseline_2018$FCSVegGre <- as.numeric(Burkina_baseline_2018$FCSVegGre)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegGre Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019$FCSVegGre <- replace(Burkina_ea_2019$FCSVegGre, is.na(Burkina_ea_2019$FCSVegGre), 0)
Burkina_ea_2019$FCSVegGre <- as.numeric(Burkina_ea_2019$FCSVegGre)
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegGre Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSVegGre <- replace(Burkina_ea_2020$FCSVegGre, is.na(Burkina_ea_2020$FCSVegGre), 0)
Burkina_ea_2020$FCSVegGre <- as.numeric(Burkina_ea_2020$FCSVegGre)


##### Burkina_ea_2021
Burkina_ea_2021$FCSVegGre <- replace(Burkina_ea_2021$FCSVegGre, is.na(Burkina_ea_2021$FCSVegGre), 0)
Burkina_ea_2021$FCSVegGre <- as.numeric(Burkina_ea_2021$FCSVegGre)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegGre Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSVegGre <- replace(Burkina_ea_2022$FCSVegGre, is.na(Burkina_ea_2022$FCSVegGre), 0)
Burkina_ea_2022$FCSVegGre <- as.numeric(Burkina_ea_2022$FCSVegGre)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegGre Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSVegGre <- replace(Burkina_pdm_2021$FCSVegGre, is.na(Burkina_pdm_2021$FCSVegGre), 0)
Burkina_pdm_2021$FCSVegGre <- as.numeric(Burkina_pdm_2021$FCSVegGre)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSVegGre,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSVegGre Nombre de jours ref-5.png)<!-- -->


### FCS : Fruits,  tels que : (banane, pomme, citron, mangue, papaye, abricot, pêche, etc)


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-5.png)<!-- -->

```r
 #Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit-6.png)<!-- -->


### FCS : Fruits,  tels que : (banane, pomme, citron, mangue, papaye, abricot, pêche, etc)  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSFruit = recode(FCSFruit,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSFruit <- replace(Burkina_baseline_2018$FCSFruit, is.na(Burkina_baseline_2018$FCSFruit), 0)

Burkina_baseline_2018$FCSFruit <- as.numeric(Burkina_baseline_2018$FCSFruit)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFruit Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019$FCSFruit <- replace(Burkina_ea_2019$FCSFruit, is.na(Burkina_ea_2019$FCSFruit), 0)
Burkina_ea_2019$FCSFruit <- as.numeric(Burkina_ea_2019$FCSFruit)

##### Burkina_ea_2020
Burkina_ea_2020$FCSFruit <- replace(Burkina_ea_2020$FCSFruit, is.na(Burkina_ea_2020$FCSFruit), 0)
Burkina_ea_2020$FCSFruit <- as.numeric(Burkina_ea_2020$FCSFruit)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFruit Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSFruit <- replace(Burkina_ea_2021$FCSFruit, is.na(Burkina_ea_2021$FCSFruit), 0)
Burkina_ea_2021$FCSFruit <- as.numeric(Burkina_ea_2021$FCSFruit)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFruit Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSFruit <- replace(Burkina_ea_2022$FCSFruit, is.na(Burkina_ea_2022$FCSFruit), 0)
Burkina_ea_2022$FCSFruit <- as.numeric(Burkina_ea_2022$FCSFruit)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFruit Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSFruit <- replace(Burkina_pdm_2021$FCSFruit, is.na(Burkina_pdm_2021$FCSFruit), 0)
Burkina_pdm_2021$FCSFruit <- as.numeric(Burkina_pdm_2021$FCSFruit)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSFruit,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFruit Nombre de jours ref-5.png)<!-- -->



### FCS : Fruits,  tels que : (banane, pomme, citron, mangue, papaye, abricot, pêche, etc) - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSFruitSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSFruitSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8, "8"=9, "9"=10, "88"=NA_real_)
Burkina_baseline_2018$FCSFruitSRf <- labelled::labelled(Burkina_baseline_2018$FCSFruitSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSFruitSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-2.png)<!-- -->

```r
#####Burkina_pdm_2019

#No observations for the variables
expss::val_lab(Burkina_ea_2019$FCSFruitSRf)
```

```
## NULL
```

```r
Burkina_ea_2019$FCSFruitSRf <- as.factor(Burkina_ea_2019$FCSFruitSRf)
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-3.png)<!-- -->

```r
#view(table(Burkina_ea_2019$FCSFruitSRf))


expss::val_lab(Burkina_ea_2020$FCSFruitSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-4.png)<!-- -->

```r
Burkina_ea_2020 <-
Burkina_ea_2020%>%  
  dplyr::mutate_at(c("FCSFruitSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4,"9"=2,"10"=8,"11"=8)
Burkina_ea_2020$FCSFruitSRf <- labelled::labelled(Burkina_ea_2020$FCSFruitSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_ea_2020$FCSFruitSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSFruitSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-6.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSFruitSRf"),recode,"100"=1,"300"=3,"500"=5,"600"=6,"800"=8, "1000"=10)
Burkina_ea_2021$FCSFruitSRf <- labelled::labelled(Burkina_ea_2021$FCSFruitSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSFruitSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-7.png)<!-- -->

```r
expss::val_lab(Burkina_pdm_2021$FCSFruitSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-8.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSFruitSRf"),recode,"1"=1,"3"=1,"4"=5,"7"=9,"9"=2, .default = NA_real_)
Burkina_pdm_2021$FCSFruitSRf <- labelled::labelled(Burkina_pdm_2021$FCSFruitSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSFruitSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
  sjPlot::plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-10.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSFruitSRf"),recode,"100"=1,"200"=2,"300"=3,"500"=5,"600"=6,"900"=9)
Burkina_ea_2022$FCSFruitSRf <- labelled::labelled(Burkina_ea_2022$FCSFruitSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSFruitSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSFruitSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFruit Sources-11.png)<!-- -->

### FCS : Huile/matières grasses/beurre: tels que (huile végétale, huile de palme, beurre de karité, margarine, autres huiles / matières grasses)


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-5.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat-6.png)<!-- -->



### FCS : Huile/matières grasses/beurre: tels que (huile végétale, huile de palme, beurre de karité, margarine, autres huiles / matières grasses)  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSFat = recode(FCSFat,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSFat <- replace(Burkina_baseline_2018$FCSFat, is.na(Burkina_baseline_2018$FCSFat), 0)

Burkina_baseline_2018$FCSFat <- as.numeric(Burkina_baseline_2018$FCSFat)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFat Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019$FCSFat <- replace(Burkina_ea_2019$FCSFat, is.na(Burkina_ea_2019$FCSFat), 0)
Burkina_ea_2019$FCSFat <- as.numeric(Burkina_ea_2019$FCSFat)

##### Burkina_ea_2020
Burkina_ea_2020$FCSFat <- replace(Burkina_ea_2020$FCSFat, is.na(Burkina_ea_2020$FCSFat), 0)
Burkina_ea_2020$FCSFat <- as.numeric(Burkina_ea_2020$FCSFat)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFat Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSFat <- replace(Burkina_ea_2021$FCSFat, is.na(Burkina_ea_2021$FCSFat), 0)
Burkina_ea_2021$FCSFat <- as.numeric(Burkina_ea_2021$FCSFat)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFat Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSFat <- replace(Burkina_ea_2022$FCSFat, is.na(Burkina_ea_2022$FCSFat), 0)
Burkina_ea_2022$FCSFat <- as.numeric(Burkina_ea_2022$FCSFat)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFat Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSFat <- replace(Burkina_pdm_2021$FCSFat, is.na(Burkina_pdm_2021$FCSFat), 0)
Burkina_pdm_2021$FCSFat <- as.numeric(Burkina_pdm_2021$FCSFat)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSFat,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSFat Nombre de jours ref-5.png)<!-- -->



### FCS : Huile/matières grasses/beurre: tels que (huile végétale, huile de palme, beurre de karité, margarine, autres huiles / matières grasses) - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSFatSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSFatSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8, "8"=9, "9"=10, "88"=NA_real_)
Burkina_baseline_2018$FCSFatSRf <- labelled::labelled(Burkina_baseline_2018$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-2.png)<!-- -->

```r
#####Burkina_pdm_2019

#No observations for the variables
expss::val_lab(Burkina_ea_2019$FCSFatSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019$FCSFatSRf <- as.factor(Burkina_ea_2019$FCSFatSRf)
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSFatSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2, "5"=2,"6"=4,"7"=7,"8"=9,"9"=10, "88"=NA_real_)
Burkina_ea_2019$FCSFatSRf <- labelled::labelled(Burkina_ea_2019$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSFatSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-5.png)<!-- -->

```r
Burkina_ea_2020 <-
Burkina_ea_2020%>%  
  dplyr::mutate_at(c("FCSFatSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4,"9"=2,"10"=8,"11"=8)
Burkina_ea_2020$FCSFatSRf <- labelled::labelled(Burkina_ea_2020$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))

expss::val_lab(Burkina_ea_2020$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSFatSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-7.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSFatSRf"),recode,"100"=1,"300"=3,"400"=4, "500"=5,"600"=6,"900"=9, "1000"=10)
Burkina_ea_2021$FCSFatSRf <- labelled::labelled(Burkina_ea_2021$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-8.png)<!-- -->

```r
###PROBLEME
expss::val_lab(Burkina_pdm_2021$FCSFatSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
   sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-9.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSFatSRf"),recode,"4"=5,"5"=10,"7" = 9, .default=NA_real_)
Burkina_pdm_2021$FCSFatSRf <- labelled::labelled(Burkina_pdm_2021$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_pdm_2021$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021 %>% 
   sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSFatSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
  sjPlot::plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-11.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSFatSRf"),recode,"100"=1,"300"=3,"400" = 4, "500"=5,"600"=6,"800"=8, "900"=9, "1000"=10)
Burkina_ea_2022$FCSFatSRf <- labelled::labelled(Burkina_ea_2022$FCSFatSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSFatSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSFatSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSFat Sources-12.png)<!-- -->



### FSC : Sucre ou sucreries, tels que (sucre, miel, confiture, gâteau, bonbons, biscuits, viennoiserie et autres produits sucrés (boissons sucrées)  )


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-5.png)<!-- -->

```r
# Burkina_pdm_2019%>% 
#   sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar-6.png)<!-- -->


### FCS : Sucre ou sucreries, tels que (sucre, miel, confiture, gâteau, bonbons, biscuits, viennoiserie et autres produits sucrés (boissons sucrées)  )  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSSugar = recode(FCSSugar,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSSugar <- replace(Burkina_baseline_2018$FCSSugar, is.na(Burkina_baseline_2018$FCSSugar), 0)

Burkina_baseline_2018$FCSSugar <- as.numeric(Burkina_baseline_2018$FCSSugar)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSSugar Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019$FCSSugar <- replace(Burkina_ea_2019$FCSSugar, is.na(Burkina_ea_2019$FCSSugar), 0)
Burkina_ea_2019$FCSSugar <- as.numeric(Burkina_ea_2019$FCSSugar)

##### Burkina_ea_2020
Burkina_ea_2020$FCSSugar <- replace(Burkina_ea_2020$FCSSugar, is.na(Burkina_ea_2020$FCSSugar), 0)
Burkina_ea_2020$FCSSugar <- as.numeric(Burkina_ea_2020$FCSSugar)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSSugar Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSSugar <- replace(Burkina_ea_2021$FCSSugar, is.na(Burkina_ea_2021$FCSSugar), 0)
Burkina_ea_2021$FCSSugar <- as.numeric(Burkina_ea_2021$FCSSugar)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSSugar Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSSugar <- replace(Burkina_ea_2022$FCSSugar, is.na(Burkina_ea_2022$FCSSugar), 0)
Burkina_ea_2022$FCSSugar <- as.numeric(Burkina_ea_2022$FCSSugar)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSSugar Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$FCSSugar <- replace(Burkina_pdm_2021$FCSSugar, is.na(Burkina_pdm_2021$FCSSugar), 0)
Burkina_pdm_2021$FCSSugar <- as.numeric(Burkina_pdm_2021$FCSSugar)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSSugar,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSSugar Nombre de jours ref-5.png)<!-- -->

### FSC : Sucre ou sucreries, tels que (sucre, miel, confiture, gâteau, bonbons, biscuits, viennoiserie et autres produits sucrés (boissons sucrées)  ) - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSSugarSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSSugarSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8, "8"=9, "9"=10, "88"=NA_real_)
Burkina_baseline_2018$FCSSugarSRf <- labelled::labelled(Burkina_baseline_2018$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-2.png)<!-- -->

```r
#####Burkina_pdm_2019

#No observations for the variables
expss::val_lab(Burkina_ea_2019$FCSSugarSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019$FCSSugarSRf <-as.factor(Burkina_ea_2019$FCSSugarSRf)

Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSSugarSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2, "5"=2,"6"=4,"7"=7,"8"=9,"9"=10, "88"=NA_real_)
Burkina_ea_2019$FCSSugarSRf <- labelled::labelled(Burkina_ea_2019$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSSugarSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-5.png)<!-- -->

```r
Burkina_ea_2020 <-
Burkina_ea_2020%>%  
  dplyr::mutate_at(c("FCSSugarSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4,"9"=2,"10"=8,"11"=8)
Burkina_ea_2020$FCSSugarSRf <- labelled::labelled(Burkina_ea_2020$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_ea_2020$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSSugarSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-7.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSSugarSRf"),recode,"100"=1,"300"=3,"400"=4, "500"=5,"600"=6,"900"=9)
Burkina_ea_2021$FCSSugarSRf <- labelled::labelled(Burkina_ea_2021$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-8.png)<!-- -->

```r
expss::val_lab(Burkina_pdm_2021$FCSSugarSRf)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
   sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-9.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSSugarSRf"),recode,"4"=5, .default=NA_real_)
Burkina_pdm_2021$FCSSugarSRf <- labelled::labelled(Burkina_pdm_2021$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
expss::val_lab(Burkina_pdm_2021$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021 %>% 
   sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSSugarSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
  sjPlot::plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-11.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSSugarSRf"),recode,"100"=1,"300"=3,"400" = 4, "500"=5,"600"=6,"700"=7, "900"=9)
Burkina_ea_2022$FCSSugarSRf <- labelled::labelled(Burkina_ea_2022$FCSSugarSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSSugarSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSSugarSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSSugar Sources-12.png)<!-- -->



### FCS : Condiments/épices: tels que (thé, café/cacao, sel, ail, épices, levure/levure chimique, tomate/sauce, viande ou poisson comme condiment, condiments incluant des petites quantités de lait/thé, café.) ?


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-1.png)<!-- -->

```r
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-4.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-5.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
 # sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond-6.png)<!-- -->

### FCS : Condiments/épices: tels que (thé, café/cacao, sel, ail, épices, levure/levure chimique, tomate/sauce, viande ou poisson comme condiment, condiments incluant des petites quantités de lait/thé, café.) ? - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(FCSCond = recode(FCSCond,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$FCSCond <- replace(Burkina_baseline_2018$FCSCond, is.na(Burkina_baseline_2018$FCSCond), 0)

Burkina_baseline_2018$FCSCond <- as.numeric(Burkina_baseline_2018$FCSCond)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019
Burkina_ea_2019 <-
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSCond"),recode,"1 jour"=1,"2 jours"=2,"3 jours"=3,"4 jours"=4,"5 jours"=5,"6 jours"=6,"7 jours"=7,"Pas mangé"=0)

Burkina_ea_2019$FCSCond <- as.numeric(Burkina_ea_2019$FCSCond)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$FCSCond <- as.numeric(Burkina_ea_2020$FCSCond)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$FCSCond <- as.numeric(Burkina_ea_2021$FCSCond)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$FCSCond <- as.numeric(Burkina_ea_2022$FCSCond)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021

Burkina_pdm_2021$FCSCond <- as.numeric(Burkina_pdm_2021$FCSCond)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSCond,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS  FCSCond Nombre de jours ref-6.png)<!-- -->


### FCS : Condiments/épices: tels que (thé, café/cacao, sel, ail, épices, levure/levure chimique, tomate/sauce, viande ou poisson comme condiment, condiments incluant des petites quantités de lait/thé, café.) ? - Sources


```r
expss::val_lab(Burkina_baseline_2018$FCSCondSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au march? avec cash 
##                                           2 
##                    Achat au march? ? cr?dit 
##                                           3 
##                   Chasse, cueillette, p?che 
##                                           4 
##                                     Emprunt 
##                                           5 
##                     Mendier pour se nourrir 
##                                           6 
##                                     Echange 
##                                           7 
##        Dons (famille, voisins, communaut??) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate_at(c("FCSCondSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2,"5"=4,"6"=7,"7"=8, "8"=9, "9"=10, "88"=NA_real_)
Burkina_baseline_2018$FCSCondSRf <- labelled::labelled(Burkina_baseline_2018$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_baseline_2018$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-2.png)<!-- -->

```r
#####Burkina_pdm_2019

#No observations for the variables
expss::val_lab(Burkina_ea_2019$FCSCondSRf)
```

```
##                           Propre production 
##                                           1 
##                   Achat au marché avec cash 
##                                           2 
##                    Achat au marché à crédit 
##                                           3 
##                   Chasse, cueillette, pêche 
##                                           4 
##                     Chasse/cueillette/pêche 
##                                           5 
##                                     Emprunt 
##                                           6 
##                     Mendier pour se nourrir 
##                                           7 
##        Dons (famille, voisins, communauté…) 
##                                           8 
## Aide alimentaire (ONGs, PAM,  Gouvernement) 
##                                           9 
##                              Non applicable 
##                                          88
```

```r
Burkina_ea_2019$FCSCondSRf<-as.factor(Burkina_ea_2019$FCSCondSRf)
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate_at(c("FCSCondSRf"),recode,"1"=1,"2"=5,"3"=6,"4"=2, "5"=2,"6"=4,"7"=7,"8"=9,"9"=10, "88"=NA_real_)
Burkina_ea_2019$FCSCondSRf <- labelled::labelled(Burkina_ea_2019$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2019$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$FCSCondSRf)
```

```
##                                           Propre production pluviale 
##                                                                    1 
##                                    Propres productions Contre saison 
##                                                                    2 
##                                         Propres productions animales 
##                                                                    3 
##                                                               Achats 
##                                                                    4 
##  Assistance alimentaire (transferts monétaires ou des bons d'achats) 
##                                                                    5 
##                         Nourriture contre travail avec un projet/ONG 
##                                                                    6 
##                                                           Dons/Zakat 
##                                                                    7 
##                                    Emprunt, (crédit  de la boutique) 
##                                                                    8 
##                                              Chasse/cueillette/pêche 
##                                                                    9 
## Travail contre nourriture dans le cadre de la main d'œuvre ordinaire 
##                                                                   10 
##                                                         Echange/troc 
##                                                                   11
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-5.png)<!-- -->

```r
Burkina_ea_2020 <-
Burkina_ea_2020%>%  
  dplyr::mutate_at(c("FCSCondSRf"),recode,"1"=1,"2"=1,"3"=1,"4"=5,"5"=6,"6"=8,"7"=9,"8"=4,"9"=2,"10"=8,"11"=8)
Burkina_ea_2020$FCSCondSRf <- labelled::labelled(Burkina_ea_2020$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))

expss::val_lab(Burkina_ea_2020$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$FCSCondSRf)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-7.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate_at(c("FCSCondSRf"),recode,"100"=1,"400"=4, "500"=5,"600"=6,"800"=8, "900"=9, "1000"=10)
Burkina_ea_2021$FCSCondSRf <- labelled::labelled(Burkina_ea_2021$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2021$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-8.png)<!-- -->

```r
# expss::val_lab(Burkina_pdm_2021$FCSCondSRf)
#Burkina_pdm_2021 %>% 
   #sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate_at(c("FCSCondSRf"),recode,"1"=1,"2" = 2, "4"=5,"9"=2, .default=NA_real_)
Burkina_pdm_2021$FCSCondSRf <- labelled::labelled(Burkina_pdm_2021$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_pdm_2021$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$FCSCondSRf)
```

```
##                               Production propre (récoltes, élevage) 
##                                                                 100 
##                                                      Pêche / Chasse 
##                                                                 200 
##                                                          Cueillette 
##                                                                 300 
##                                                               Prêts 
##                                                                 400 
##                                     Marché (achat avec des espèces) 
##                                                                 500 
##                                             Marché (achat à crédit) 
##                                                                 600 
##                                                           Mendicité 
##                                                                 700 
##                           Troc travail ou biens contre des aliments 
##                                                                 800 
##                  Dons (aliments) de membres de la famille ou d'amis 
##                                                                 900 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc. 
##                                                                1000
```

```r
Burkina_ea_2022 %>%
  sjPlot::plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-10.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate_at(c("FCSCondSRf"),recode,"100"=1,"400" = 4, "500"=5,"600"=6,"700"=7, "900"=9)
Burkina_ea_2022$FCSCondSRf <- labelled::labelled(Burkina_ea_2022$FCSCondSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette`=3, `Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8, `Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(Burkina_ea_2022$FCSCondSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,FCSCondSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSCond Sources-11.png)<!-- -->


### FCS computation


```r
#calculate FCS
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(FCS = (2*FCSStap) + (3 * FCSPulse)+ (4*FCSPr) + FCSVeg  + FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_baseline_2018$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_baseline_2018$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_baseline_2018$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-1.png)<!-- -->

```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-2.png)<!-- -->

```r
#############################
#calculate FCS
# Burkina_pdm_2019 <- Burkina_pdm_2019 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSDairy)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
# var_label(Burkina_pdm_2019$FCS) <- "Score de consommation alimentaire"
# #create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
# Burkina_pdm_2019 <- Burkina_pdm_2019 %>% mutate(
#   FCSCat21 = case_when(
#     FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
#   FCSCat28 = case_when(
#     FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
# var_label(Burkina_pdm_2019$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
# var_label(Burkina_pdm_2019$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"
# 
# Burkina_pdm_2019 %>% 
#   sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
# Burkina_pdm_2019 %>% 
#   sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)

#######################################
#calculate FCS
Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSPulse)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_ea_2019$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_ea_2019$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_ea_2019$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-3.png)<!-- -->

```r
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-4.png)<!-- -->

```r
#############################################
#calculate FCS
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSPulse)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_ea_2020$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_ea_2020$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_ea_2020$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_ea_2020 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-5.png)<!-- -->

```r
Burkina_ea_2020 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-6.png)<!-- -->

```r
########################################
#calculate FCS
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSPulse)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_ea_2021$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_ea_2021$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_ea_2021$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-7.png)<!-- -->

```r
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-8.png)<!-- -->

```r
###########################################
Burkina_pdm_2021$FCSPr <- as_numeric(Burkina_pdm_2021$FCSPr)
#calculate FCS
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSPulse)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_pdm_2021$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_pdm_2021$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_pdm_2021$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-9.png)<!-- -->

```r
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-10.png)<!-- -->

```r
#############################################
#calculate FCS
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(FCS = (2 * FCSStap) + (3 * FCSPulse)+ (4*FCSPr) +FCSVeg  +FCSFruit +(4*FCSDairy) + (0.5*FCSFat) + (0.5*FCSSugar))
var_label(Burkina_ea_2022$FCS) <- "Score de consommation alimentaire"
#create FCG groups based on 21/25 or 28/42 thresholds - analyst should decide which one to use.
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(
  FCSCat21 = case_when(
    FCS <= 21 ~ "Pauvre", between(FCS, 21.5, 35) ~ "Limite", FCS > 35 ~ "Acceptable"),
  FCSCat28 = case_when(
    FCS <= 28 ~ "Pauvre", between(FCS, 28.5, 42) ~ "Limite", FCS > 42 ~ "Acceptable"))
var_label(Burkina_ea_2022$FCSCat21) <- "Groupe de consommation alimentaire - Seuils du 21/35"
var_label(Burkina_ea_2022$FCSCat28) <-  "Groupe de consommation alimentaire - Seuils du 28/42"

Burkina_ea_2022 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat21,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-11.png)<!-- -->

```r
Burkina_ea_2022 %>% 
  sjPlot::plot_frq(coord.flip =T,FCSCat28,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCS-12.png)<!-- -->


## reduced coping strategy index OU l’indice réduit des stratégies de survie (rCSI)

### rCSI : Consommer des aliments moins préférés et moins chers


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty-6.png)<!-- -->

### FCS : Consommer des aliments moins préférés et moins chers  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(rCSILessQlty = recode(rCSILessQlty,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$rCSILessQlty <- replace(Burkina_baseline_2018$rCSILessQlty, is.na(Burkina_baseline_2018$rCSILessQlty), 0)

Burkina_baseline_2018$rCSILessQlty <- as.numeric(Burkina_baseline_2018$rCSILessQlty)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(rCSILessQlty = recode(rCSILessQlty,
                          "5" = 5,
                          "7" = 7,
                          .default = 0))
Burkina_ea_2019$rCSILessQlty <- replace(Burkina_ea_2019$rCSILessQlty, is.na(Burkina_ea_2019$rCSILessQlty), 0)

Burkina_ea_2019$rCSILessQlty <- as.numeric(Burkina_ea_2019$rCSILessQlty)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$rCSILessQlty <- replace(Burkina_ea_2020$rCSILessQlty, is.na(Burkina_ea_2020$rCSILessQlty), 0)
Burkina_ea_2020$rCSILessQlty <- as.numeric(Burkina_ea_2020$rCSILessQlty)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021$rCSILessQlty <- replace(Burkina_ea_2021$rCSILessQlty, is.na(Burkina_ea_2021$rCSILessQlty), 0)
Burkina_ea_2021$rCSILessQlty <- as.numeric(Burkina_ea_2021$rCSILessQlty)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$rCSILessQlty <- replace(Burkina_ea_2022$rCSILessQlty, is.na(Burkina_ea_2022$rCSILessQlty), 0)
Burkina_ea_2022$rCSILessQlty <- as.numeric(Burkina_ea_2022$rCSILessQlty)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$rCSILessQlty <- replace(Burkina_pdm_2021$rCSILessQlty, is.na(Burkina_pdm_2021$rCSILessQlty), 0)
Burkina_pdm_2021$rCSILessQlty <-
  as.numeric(Burkina_pdm_2021$rCSILessQlty)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,rCSILessQlty,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSILessQlty  Nombre de jours ref-6.png)<!-- -->


### rCSI : Emprunter de la nourriture ou compter sur l’aide des parents/amis



```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow-6.png)<!-- -->


### FCS : Emprunter de la nourriture ou compter sur l’aide des parents/amis  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(rCSIBorrow = recode(rCSIBorrow,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$rCSIBorrow <- replace(Burkina_baseline_2018$rCSIBorrow, is.na(Burkina_baseline_2018$rCSIBorrow), 0)

Burkina_baseline_2018$rCSIBorrow <- as.numeric(Burkina_baseline_2018$rCSIBorrow)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(rCSIBorrow = recode(rCSIBorrow,
                          "5" = 5,
                          "3" = 3,
                          "0" = 0,
                          .default = 0))
Burkina_ea_2019$rCSIBorrow <- replace(Burkina_ea_2019$rCSIBorrow, is.na(Burkina_ea_2019$rCSIBorrow), 0)

Burkina_ea_2019$rCSIBorrow <- as.numeric(Burkina_ea_2019$rCSIBorrow)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$rCSIBorrow <- replace(Burkina_ea_2020$rCSIBorrow, is.na(Burkina_ea_2020$rCSIBorrow), 0)
Burkina_ea_2020$rCSIBorrow <- as.numeric(Burkina_ea_2020$rCSIBorrow)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(rCSIBorrow = recode(rCSIBorrow,
                           "0" = 0,
                           "1" = 1,
                           "2" = 2,
                           "3" = 3,
                           "4" = 4,
                           "5" = 5,
                           "6" = 6,
                           "7" = 7,
                          .default = 0))
Burkina_ea_2021$rCSIBorrow <- replace(Burkina_ea_2021$rCSIBorrow, is.na(Burkina_ea_2021$rCSIBorrow), 0)
Burkina_ea_2021$rCSIBorrow <- as.numeric(Burkina_ea_2021$rCSIBorrow)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$rCSIBorrow <- replace(Burkina_ea_2022$rCSIBorrow, is.na(Burkina_ea_2022$rCSIBorrow), 0)
Burkina_ea_2022$rCSIBorrow <- as.numeric(Burkina_ea_2022$rCSIBorrow)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$rCSIBorrow <- replace(Burkina_pdm_2021$rCSIBorrow, is.na(Burkina_pdm_2021$rCSIBorrow), 0)
Burkina_pdm_2021$rCSIBorrow <- as.numeric(Burkina_pdm_2021$rCSIBorrow)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,rCSIBorrow,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIBorrow  Nombre de jours ref-6.png)<!-- -->


### rCSI : Diminuer la quantité consommée pendant les repas


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize-6.png)<!-- -->


### FCS : Diminuer la quantité consommée pendant les repas  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(rCSIMealSize = recode(rCSIMealSize,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$rCSIMealSize <- replace(Burkina_baseline_2018$rCSIMealSize, is.na(Burkina_baseline_2018$rCSIMealSize), 0)

Burkina_baseline_2018$rCSIMealSize <- as.numeric(Burkina_baseline_2018$rCSIMealSize)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(rCSIMealSize = recode(rCSIMealSize,
                          "7" = 7,
                          "0" = 0,
                          .default = 0))
Burkina_ea_2019$rCSIMealSize <- replace(Burkina_ea_2019$rCSIMealSize, is.na(Burkina_ea_2019$rCSIMealSize), 0)

Burkina_ea_2019$rCSIMealSize <- as.numeric(Burkina_ea_2019$rCSIMealSize)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$rCSIMealSize <- replace(Burkina_ea_2020$rCSIMealSize, is.na(Burkina_ea_2020$rCSIMealSize), 0)
Burkina_ea_2020$rCSIMealSize <- as.numeric(Burkina_ea_2020$rCSIMealSize)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(rCSIMealSize = recode(rCSIMealSize,
                           "0" = 0,
                           "1" = 1,
                           "2" = 2,
                           "3" = 3,
                           "4" = 4,
                           "5" = 5,
                           "6" = 6,
                           "7" = 7,
                          .default = 0))
Burkina_ea_2021$rCSIMealSize <- replace(Burkina_ea_2021$rCSIMealSize, is.na(Burkina_ea_2021$rCSIMealSize), 0)
Burkina_ea_2021$rCSIMealSize <- as.numeric(Burkina_ea_2021$rCSIMealSize)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$rCSIMealSize <- replace(Burkina_ea_2022$rCSIMealSize, is.na(Burkina_ea_2022$rCSIMealSize), 0)
Burkina_ea_2022$rCSIMealSize <- as.numeric(Burkina_ea_2022$rCSIMealSize)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$rCSIMealSize <- replace(Burkina_pdm_2021$rCSIMealSize, is.na(Burkina_pdm_2021$rCSIMealSize), 0)
Burkina_pdm_2021$rCSIMealSize <- as.numeric(Burkina_pdm_2021$rCSIMealSize)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealSize,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealSize  Nombre de jours ref-6.png)<!-- -->

### rCSI :  Restreindre la consommation des adultes  pour nourrir les enfants


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-4.png)<!-- -->

```r
Burkina_pdm_2021%>%
sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult-6.png)<!-- -->


### FCS : Restreindre la consommation des adultes  pour nourrir les enfants  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(rCSIMealAdult = recode(rCSIMealAdult,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$rCSIMealAdult <- replace(Burkina_baseline_2018$rCSIMealAdult, is.na(Burkina_baseline_2018$rCSIMealAdult), 0)

Burkina_baseline_2018$rCSIMealAdult <- as.numeric(Burkina_baseline_2018$rCSIMealAdult)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(rCSIMealAdult = recode(rCSIMealAdult,
                          "7" = 7,
                          "0" = 0,
                          .default = 0))
Burkina_ea_2019$rCSIMealAdult <- replace(Burkina_ea_2019$rCSIMealAdult, is.na(Burkina_ea_2019$rCSIMealAdult), 0)

Burkina_ea_2019$rCSIMealAdult <- as.numeric(Burkina_ea_2019$rCSIMealAdult)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$rCSIMealAdult <- replace(Burkina_ea_2020$rCSIMealAdult, is.na(Burkina_ea_2020$rCSIMealAdult), 0)
Burkina_ea_2020$rCSIMealAdult <- as.numeric(Burkina_ea_2020$rCSIMealAdult)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(rCSIMealAdult = recode(rCSIMealAdult,
                           "0" = 0,
                           "1" = 1,
                           "2" = 2,
                           "3" = 3,
                           "4" = 4,
                           "5" = 5,
                           "6" = 6,
                           "7" = 7,
                          .default = 0))
Burkina_ea_2021$rCSIMealAdult <- replace(Burkina_ea_2021$rCSIMealAdult, is.na(Burkina_ea_2021$rCSIMealAdult), 0)
Burkina_ea_2021$rCSIMealAdult <- as.numeric(Burkina_ea_2021$rCSIMealAdult)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$rCSIMealAdult <- replace(Burkina_ea_2022$rCSIMealAdult, is.na(Burkina_ea_2022$rCSIMealAdult), 0)
Burkina_ea_2022$rCSIMealAdult <- as.numeric(Burkina_ea_2022$rCSIMealAdult)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$rCSIMealAdult <- replace(Burkina_pdm_2021$rCSIMealAdult, is.na(Burkina_pdm_2021$rCSIMealAdult), 0)
Burkina_pdm_2021$rCSIMealAdult <- as.numeric(Burkina_pdm_2021$rCSIMealAdult)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealAdult,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealAdult  Nombre de jours ref-6.png)<!-- -->


### rCSI : Diminuer le nombre de repas par jour


```r
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-1.png)<!-- -->

```r
#Burkina_pdm_2019%>% 
  #sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
Burkina_ea_2019%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-2.png)<!-- -->

```r
Burkina_ea_2020%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-3.png)<!-- -->

```r
Burkina_ea_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-4.png)<!-- -->

```r
Burkina_pdm_2021%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-5.png)<!-- -->

```r
Burkina_ea_2022%>% 
  sjPlot::plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb-6.png)<!-- -->


### FCS : Diminuer le nombre de repas par jour  - Nombre de jours


```r
##### Burkina_baseline_2018
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(rCSIMealNb = recode(rCSIMealNb,
                          "0" = 0,
                          "1" = 1,
                          "2" = 2,
                          "3" = 3,
                          "4" = 4,
                          "5" = 5,
                          "6" = 6,
                          "7" = 7,
                          .default = 0))
Burkina_baseline_2018$rCSIMealNb <- replace(Burkina_baseline_2018$rCSIMealNb, is.na(Burkina_baseline_2018$rCSIMealNb), 0)

Burkina_baseline_2018$rCSIMealNb <- as.numeric(Burkina_baseline_2018$rCSIMealNb)
#Plot
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-1.png)<!-- -->

```r
##### Burkina_ea_2019

Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(rCSIMealNb = recode(rCSIMealNb,
                          "5" = 5,
                          "0" = 0,
                          .default = 0))
Burkina_ea_2019$rCSIMealNb <- replace(Burkina_ea_2019$rCSIMealNb, is.na(Burkina_ea_2019$rCSIMealNb), 0)

Burkina_ea_2019$rCSIMealNb <- as.numeric(Burkina_ea_2019$rCSIMealNb)

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-2.png)<!-- -->

```r
##### Burkina_ea_2020
Burkina_ea_2020$rCSIMealNb <- replace(Burkina_ea_2020$rCSIMealNb, is.na(Burkina_ea_2020$rCSIMealNb), 0)
Burkina_ea_2020$rCSIMealNb <- as.numeric(Burkina_ea_2020$rCSIMealNb)

Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-3.png)<!-- -->

```r
##### Burkina_ea_2021
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(rCSIMealNb = recode(rCSIMealNb,
                           "0" = 0,
                           "1" = 1,
                           "2" = 2,
                           "3" = 3,
                           "4" = 4,
                           "5" = 5,
                           "6" = 6,
                           "7" = 7,
                          .default = 0))
Burkina_ea_2021$rCSIMealNb <- replace(Burkina_ea_2021$rCSIMealNb, is.na(Burkina_ea_2021$rCSIMealNb), 0)
Burkina_ea_2021$rCSIMealNb <- as.numeric(Burkina_ea_2021$rCSIMealNb)
#Plot
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-4.png)<!-- -->

```r
##### Burkina_ea_2022
Burkina_ea_2022$rCSIMealNb <- replace(Burkina_ea_2022$rCSIMealNb, is.na(Burkina_ea_2022$rCSIMealNb), 0)
Burkina_ea_2022$rCSIMealNb <- as.numeric(Burkina_ea_2022$rCSIMealNb)
#Plot
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-5.png)<!-- -->

```r
##### Burkina_pdm_2021
Burkina_pdm_2021$rCSIMealNb <- replace(Burkina_pdm_2021$rCSIMealNb, is.na(Burkina_pdm_2021$rCSIMealNb), 0)
Burkina_pdm_2021$rCSIMealNb <- as.numeric(Burkina_pdm_2021$rCSIMealNb)

Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,rCSIMealNb,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rCSIMealNb  Nombre de jours ref-6.png)<!-- -->



```r
#calculate rCSI Score
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_baseline_2018$rCSI) <- "rCSI"
#calculate rCSI Score
# Burkina_pdm_2019 <- Burkina_pdm_2019 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
# var_label(Burkina_pdm_2019$rCSI) <- "rCSI"
#calculate rCSI Score
Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_ea_2019$rCSI) <- "rCSI"
#calculate rCSI Score
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_ea_2020$rCSI) <- "rCSI"
#calculate rCSI Score
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_ea_2021$rCSI) <- "rCSI"
#calculate rCSI Score
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_pdm_2021$rCSI) <- "rCSI"
#calculate rCSI Score
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(rCSI = rCSILessQlty  + (2 * rCSIBorrow) + rCSIMealSize + (3 * rCSIMealAdult) + rCSIMealNb)
var_label(Burkina_ea_2022$rCSI) <- "rCSI"
```


Households are divided in four classes according to the rCSI score: 0-3, 4-18, and 19 and above which correspond to IPC Phases 1, 2 and 3 and above respectively.


```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3", 
    between(rCSI, 0, 3) ~ "Phase 1",
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_baseline_2018$rcsi_class) <- "Phases de l'IPC"
Burkina_baseline_2018 %>% 
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-1.png)<!-- -->

```r
# Burkina_pdm_2019 <- Burkina_pdm_2019 %>% mutate(
#   rcsi_class = case_when(
#     rCSI <= 19 ~ 3, between(rCSI, 0, 3) ~ 1, between(rCSI, 4, 18) ~ 2, rCSI > 19 ~ "above"))
# var_label(Burkina_pdm_2019$rcsi_class) <- "Phases de l'IPC"
# Burkina_pdm_2019 %>% 
#   sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)

Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3",
    between(rCSI, 0, 3) ~ "Phase 1",
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_ea_2019$rcsi_class) <- "Phases de l'IPC"
Burkina_ea_2019 %>% 
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-2.png)<!-- -->

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3", 
    between(rCSI, 0, 3) ~ "Phase 1",
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_ea_2020$rcsi_class) <- "Phases de l'IPC"
Burkina_ea_2020 %>% 
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-3.png)<!-- -->

```r
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3", 
    between(rCSI, 0, 3) ~ "Phase 1",
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_ea_2021$rcsi_class) <- "Phases de l'IPC"
Burkina_ea_2021 %>% 
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-4.png)<!-- -->

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3",
    between(rCSI, 0, 3) ~ "Phase 1", 
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_pdm_2021$rcsi_class) <- "Phases de l'IPC"
Burkina_pdm_2021 %>%
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-5.png)<!-- -->

```r
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(
  rcsi_class = case_when(
    rCSI >= 19 ~ "Phase 3", 
    between(rCSI, 0, 3) ~ "Phase 1", 
    between(rCSI, 4, 18) ~ "Phase 2"))
var_label(Burkina_ea_2022$rcsi_class) <- "Phases de l'IPC"
Burkina_ea_2022 %>% 
  sjPlot::plot_frq(coord.flip =T,rcsi_class,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/rcsi_class-6.png)<!-- -->


## Stratégies d'adaptation aux moyens d'existence (LhCSI)


```r
# 1 = Non, je n'ai pas été confronté à une insuffisance de nourriture
# 2 = Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire
# 3 = Oui
# 4 = Non applicable
```


### LhCSI : Vendre des actifs/biens non productifs du ménage (radio, meuble, réfrigérateur, télévision, bijoux etc.)


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIStress1)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIStress1 <- as.character(Burkina_baseline_2018$LhCSIStress1)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSIStress1 = dplyr::case_when(
      LhCSIStress1 == "0" ~ NA,
      .default = as.factor(LhCSIStress1)
    ) %>% structure(label = label(LhCSIStress1)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIStress1 = case_when(
    LhCSIStress1 == "1" ~ 1,
    LhCSIStress1 == "2" ~ 2,
    is.na(LhCSIStress1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSIStress1 <- labelled::labelled(Burkina_baseline_2018$LhCSIStress1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIStress1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIStress1)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIStress1 <- as.character(Burkina_ea_2019$LhCSIStress1)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSIStress1 = dplyr::case_when(
      LhCSIStress1 == "0" ~ NA,
      .default = as.factor(LhCSIStress1)
    ) %>% structure(label = label(LhCSIStress1)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIStress1 = case_when(
    LhCSIStress1 == "1" ~ 1,
    LhCSIStress1 == "2" ~ 2,
    is.na(LhCSIStress1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIStress1 <- labelled::labelled(Burkina_ea_2019$LhCSIStress1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIStress1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIStress1)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIStress1 <- as.character(Burkina_ea_2020$LhCSIStress1)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSIStress1 = dplyr::case_when(
      LhCSIStress1 == "0" ~ NA,
      .default = as.factor(LhCSIStress1)
    ) %>% structure(label = label(LhCSIStress1)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIStress1 = case_when(
    LhCSIStress1 == "1" ~ 1,
    LhCSIStress1 == "2" ~ 2,
    LhCSIStress1 == "3" ~ 4,
    is.na(LhCSIStress1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIStress1 <- labelled::labelled(Burkina_ea_2020$LhCSIStress1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIStress1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress1)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIStress1 = dplyr::recode(LhCSIStress1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIStress1 <- labelled::labelled(Burkina_ea_2021$LhCSIStress1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress1)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIStress1 = dplyr::recode(LhCSIStress1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIStress1 <- labelled::labelled(Burkina_ea_2022$LhCSIStress1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIStress1)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIStress1 <- as.character(Burkina_pdm_2021$LhCSIStress1)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIStress1 = dplyr::case_when(
      LhCSIStress1 == "0" ~ NA,
      .default = as.factor(LhCSIStress1)
    ) %>% structure(label = label(LhCSIStress1)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIStress1 = case_when(
    LhCSIStress1 == "1" ~ 1,
    LhCSIStress1 == "2" ~ 2,
    LhCSIStress1 == "3" ~ 4,
    is.na(LhCSIStress1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIStress1 <- labelled::labelled(Burkina_pdm_2021$LhCSIStress1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIStress1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress1-12.png)<!-- -->


### LhCSI : Vendre plus d’animaux (non-productifs) que d’habitude


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIStress2)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIStress2 <- as.character(Burkina_baseline_2018$LhCSIStress2)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSIStress2 = dplyr::case_when(
      LhCSIStress2 == "0" ~ NA,
      .default = as.factor(LhCSIStress2)
    ) %>% structure(label = label(LhCSIStress2)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIStress2 = case_when(
    LhCSIStress2 == "1" ~ 1,
    LhCSIStress2 == "2" ~ 2,
    is.na(LhCSIStress2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSIStress2 <- labelled::labelled(Burkina_baseline_2018$LhCSIStress2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIStress2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIStress2)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIStress2 <- as.character(Burkina_ea_2019$LhCSIStress2)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSIStress2 = dplyr::case_when(
      LhCSIStress2 == "0" ~ NA,
      .default = as.factor(LhCSIStress2)
    ) %>% structure(label = label(LhCSIStress2)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIStress2 = case_when(
    LhCSIStress2 == "1" ~ 1,
    LhCSIStress2 == "2" ~ 2,
    is.na(LhCSIStress2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIStress2 <- labelled::labelled(Burkina_ea_2019$LhCSIStress2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIStress2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIStress2)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIStress2 <- as.character(Burkina_ea_2020$LhCSIStress2)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSIStress2 = dplyr::case_when(
      LhCSIStress2 == "0" ~ NA,
      .default = as.factor(LhCSIStress2)
    ) %>% structure(label = label(LhCSIStress2)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIStress2 = case_when(
    LhCSIStress2 == "1" ~ 1,
    LhCSIStress2 == "2" ~ 2,
    LhCSIStress2 == "3" ~ 4,
    is.na(LhCSIStress2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIStress2 <- labelled::labelled(Burkina_ea_2020$LhCSIStress2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIStress2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress2)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIStress2 = dplyr::recode(LhCSIStress2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIStress2 <- labelled::labelled(Burkina_ea_2021$LhCSIStress2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress2)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIStress2 = dplyr::recode(LhCSIStress2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIStress2 <- labelled::labelled(Burkina_ea_2022$LhCSIStress2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIStress2)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIStress2 <- as.character(Burkina_pdm_2021$LhCSIStress2)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIStress2 = dplyr::case_when(
      LhCSIStress2 == "0" ~ NA,
      .default = as.factor(LhCSIStress2)
    ) %>% structure(label = label(LhCSIStress2)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIStress2 = case_when(
    LhCSIStress2 == "1" ~ 1,
    LhCSIStress2 == "2" ~ 2,
    LhCSIStress2 == "3" ~ 4,
    is.na(LhCSIStress2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIStress2 <- labelled::labelled(Burkina_pdm_2021$LhCSIStress2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIStress2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress2-12.png)<!-- -->


### LhCSI : Dépenser l’épargne en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIStress3)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIStress3 <- as.character(Burkina_baseline_2018$LhCSIStress3)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSIStress3 = dplyr::case_when(
      LhCSIStress3 == "0" ~ NA,
      .default = as.factor(LhCSIStress3)
    ) %>% structure(label = label(LhCSIStress3)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIStress3 = case_when(
    LhCSIStress3 == "1" ~ 1,
    LhCSIStress3 == "2" ~ 2,
    is.na(LhCSIStress3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSIStress3 <- labelled::labelled(Burkina_baseline_2018$LhCSIStress3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIStress3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIStress3)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIStress3 <- as.character(Burkina_ea_2019$LhCSIStress3)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSIStress3 = dplyr::case_when(
      LhCSIStress3 == "0" ~ NA,
      .default = as.factor(LhCSIStress3)
    ) %>% structure(label = label(LhCSIStress3)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIStress3 = case_when(
    LhCSIStress3 == "1" ~ 1,
    LhCSIStress3 == "2" ~ 2,
    is.na(LhCSIStress3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIStress3 <- labelled::labelled(Burkina_ea_2019$LhCSIStress3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIStress3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIStress3)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIStress3 <- as.character(Burkina_ea_2020$LhCSIStress3)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSIStress3 = dplyr::case_when(
      LhCSIStress3 == "0" ~ NA,
      .default = as.factor(LhCSIStress3)
    ) %>% structure(label = label(LhCSIStress3)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIStress3 = case_when(
    LhCSIStress3 == "1" ~ 1,
    LhCSIStress3 == "2" ~ 2,
    LhCSIStress3 == "3" ~ 4,
    is.na(LhCSIStress3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIStress3 <- labelled::labelled(Burkina_ea_2020$LhCSIStress3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIStress3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress3)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIStress3 = dplyr::recode(LhCSIStress3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIStress3 <- labelled::labelled(Burkina_ea_2021$LhCSIStress3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress3)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIStress3 = dplyr::recode(LhCSIStress3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIStress3 <- labelled::labelled(Burkina_ea_2022$LhCSIStress3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIStress3)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIStress3 <- as.character(Burkina_pdm_2021$LhCSIStress3)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIStress3 = dplyr::case_when(
      LhCSIStress3 == "0" ~ NA,
      .default = as.factor(LhCSIStress3)
    ) %>% structure(label = label(LhCSIStress3)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIStress3 = case_when(
    LhCSIStress3 == "1" ~ 1,
    LhCSIStress3 == "2" ~ 2,
    LhCSIStress3 == "3" ~ 4,
    is.na(LhCSIStress3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIStress3 <- labelled::labelled(Burkina_pdm_2021$LhCSIStress3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIStress3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress3-12.png)<!-- -->


### LhCSI : Emprunter de l’argent / nourriture auprès d’un prêteur formel /banque


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIStress4)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIStress4 <- as.character(Burkina_baseline_2018$LhCSIStress4)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSIStress4 = dplyr::case_when(
      LhCSIStress4 == "0" ~ NA,
      .default = as.factor(LhCSIStress4)
    ) %>% structure(label = label(LhCSIStress4)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIStress4 = case_when(
    LhCSIStress4 == "1" ~ 1,
    LhCSIStress4 == "2" ~ 2,
    is.na(LhCSIStress4) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSIStress4 <- labelled::labelled(Burkina_baseline_2018$LhCSIStress4, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIStress4)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIStress4)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIStress4 <- as.character(Burkina_ea_2019$LhCSIStress4)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSIStress4 = dplyr::case_when(
      LhCSIStress4 == "0" ~ NA,
      .default = as.factor(LhCSIStress4)
    ) %>% structure(label = label(LhCSIStress4)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIStress4 = case_when(
    LhCSIStress4 == "1" ~ 1,
    LhCSIStress4 == "2" ~ 2,
    is.na(LhCSIStress4) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIStress4 <- labelled::labelled(Burkina_ea_2019$LhCSIStress4, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIStress4)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIStress4)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIStress4 <- as.character(Burkina_ea_2020$LhCSIStress4)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSIStress4 = dplyr::case_when(
      LhCSIStress4 == "0" ~ NA,
      .default = as.factor(LhCSIStress4)
    ) %>% structure(label = label(LhCSIStress4)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIStress4 = case_when(
    LhCSIStress4 == "1" ~ 1,
    LhCSIStress4 == "2" ~ 2,
    LhCSIStress4 == "3" ~ 4,
    is.na(LhCSIStress4) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIStress4 <- labelled::labelled(Burkina_ea_2020$LhCSIStress4, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIStress4)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress4)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress4)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIStress4 = dplyr::recode(LhCSIStress4,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIStress4 <- labelled::labelled(Burkina_ea_2021$LhCSIStress4, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIStress4)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress4)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress4)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress4)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIStress4 = dplyr::recode(LhCSIStress4,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIStress4 <- labelled::labelled(Burkina_ea_2022$LhCSIStress4, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIStress4)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIStress4)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIStress4)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIStress4 <- as.character(Burkina_pdm_2021$LhCSIStress4)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIStress4 = dplyr::case_when(
      LhCSIStress4 == "0" ~ NA,
      .default = as.factor(LhCSIStress4)
    ) %>% structure(label = label(LhCSIStress4)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIStress4 = case_when(
    LhCSIStress4 == "1" ~ 1,
    LhCSIStress4 == "2" ~ 2,
    LhCSIStress4 == "3" ~ 4,
    is.na(LhCSIStress4) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIStress4 <- labelled::labelled(Burkina_pdm_2021$LhCSIStress4, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIStress4)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIStress4, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIStress4-12.png)<!-- -->



### LhCSI : Réduire les dépenses non alimentaires essentielles telles que l’éducation, la santé (dont de médicaments)


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSICrisis1)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSICrisis1 <- as.character(Burkina_baseline_2018$LhCSICrisis1)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSICrisis1 = dplyr::case_when(
      LhCSICrisis1 == "0" ~ NA,
      .default = as.factor(LhCSICrisis1)
    ) %>% structure(label = label(LhCSICrisis1)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSICrisis1 = case_when(
    LhCSICrisis1 == "1" ~ 1,
    LhCSICrisis1 == "2" ~ 2,
    is.na(LhCSICrisis1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSICrisis1 <- labelled::labelled(Burkina_baseline_2018$LhCSICrisis1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSICrisis1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSICrisis1)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSICrisis1 <- as.character(Burkina_ea_2019$LhCSICrisis1)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSICrisis1 = dplyr::case_when(
      LhCSICrisis1 == "0" ~ NA,
      .default = as.factor(LhCSICrisis1)
    ) %>% structure(label = label(LhCSICrisis1)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSICrisis1 = case_when(
    LhCSICrisis1 == "1" ~ 1,
    LhCSICrisis1 == "2" ~ 2,
    is.na(LhCSICrisis1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSICrisis1 <- labelled::labelled(Burkina_ea_2019$LhCSICrisis1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSICrisis1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSICrisis1)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSICrisis1 <- as.character(Burkina_ea_2020$LhCSICrisis1)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSICrisis1 = dplyr::case_when(
      LhCSICrisis1 == "0" ~ NA,
      .default = as.factor(LhCSICrisis1)
    ) %>% structure(label = label(LhCSICrisis1)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSICrisis1 = case_when(
    LhCSICrisis1 == "1" ~ 1,
    LhCSICrisis1 == "2" ~ 2,
    LhCSICrisis1 == "3" ~ 4,
    is.na(LhCSICrisis1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSICrisis1 <- labelled::labelled(Burkina_ea_2020$LhCSICrisis1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSICrisis1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis1)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSICrisis1 = dplyr::recode(LhCSICrisis1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSICrisis1 <- labelled::labelled(Burkina_ea_2021$LhCSICrisis1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis1)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSICrisis1 = dplyr::recode(LhCSICrisis1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSICrisis1 <- labelled::labelled(Burkina_ea_2022$LhCSICrisis1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSICrisis1)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSICrisis1 <- as.character(Burkina_pdm_2021$LhCSICrisis1)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSICrisis1 = dplyr::case_when(
      LhCSICrisis1 == "0" ~ NA,
      .default = as.factor(LhCSICrisis1)
    ) %>% structure(label = label(LhCSICrisis1)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSICrisis1 = case_when(
    LhCSICrisis1 == "1" ~ 1,
    LhCSICrisis1 == "2" ~ 2,
    LhCSICrisis1 == "3" ~ 4,
    is.na(LhCSICrisis1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSICrisis1 <- labelled::labelled(Burkina_pdm_2021$LhCSICrisis1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSICrisis1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis1-12.png)<!-- -->

### LhCSI : Vendre des biens productifs ou des moyens de transport (machine à coudre, brouette, vélo, car, etc.)


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSICrisis2)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSICrisis2 <- as.character(Burkina_baseline_2018$LhCSICrisis2)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSICrisis2 = dplyr::case_when(
      LhCSICrisis2 == "0" ~ NA,
      .default = as.factor(LhCSICrisis2)
    ) %>% structure(label = label(LhCSICrisis2)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSICrisis2 = case_when(
    LhCSICrisis2 == "1" ~ 1,
    LhCSICrisis2 == "2" ~ 2,
    is.na(LhCSICrisis2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSICrisis2 <- labelled::labelled(Burkina_baseline_2018$LhCSICrisis2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSICrisis2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSICrisis2)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSICrisis2 <- as.character(Burkina_ea_2019$LhCSICrisis2)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSICrisis2 = dplyr::case_when(
      LhCSICrisis2 == "0" ~ NA,
      .default = as.factor(LhCSICrisis2)
    ) %>% structure(label = label(LhCSICrisis2)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSICrisis2 = case_when(
    LhCSICrisis2 == "1" ~ 1,
    LhCSICrisis2 == "2" ~ 2,
    is.na(LhCSICrisis2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSICrisis2 <- labelled::labelled(Burkina_ea_2019$LhCSICrisis2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSICrisis2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSICrisis2)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSICrisis2 <- as.character(Burkina_ea_2020$LhCSICrisis2)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSICrisis2 = dplyr::case_when(
      LhCSICrisis2 == "0" ~ NA,
      .default = as.factor(LhCSICrisis2)
    ) %>% structure(label = label(LhCSICrisis2)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSICrisis2 = case_when(
    LhCSICrisis2 == "1" ~ 1,
    LhCSICrisis2 == "2" ~ 2,
    LhCSICrisis2 == "3" ~ 4,
    is.na(LhCSICrisis2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSICrisis2 <- labelled::labelled(Burkina_ea_2020$LhCSICrisis2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSICrisis2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis2)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSICrisis2 = dplyr::recode(LhCSICrisis2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSICrisis2 <- labelled::labelled(Burkina_ea_2021$LhCSICrisis2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis2)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSICrisis2 = dplyr::recode(LhCSICrisis2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSICrisis2 <- labelled::labelled(Burkina_ea_2022$LhCSICrisis2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSICrisis2)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSICrisis2 <- as.character(Burkina_pdm_2021$LhCSICrisis2)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSICrisis2 = dplyr::case_when(
      LhCSICrisis2 == "0" ~ NA,
      .default = as.factor(LhCSICrisis2)
    ) %>% structure(label = label(LhCSICrisis2)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSICrisis2 = case_when(
    LhCSICrisis2 == "1" ~ 1,
    LhCSICrisis2 == "2" ~ 2,
    LhCSICrisis2 == "3" ~ 4,
    is.na(LhCSICrisis2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSICrisis2 <- labelled::labelled(Burkina_pdm_2021$LhCSICrisis2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSICrisis2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis2-12.png)<!-- -->

### LhCSI : Retirer les enfants de l’école


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSICrisis3)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSICrisis3 <- as.character(Burkina_baseline_2018$LhCSICrisis3)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>%
  dplyr::mutate(
    LhCSICrisis3 = dplyr::case_when(
      LhCSICrisis3 == "0" ~ NA,
      .default = as.factor(LhCSICrisis3)
    ) %>% structure(label = label(LhCSICrisis3)))
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSICrisis3 = case_when(
    LhCSICrisis3 == "1" ~ 1,
    LhCSICrisis3 == "2" ~ 2,
    is.na(LhCSICrisis3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_baseline_2018$LhCSICrisis3 <- labelled::labelled(Burkina_baseline_2018$LhCSICrisis3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSICrisis3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSICrisis3)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSICrisis3 <- as.character(Burkina_ea_2019$LhCSICrisis3)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>%
  dplyr::mutate(
    LhCSICrisis3 = dplyr::case_when(
      LhCSICrisis3 == "0" ~ NA,
      .default = as.factor(LhCSICrisis3)
    ) %>% structure(label = label(LhCSICrisis3)))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSICrisis3 = case_when(
    LhCSICrisis3 == "1" ~ 1,
    LhCSICrisis3 == "2" ~ 2,
    is.na(LhCSICrisis3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSICrisis3 <- labelled::labelled(Burkina_ea_2019$LhCSICrisis3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSICrisis3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSICrisis3)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSICrisis3 <- as.character(Burkina_ea_2020$LhCSICrisis3)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>%
  dplyr::mutate(
    LhCSICrisis3 = dplyr::case_when(
      LhCSICrisis3 == "0" ~ NA,
      .default = as.factor(LhCSICrisis3)
    ) %>% structure(label = label(LhCSICrisis3)))
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSICrisis3 = case_when(
    LhCSICrisis3 == "1" ~ 1,
    LhCSICrisis3 == "2" ~ 2,
    LhCSICrisis3 == "3" ~ 4,
    is.na(LhCSICrisis3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSICrisis3 <- labelled::labelled(Burkina_ea_2020$LhCSICrisis3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSICrisis3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis3)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSICrisis3 = dplyr::recode(LhCSICrisis3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSICrisis3 <- labelled::labelled(Burkina_ea_2021$LhCSICrisis3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSICrisis3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis3)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSICrisis3 = dplyr::recode(LhCSICrisis3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSICrisis3 <- labelled::labelled(Burkina_ea_2022$LhCSICrisis3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSICrisis3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSICrisis3)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSICrisis3 <- as.character(Burkina_pdm_2021$LhCSICrisis3)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSICrisis3 = dplyr::case_when(
      LhCSICrisis3 == "0" ~ NA,
      .default = as.factor(LhCSICrisis3)
    ) %>% structure(label = label(LhCSICrisis3)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSICrisis3 = case_when(
    LhCSICrisis3 == "1" ~ 1,
    LhCSICrisis3 == "2" ~ 2,
    LhCSICrisis3 == "3" ~ 4,
    is.na(LhCSICrisis3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSICrisis3 <- labelled::labelled(Burkina_pdm_2021$LhCSICrisis3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSICrisis3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSICrisis3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSICrisis3-12.png)<!-- -->



### LhCSI : Vendre la maison ou des terrains


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency1)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIEmergency1 <- as.character(Burkina_baseline_2018$LhCSIEmergency1)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIEmergency1 = case_when(
    LhCSIEmergency1 == "1" ~ 1,
    LhCSIEmergency1 == "2" ~ 2,
    is.na(LhCSIEmergency1) ~ 3,
    TRUE ~ 4
  ))

Burkina_baseline_2018$LhCSIEmergency1 <- labelled::labelled(Burkina_baseline_2018$LhCSIEmergency1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIEmergency1)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIEmergency1 <- as.character(Burkina_ea_2019$LhCSIEmergency1)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIEmergency1 = case_when(
    LhCSIEmergency1 == "1" ~ 1,
    LhCSIEmergency1 == "2" ~ 2,
    is.na(LhCSIEmergency1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIEmergency1 <- labelled::labelled(Burkina_ea_2019$LhCSIEmergency1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIEmergency1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIEmergency1)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIEmergency1 <- as.character(Burkina_ea_2020$LhCSIEmergency1)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIEmergency1 = case_when(
    LhCSIEmergency1 == "1" ~ 1,
    LhCSIEmergency1 == "2" ~ 2,
    LhCSIEmergency1 == "3" ~ 4,
    is.na(LhCSIEmergency1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIEmergency1 <- labelled::labelled(Burkina_ea_2020$LhCSIEmergency1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIEmergency1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency1)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIEmergency1 = dplyr::recode(LhCSIEmergency1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIEmergency1 <- labelled::labelled(Burkina_ea_2021$LhCSIEmergency1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency1)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIEmergency1 = dplyr::recode(LhCSIEmergency1,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIEmergency1 <- labelled::labelled(Burkina_ea_2022$LhCSIEmergency1, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency1)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency1)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIEmergency1 <- as.character(Burkina_pdm_2021$LhCSIEmergency1)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIEmergency1 = dplyr::case_when(
      LhCSIEmergency1 == "0" ~ NA,
      .default = as.factor(LhCSIEmergency1)
    ) %>% structure(label = label(LhCSIEmergency1)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIEmergency1 = case_when(
    LhCSIEmergency1 == "1" ~ 1,
    LhCSIEmergency1 == "2" ~ 2,
    LhCSIEmergency1 == "3" ~ 4,
    is.na(LhCSIEmergency1) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIEmergency1 <- labelled::labelled(Burkina_pdm_2021$LhCSIEmergency1, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency1)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency1, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency1-12.png)<!-- -->


### LhCSI : Mendier


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency2)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIEmergency2 <- as.character(Burkina_baseline_2018$LhCSIEmergency2)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIEmergency2 = case_when(
    LhCSIEmergency2 == "1" ~ 1,
    LhCSIEmergency2 == "2" ~ 2,
    is.na(LhCSIEmergency2) ~ 3,
    TRUE ~ 4
  ))

Burkina_baseline_2018$LhCSIEmergency2 <- labelled::labelled(Burkina_baseline_2018$LhCSIEmergency2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIEmergency2)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIEmergency2 <- as.character(Burkina_ea_2019$LhCSIEmergency2)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIEmergency2 = case_when(
    LhCSIEmergency2 == "1" ~ 1,
    LhCSIEmergency2 == "2" ~ 2,
    is.na(LhCSIEmergency2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIEmergency2 <- labelled::labelled(Burkina_ea_2019$LhCSIEmergency2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIEmergency2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIEmergency2)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIEmergency2 <- as.character(Burkina_ea_2020$LhCSIEmergency2)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIEmergency2 = case_when(
    LhCSIEmergency2 == "1" ~ 1,
    LhCSIEmergency2 == "2" ~ 2,
    LhCSIEmergency2 == "3" ~ 4,
    is.na(LhCSIEmergency2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIEmergency2 <- labelled::labelled(Burkina_ea_2020$LhCSIEmergency2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIEmergency2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency2)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIEmergency2 = dplyr::recode(LhCSIEmergency2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIEmergency2 <- labelled::labelled(Burkina_ea_2021$LhCSIEmergency2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency2)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIEmergency2 = dplyr::recode(LhCSIEmergency2,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIEmergency2 <- labelled::labelled(Burkina_ea_2022$LhCSIEmergency2, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency2)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency2)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIEmergency2 <- as.character(Burkina_pdm_2021$LhCSIEmergency2)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIEmergency2 = dplyr::case_when(
      LhCSIEmergency2 == "0" ~ NA,
      .default = as.factor(LhCSIEmergency2)
    ) %>% structure(label = label(LhCSIEmergency2)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIEmergency2 = case_when(
    LhCSIEmergency2 == "1" ~ 1,
    LhCSIEmergency2 == "2" ~ 2,
    LhCSIEmergency2 == "3" ~ 4,
    is.na(LhCSIEmergency2) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIEmergency2 <- labelled::labelled(Burkina_pdm_2021$LhCSIEmergency2, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency2)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency2, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency2-12.png)<!-- -->


### LhCSI : Vendre les derniers animaux femelles reproductrices


```r
###################################Baseline 2018###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency3)
```

```
##                                                                                Non, parce ce n'?tait pas n?cessaire 
##                                                                                                                   1 
## Non, parce que j'ai d?j? vendu ces biens ou a fait de cette activit? dans les 12 derniers mois et je ne peux pas c? 
##                                                                                                                   2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-1.png)<!-- -->

```r
Burkina_baseline_2018$LhCSIEmergency3 <- as.character(Burkina_baseline_2018$LhCSIEmergency3)
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(LhCSIEmergency3 = case_when(
    LhCSIEmergency3 == "1" ~ 1,
    LhCSIEmergency3 == "2" ~ 2,
    is.na(LhCSIEmergency3) ~ 3,
    TRUE ~ 4
  ))

Burkina_baseline_2018$LhCSIEmergency3 <- labelled::labelled(Burkina_baseline_2018$LhCSIEmergency3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_baseline_2018$LhCSIEmergency3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-2.png)<!-- -->

```r
###################################Burkina_ea_2019
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2019$LhCSIEmergency3)
```

```
##                                                                                   No, parce ce n'était pas nécessaire 
##                                                                                                                     1 
## Non, parce que j'ai déjà vendu ces biens ou a fait de cette activité dans les 12 derniers mois et je ne peux pas cont 
##                                                                                                                     2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-3.png)<!-- -->

```r
Burkina_ea_2019$LhCSIEmergency3 <- as.character(Burkina_ea_2019$LhCSIEmergency3)
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(LhCSIEmergency3 = case_when(
    LhCSIEmergency3 == "1" ~ 1,
    LhCSIEmergency3 == "2" ~ 2,
    is.na(LhCSIEmergency3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2019$LhCSIEmergency3 <- labelled::labelled(Burkina_ea_2019$LhCSIEmergency3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2019$LhCSIEmergency3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-4.png)<!-- -->

```r
###################################Burkina_ea_2020
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2020$LhCSIEmergency3)
```

```
##                                                                          Non, parce que cela n'était pas nécessaire 
##                                                                                                                   1 
## Non,  parce que j'ai déjà vendu ces actifs ou fait cette activité et je ne peux pas continuer à déployer cette stra 
##                                                                                                                   2 
##                                                     Non, parce que je n'ai jamais eu la possibilité/Non applicalble 
##                                                                                                                   3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-5.png)<!-- -->

```r
Burkina_ea_2020$LhCSIEmergency3 <- as.character(Burkina_ea_2020$LhCSIEmergency3)
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(LhCSIEmergency3 = case_when(
    LhCSIEmergency3 == "1" ~ 1,
    LhCSIEmergency3 == "2" ~ 2,
    LhCSIEmergency3 == "3" ~ 4,
    is.na(LhCSIEmergency3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_ea_2020$LhCSIEmergency3 <- labelled::labelled(Burkina_ea_2020$LhCSIEmergency3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_ea_2020$LhCSIEmergency3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-6.png)<!-- -->

```r
###################################ea 2021###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency3)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-7.png)<!-- -->

```r
#change labels
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(LhCSIEmergency3 = dplyr::recode(LhCSIEmergency3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2021$LhCSIEmergency3 <- labelled::labelled(Burkina_ea_2021$LhCSIEmergency3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2021$LhCSIEmergency3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-8.png)<!-- -->

```r
###################################ea 2022###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency3)
```

```
##                                                      Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                    1 
## Non, parce que j'ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas con 
##                                                                                                                    2 
##                                                                                                                  Oui 
##                                                                                                                    3 
##                                                                                                       Non applicable 
##                                                                                                                    4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-9.png)<!-- -->

```r
#change labels
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(LhCSIEmergency3 = dplyr::recode(LhCSIEmergency3,"1"=1,"2"=2,"3"=3,"4"=4))
#update labels
Burkina_ea_2022$LhCSIEmergency3 <- labelled::labelled(Burkina_ea_2022$LhCSIEmergency3, c(`Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1, `Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire` = 2, `Oui`= 3,`Non applicable`=4))
#check labels
print("New Labels: \n")
```

```
## [1] "New Labels: \n"
```

```r
expss::val_lab(Burkina_ea_2022$LhCSIEmergency3)
```

```
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-10.png)<!-- -->

```r
###################################Burkina_pdm_2021
###########################################
#View labels
print("Old Labels: \n")
```

```
## [1] "Old Labels: \n"
```

```r
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency3)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-11.png)<!-- -->

```r
Burkina_pdm_2021$LhCSIEmergency3 <- as.character(Burkina_pdm_2021$LhCSIEmergency3)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>%
  dplyr::mutate(
    LhCSIEmergency3 = dplyr::case_when(
      LhCSIEmergency3 == "0" ~ NA,
      .default = as.factor(LhCSIEmergency3)
    ) %>% structure(label = label(LhCSIEmergency3)))
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(LhCSIEmergency3 = case_when(
    LhCSIEmergency3 == "1" ~ 1,
    LhCSIEmergency3 == "2" ~ 2,
    LhCSIEmergency3 == "3" ~ 4,
    is.na(LhCSIEmergency3) ~ 3,
    TRUE ~ 4  
  ))

Burkina_pdm_2021$LhCSIEmergency3 <- labelled::labelled(Burkina_pdm_2021$LhCSIEmergency3, c(`Oui` = 3, `Non, je n'ai pas été confronté à une insuffisance de nourriture` = 1,`Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire`=2, `Non applicable`=4))

#check labels
expss::val_lab(Burkina_pdm_2021$LhCSIEmergency3)
```

```
##                                                                                                                                   Oui 
##                                                                                                                                     3 
##                                                                       Non, je n'ai pas été confronté à une insuffisance de nourriture 
##                                                                                                                                     1 
## Non, parce que j’ai déjà vendu ces actifs ou mené cette activité au cours des 12 derniers mois et je ne peux pas continuer à le faire 
##                                                                                                                                     2 
##                                                                                                                        Non applicable 
##                                                                                                                                     4
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,LhCSIEmergency3, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/LhCSIEmergency3-12.png)<!-- -->


# Self-evaluated resilience score (SERS) 


```r
sers_variables = Burkina_baseline_2018 %>% dplyr::select(gtsummary::starts_with("SERS")) %>% names()

#Burkina_baseline_2018
#df <-Burkina_baseline_2018 %>%
   #dplyr::select(sers_variables)
#No observations 
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))

#Burkina_ea_2019
# df <-Burkina_ea_2019 %>%
#   dplyr::select(sers_variables)
 #Not observations 
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))

#Burkina_ea_2020
# df <-Burkina_ea_2020 %>%
#   dplyr::select(sers_variables)
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))
expss::val_lab(Burkina_ea_2020$SERSRebondir)
```

```
##         tout à fait d'accord                     d'accord 
##                            1                            2 
## ni d'accord ni pas d'accord                  pas d'accord 
##                            3                            4 
##         pas du tout d'accord 
##                            5
```

```r
#Burkina_ea_2021
# df <-Burkina_ea_2021 %>%
#   dplyr::select(sers_variables)
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))
expss::val_lab(Burkina_ea_2021$SERSRebondir)
```

```
##         tout à fait d'accord                     d'accord 
##                            1                            2 
## ni d'accord ni pas d'accord                  pas d'accord 
##                            3                            4 
##         pas du tout d'accord 
##                            5
```

```r
#Burkina_ea_2022
# df <-Burkina_ea_2022 %>%
#   dplyr::select(sers_variables)
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))
expss::val_lab(Burkina_ea_2022$SERSRebondir)
```

```
##         tout à fait d'accord                     d'accord 
##                            1                            2 
## ni d'accord ni pas d'accord                  pas d'accord 
##                            3                            4 
##         pas du tout d'accord 
##                            5
```

```r
#Burkina_pdm_2021
# df <-Burkina_pdm_2021 %>%
#   dplyr::select(sers_variables)
#not obserations
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(sers_variables, ~recode(., 
                    "1" = 1,
                    "2" = 2,
                    "3" = 3,
                    "4" = 4,
                    "5" = 5)))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(sers_variables,
                ~labelled(., labels = c(
                  "tout à fait d'accord" = 1,
                  "d'accord" = 2,
                  "ni d'accord ni pas d'accord " = 3,
                  "pas d'accord" = 4,
                  "pas du tout d'accord" = 5
                )
                )))
```


# ASSET BENEFIT INDICATOR (ABI) 


```r
abi_variables = Burkina_baseline_2018 %>% dplyr::select(gtsummary::starts_with("ABI")) %>% names()
abi_variables <- c(abi_variables,"ActifCreationEmploi",
"BeneficieEmploi",
"TRavailMaintienActif")
#
abi_variables <- abi_variables[! abi_variables %in% c('ABISexparticipant')]


# df <-Burkina_baseline_2018 %>%
#    dplyr::select(abi_variables)

expss::val_lab(Burkina_baseline_2018$ABIProteger)
```

```
## Oui Non  NA 
##   1   2   3
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-1.png)<!-- -->

```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(abi_variables, ~recode(., 
                    "2" = 0,
                    "1" = 1,
                    "3" = 888)))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(abi_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sait pas" = 888))))

expss::val_lab(Burkina_baseline_2018$ABIProteger)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-2.png)<!-- -->

```r
# df <-Burkina_ea_2019 %>%
#    dplyr::select(abi_variables)
expss::val_lab(Burkina_ea_2019$ABIProteger)
```

```
## Oui Non  NA 
##   1   2   3
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-3.png)<!-- -->

```r
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(abi_variables,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(abi_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sait pas" = 888))))
expss::val_lab(Burkina_ea_2019$ABIProteger)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-4.png)<!-- -->

```r
# df <-Burkina_ea_2020 %>%
#    dplyr::select(abi_variables)
expss::val_lab(Burkina_ea_2020$ABIProteger)
```

```
##            Oui            Non Non applicable 
##              1              2              3
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-5.png)<!-- -->

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(abi_variables,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(abi_variables,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-6.png)<!-- -->

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(ABISexparticipant=recode(ABISexparticipant,
                  "2" = 0,
                  "1" = 1,
                 ))
# Burkina_ea_2021
expss::val_lab(Burkina_ea_2021$ABIProteger)
```

```
## NULL
```

```r
Burkina_ea_2021 <-Burkina_ea_2021 %>% dplyr::mutate(across(sers_variables, as.factor))
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-7.png)<!-- -->

```r
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(abi_variables, ~recode(., 
                    "0" = 0,
                    "1" = 1)))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(abi_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sait pas" = 888))))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(ABISexparticipant=recode(ABISexparticipant,
                  "2" = 0,
                  "1" = 1,
                 ))

expss::val_lab(Burkina_ea_2022$ABIProteger)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2022 <-Burkina_ea_2022 %>% dplyr::mutate(across(sers_variables, as.factor))
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-8.png)<!-- -->

```r
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(abi_variables, ~recode(., 
                    "0" = 0,
                    "1" = 1)))
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(abi_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sait pas" = 888))))
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(ABISexparticipant=recode(ABISexparticipant,
                  "2" = 0,
                  "1" = 1,
                 ))
#Pas de pmd 2019


# Burkina_pdm_2021
# df <-Burkina_pdm_2021 %>%
#    dplyr::select(abi_variables)
expss::val_lab(Burkina_pdm_2021$ABIProteger)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-9.png)<!-- -->

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(abi_variables,
                       ~recode(.,
                               "1" = 1,
                               "2" = 0
                       )))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(abi_variables,
                       ~labelled(., labels = c(
                         "Non" = 0,
                         "Oui" = 1,
                         "Ne sait pas" = 888
                       )
                       )))
expss::val_lab(Burkina_pdm_2021$ABIProteger)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,ABIProteger, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-6-10.png)<!-- -->

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(ABISexparticipant=recode(ABISexparticipant,
                  "2" = 0,
                  "1" = 1,
                 ))
```


# DEPART EN EXODE ET MIGRATION  





```r
# Burkina_baseline_2018
  # MigrationEmploi
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,MigrationEmploi, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-1.png)<!-- -->

```r
expss::val_lab(Burkina_baseline_2018$MigrationEmploi)
```

```
## Oui Non 
##   1   2
```

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(MigrationEmploi = case_when(
    MigrationEmploi == 1 ~ 1,
    MigrationEmploi == 2 ~ 0
  ))

  # NbMigrants
#No problem here
Burkina_baseline_2018$NbMigrants <- as_numeric(Burkina_baseline_2018$NbMigrants)

  # RaisonMigration
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,RaisonMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-2.png)<!-- -->

```r
expss::val_lab(Burkina_baseline_2018$RaisonMigration)
```

```
##                            Difficult?s alimentaires conjoncturelles 
##                                                                   1 
##                                   Manque d?opportunit?s ?conomiques 
##                                                                   2 
##                            Uniquement en ann?e de crise alimentaire 
##                                                                   3 
## La migration fait d?sormais partie des moyens d?existence classique 
##                                                                   4 
##                                                  Autre (? pr?ciser) 
##                                                                   5
```

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(RaisonMigration = case_when(
    RaisonMigration == 1 ~ 4,
    RaisonMigration == 2 ~ 1,
    RaisonMigration == 3 ~ 5,
    RaisonMigration == 4 ~ 6,
    RaisonMigration == 5 ~ 9
  ))


  # AutreRaisonEconomiques
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,AutreRaisonEconomiques, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-3.png)<!-- -->

```r
#Not observations 

  # RaisonAccesServices
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,RaisonAccesServices, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-4.png)<!-- -->

```r
#Not observations 

  # DestinationMigration
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,DestinationMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-5.png)<!-- -->

```r
expss::val_lab(Burkina_baseline_2018$DestinationMigration)
```

```
## Autre village de la commune           Ville Ouagadougou 
##                           1                           2 
## Autre ville du Burkina Faso        Autre pays d?Afrique 
##                           3                           4 
##              Hors d?Afrique 
##                           5
```

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% 
  dplyr::mutate(DestinationMigration = case_when(
    DestinationMigration == 1 ~ 1,
    DestinationMigration == 2 ~ 1,
    DestinationMigration == 3 ~ 1,
    DestinationMigration == 4 ~ 2,
    DestinationMigration == 5 ~ 3
  ))


  # DureeMigration
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,DureeMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-6.png)<!-- -->

```r
expss::val_lab(Burkina_baseline_2018$DureeMigration)
```

```
##    Moins d?1 mois dans l?ann?e Entre 1 et 3 mois dans l?ann?e 
##                              1                              2 
## Entre 3 et 6 mois dans l?ann?e Entre 6 et 9 mois dans l?ann?e 
##                              3                              4 
##    Plus de 9 mois dans l?ann?e 
##                              5
```

```r
  # TendanceMigration
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,TendanceMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-7.png)<!-- -->

```r
expss::val_lab(Burkina_baseline_2018$TendanceMigration)
```

```
##   Beaucoup augment? L?g?rement augment?              Stable     Beaucoup baiss? 
##                   1                   2                   3                   4 
##   L?g?rement baiss?                 NSP 
##                   5                   6
```

```r
#ok

  # RaisonHausseMig
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,RaisonHausseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-8.png)<!-- -->

```r
  # RaisonBaisseMig
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,RaisonBaisseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-8-9.png)<!-- -->




```r
#Burkina_ea_2019
  # MigrationEmploi
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,MigrationEmploi, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$MigrationEmploi)
```

```
## Oui Non 
##   1   2
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(MigrationEmploi = case_when(
    MigrationEmploi == 1 ~ 1,
    MigrationEmploi == 2 ~ 0,
  ))


  # NbMigrants
Burkina_ea_2019$NbMigrants <- as_numeric(Burkina_ea_2019$NbMigrants)
#No problem here

  # RaisonMigration
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,RaisonMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$RaisonMigration)
```

```
## NULL
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(RaisonMigration = case_when(
    RaisonMigration == 1 ~ 4,
    RaisonMigration == 2 ~ 1,
    RaisonMigration == 3 ~ 5,
    RaisonMigration == 4 ~ 6,
    RaisonMigration == 5 ~ 9,
  ))
  # AutreRaisonEconomiques
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,AutreRaisonEconomiques, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-3.png)<!-- -->

```r
  # RaisonAccesServices
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,RaisonAccesServices, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-4.png)<!-- -->

```r
  # DestinationMigration
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,DestinationMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$DestinationMigration)
```

```
## NULL
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% 
  dplyr::mutate(DestinationMigration = case_when(
    DestinationMigration == 1 ~ 1,
    DestinationMigration == 2 ~ 1,
    DestinationMigration == 3 ~ 1,
    DestinationMigration == 4 ~ 2,
    DestinationMigration == 5 ~ 3
  ))


  # DureeMigration
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,DureeMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$DureeMigration)
```

```
##    Moins d'1 mois dans l'année Entre 1 et 3 mois dans l'année 
##                              1                              2 
## Entre 3 et 6 mois dans l'année Entre 6 et 9 mois dans l'année 
##                              3                              4 
##    Plus de 9 mois dans l'année 
##                              5
```

```r
#ok 

  # TendanceMigration
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,TendanceMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-7.png)<!-- -->

```r
  # RaisonHausseMig
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,RaisonHausseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-8.png)<!-- -->

```r
  # RaisonBaisseMig
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,RaisonBaisseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-9-9.png)<!-- -->




```r
# Burkina_ea_2020

# MigrationEmploi
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,MigrationEmploi, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$MigrationEmploi)
```

```
## Oui Non 
##   1   2
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(MigrationEmploi = case_when(
    MigrationEmploi == 1 ~ 1,
    MigrationEmploi == 2 ~ 0,
  ))


  # NbMigrants
#No problem here
Burkina_ea_2020$NbMigrants <- as_numeric(Burkina_ea_2020$NbMigrants)

  # RaisonMigration
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,RaisonMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$RaisonMigration)
```

```
##                                                                1. Insécurité au Nigéria ou en Lybie 
##                                                                                                   1 
##                                              2. Manque de moyens financiers pour payer le transport 
##                                                                                                   2 
##                                   3. La migration ne fait pas/plus partie de la stratégie du ménage 
##                                                                                                   3 
## 4. Aucun membre du ménage n'est apte pour la migration (femmes, personnes âgées, enfants à bas âge) 
##                                                                                                   4 
##                                                                5. Occupé par les travaux champêtres 
##                                                                                                   5 
##                                      6. Occupé par les activités de Food For Asset / Cash For Asset 
##                                                                                                   6
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(RaisonMigration = case_when(
    RaisonMigration == 1 ~ 7,
    RaisonMigration == 2 ~ 9,
    RaisonMigration == 3 ~ 6,
    RaisonMigration == 4 ~ 9,
    RaisonMigration == 5 ~ 9,
  ))

  # AutreRaisonEconomiques
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,AutreRaisonEconomiques, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-3.png)<!-- -->

```r
  # RaisonAccesServices
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,RaisonAccesServices, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-4.png)<!-- -->

```r
  # DestinationMigration
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,DestinationMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-5.png)<!-- -->

```r
  # DureeMigration
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,DureeMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$DureeMigration)
```

```
##    1. Moins d'1 mois dans l'année 2. Entre 1 et 3 mois dans l'année 
##                                 1                                 2 
## 3. Entre 3 et 6 mois dans l'année 4. Entre 6 et 9 mois dans l'année 
##                                 3                                 4 
##    5. Plus de 9 mois dans l'année    6. Pas de migrants saisonniers 
##                                 5                                 6
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(DureeMigration = case_when(
    DureeMigration == 6 ~ NA_real_))

  # TendanceMigration
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,TendanceMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-7.png)<!-- -->

```r
  # RaisonHausseMig
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,RaisonHausseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-8.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$RaisonHausseMig)
```

```
##                          1. L'assistance du PAM ne permet de couvrir tous les besoins 
##                                                                                     1 
##          2. La situation alimentaire est difficile dans le village (mauvaise récolte) 
##                                                                                     2 
## 3. La migration est une stratégie habituelle chez les ménages très pauvres du village 
##                                                                                     3 
##                                                                 4. Autre (à préciser) 
##                                                                                     4
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(RaisonHausseMig = case_when(
    RaisonHausseMig == 1 ~ 1,
    RaisonHausseMig == 2 ~ 1,
    RaisonHausseMig == 3 ~ 4,
    RaisonHausseMig == 4 ~ 5,
  ))

  # RaisonBaisseMig
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,RaisonBaisseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-10-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$RaisonBaisseMig)
```

```
##                            1. Les ménages très pauvres ont accès à une assistance régulière 
##                                                                                           1 
##                                              2. La situation alimentaire est moins critique 
##                                                                                           2 
##       3. Les bras valides sont occupés par les activités de Food For Asset / Cash For Asset 
##                                                                                           3 
## 4. La migration n'est pas une stratégie habituelle chez les ménages très pauvres du village 
##                                                                                           4 
##                                                                       5. Autre (à préciser) 
##                                                                                           5
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% 
  dplyr::mutate(RaisonBaisseMig = case_when(
    RaisonBaisseMig == 1 ~ 3,
    RaisonBaisseMig == 2 ~ 4,
    RaisonBaisseMig == 3 ~ 3,
    RaisonBaisseMig == 4 ~ 5,
    RaisonBaisseMig == 5 ~ 7,
  ))
```



```r
# Burkina_ea_2021
# MigrationEmploi
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,MigrationEmploi, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$MigrationEmploi)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(MigrationEmploi = case_when(
    MigrationEmploi == "0" ~ 0,
    MigrationEmploi == "1" ~ 1,
    MigrationEmploi == "888" ~ NA_real_
  ))


  # NbMigrants
Burkina_ea_2021$NbMigrants <-as_numeric(Burkina_ea_2021$NbMigrants)
#No problem here

  # RaisonMigration
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,RaisonMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$RaisonMigration)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(RaisonMigration = case_when(
    RaisonMigration == "1" ~ 1,
    RaisonMigration == "2" ~ 2,
    RaisonMigration == "3" ~ 3,
    RaisonMigration == "4" ~ 4,
    RaisonMigration == "5" ~ 5,
    RaisonMigration == "6" ~ 6,
    RaisonMigration == "7" ~ 7,
    RaisonMigration == "8" ~ 8,
    RaisonMigration == "9" ~ 9,
  ))


  # AutreRaisonEconomiques
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,AutreRaisonEconomiques, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$AutreRaisonEconomiques)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(AutreRaisonEconomiques = case_when(
    AutreRaisonEconomiques == "1" ~ 1,
    AutreRaisonEconomiques == "2" ~ 2,
    AutreRaisonEconomiques == "3" ~ 3
  ))


  # RaisonAccesServices
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,RaisonAccesServices, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-4.png)<!-- -->

```r
  # DestinationMigration
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,DestinationMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$DestinationMigration)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(DestinationMigration = case_when(
    DestinationMigration == "1" ~ 1,
    DestinationMigration == "2" ~ 2,
    DestinationMigration == "3" ~ 3,
    DestinationMigration == "5" ~ NA
    
  ))


  # DureeMigration
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,DureeMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$DureeMigration)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(DureeMigration = case_when(
    DureeMigration == "1" ~ 1,
    DureeMigration == "2" ~ 2,
    DureeMigration == "3" ~ 3,
    DureeMigration == "4" ~ 4,
    DureeMigration == "5" ~ 5,
    DureeMigration == "6" ~ 6,
    DureeMigration == "other" ~ NA_real_
  ))


  # TendanceMigration
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,TendanceMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-7.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$TendanceMigration)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(TendanceMigration = case_when(
    TendanceMigration == "1" ~ 1,
    TendanceMigration == "2" ~ 2,
    TendanceMigration == "3" ~ 3,
    TendanceMigration == "4" ~ 4,
    TendanceMigration == "5" ~ 5,
    TendanceMigration == "6" ~ 6,
  ))


  # RaisonHausseMig
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,RaisonHausseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-8.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$RaisonHausseMig)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(RaisonHausseMig = case_when(
    RaisonHausseMig == "1" ~ 1,
    RaisonHausseMig == "2" ~ 2,
    RaisonHausseMig == "3" ~ 3,
    RaisonHausseMig == "4" ~ 4,
  ))

  # RaisonBaisseMig
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,RaisonBaisseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-11-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$RaisonBaisseMig)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(RaisonBaisseMig = case_when(
    RaisonHausseMig == 1 ~ 1,
    RaisonHausseMig == 2 ~ 2,
    RaisonHausseMig == 3 ~ 3,
    RaisonHausseMig == 4 ~ 4,
    RaisonHausseMig == 5 ~ 5,
  ))
```




```r
# Burkina_ea_2022

# MigrationEmploi
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,MigrationEmploi, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$MigrationEmploi)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(MigrationEmploi = case_when(
    MigrationEmploi == 888 ~ NA_real_
  ))

  # NbMigrants
Burkina_ea_2022$NbMigrants <- as_numeric(Burkina_ea_2022$NbMigrants)
#No problem here

  # RaisonMigration
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,RaisonMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$RaisonMigration)
```

```
##                                Recherche d'opportunités économiques 
##                                                                   0 
##    Catastrophes naturelles (par ex., inondations, sécheresse, etc.) 
##                                                                   0 
##                      Accès aux services de base (santé, éducation…) 
##                                                                   0 
##                            Difficultés alimentaires conjoncturelles 
##                                                                   0 
##                            Uniquement en année de crise alimentaire 
##                                                                   0 
## La migration fait désormais partie des moyens d'existence classique 
##                                                                   0 
##                                                      Guerre/conflit 
##                                                                   0 
##                                      Violence ciblée ou persécution 
##                                                                   0 
##                                Autres à préciser |________________| 
##                                                                   0 
##                                                               Other 
##                                                                   0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(RaisonMigration = case_when(
    as.character(RaisonMigration) == "1" ~ 1,
    as.character(RaisonMigration) == "2" ~ 2,
    as.character(RaisonMigration) == "3" ~ 3,
    as.character(RaisonMigration) == "4" ~ 4,
    as.character(RaisonMigration) == "5" ~ 5,
    as.character(RaisonMigration) == "7" ~ 7,
    as.character(RaisonMigration) == "8" ~ 8,
    as.character(RaisonMigration) == "other" ~ 9
  ))

  # AutreRaisonEconomiques
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,AutreRaisonEconomiques, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$AutreRaisonEconomiques)
```

```
##                Déplacements quotidiens/hebdomadaires pour le travail 
##                                                                    0 
## Activité agricole et pastorale (transhumance, migration saisonnière) 
##                                                                    0 
##                       Recherche d'opportunités d'emploi à l'étranger 
##                                                                    0 
##                                                                Other 
##                                                                    0 
##                                       Affaires (marché, vente/achat) 
##                                                                    0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(AutreRaisonEconomiques = case_when(
    as.character(AutreRaisonEconomiques) == "1" ~ 2,
    as.character(AutreRaisonEconomiques) == "2" ~ 3,
    as.character(AutreRaisonEconomiques) == "3" ~ 4,
    as.character(AutreRaisonEconomiques) == "4" ~ 5,
    as.character(AutreRaisonEconomiques) == "5" ~ 1
  ))

  # RaisonAccesServices
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,RaisonAccesServices, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-4.png)<!-- -->

```r
  # DestinationMigration
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,DestinationMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-5.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(DestinationMigration = case_when(
    as.character(DestinationMigration) == "1" ~ 2,
    as.character(DestinationMigration) == "2" ~ 3,
    as.character(DestinationMigration) == "3" ~ 3,
    as.character(DestinationMigration) == "4" ~ 1
  ))

  # DureeMigration
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,DureeMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$DureeMigration)
```

```
##       1 à 3 mois       3 à 6 mois       6 à 9 mois     10 à 12 mois 
##                0                0                0                0 
## Plus de 12 mois.            Other   Mois d'un mois 
##                0                0                0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(DureeMigration = case_when(
    as.character(DureeMigration) == "1" ~ 2,
    as.character(DureeMigration) == "2" ~ 3,
    as.character(DureeMigration) == "3" ~ 4,
    as.character(DureeMigration) == "4" ~ 5,
    as.character(DureeMigration) == "5" ~ 6,
    as.character(DureeMigration) == "6" ~ 6,
    as.character(DureeMigration) == "7" ~ 1,
    as.character(DureeMigration) == "other" ~ NA_real_
  ))

  # TendanceMigration
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,TendanceMigration, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-7.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$TendanceMigration)
```

```
##   Beaucoup augmenté Légèrement augmenté              Stable     Beaucoup baissé 
##                   1                   2                   3                   4 
##   Légèrement baissé       Ne sait pas ; 
##                   5                   6
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(TendanceMigration = case_when(
    TendanceMigration == 1 ~ 1,
    TendanceMigration == 2 ~ 2,
    TendanceMigration == 3 ~ 3,
    TendanceMigration == 4 ~ 4,
    TendanceMigration == 5 ~ 5,
    TendanceMigration == 6 ~ 6,
  ))


  # RaisonHausseMig
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,RaisonHausseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-8.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$RaisonHausseMig)
```

```
##                                                                                   Manque d'opportunités économiques 
##                                                                                                                   0 
## Dégradation de l'environnement (pertes de bétail, baisse de la production et du rendement à cause de la sécheresse, 
##                                                                                                                   0 
##                                                 La migration fait désormais partie des moyens d'existence classique 
##                                                                                                                   0 
##                                                                                                               Other 
##                                                                                                                   0 
##                                                                            Difficultés alimentaires conjoncturelles 
##                                                                                                                   0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(RaisonHausseMig = case_when(
    as.character(RaisonHausseMig) == "1" ~ 2,
    as.character(RaisonHausseMig) == "2" ~ 3,
    as.character(RaisonHausseMig) == "3" ~ 4,
    as.character(RaisonHausseMig) == "4" ~ 5,
    as.character(RaisonHausseMig) == "5" ~ 1
    ))


  # RaisonBaisseMig
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,RaisonBaisseMig, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-12-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$RaisonBaisseMig)
```

```
##                                                         Voyage vers la Lybie/ Nigeria devenu trop dangereux/ couteux 
##                                                                                                                    0 
##          Les ménages pauvres ont accès à une assistance régulière/ les bras valides sont occupés par les travaux FFA 
##                                                                                                                    0 
##                                                         La situation alimentaire générale du village s'est améliorée 
##                                                                                                                    0 
## La migration fait désormais partie des moyens d'existence classique 6. Emergence d'opportunités économiques grâce au 
##                                                                                                                    0 
##                                                                                                                Other 
##                                                                                                                    0 
##                                                Moins d'opportunités économiques ou insécurité au Nigéria ou en Lybie 
##                                                                                                                    0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(RaisonBaisseMig = case_when(
    as.character(RaisonBaisseMig) == "1" ~ 2,
    as.character(RaisonBaisseMig) == "2" ~ 3,
    as.character(RaisonBaisseMig) == "3" ~ 4,
    as.character(RaisonBaisseMig) == "4" ~ 5,
    as.character(RaisonBaisseMig) == "5" ~ 7,
    as.character(RaisonBaisseMig) == "6" ~ 1
  ))
```




```r
# Burkina_pdm_2021
mig_variables = c("MigrationEmploi",
"NbMigrants",
"RaisonMigration",
"AutreRaisonEconomiques",
"RaisonAccesServices",
"DestinationMigration",
"DureeMigration",
"TendanceMigration",
"RaisonHausseMig",
"RaisonBaisseMig"
)
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% 
  dplyr::mutate(across(as_factor(mig_variables))) 
```


# Social capital index (Indice de capital social)


```r
SCI_var = c("SCIAideIntraCom", "SCIAideDehorsCom", "SCIEvolRessSociales", 
            "SCIPersAAiderCom", "SCIPersAAiderEnDehorsCom", 
            "SCIConMembreGvrnmt", "SCIPersConMembreGvrnmt", 
            "SCICapAideGvnmt","SCIConMembreNGO", "SCIPersConMembreNGO",
            "SCIAideAubesoin")

Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
           mutate(across(as_factor(SCI_var)))
```




```r
Burkina_ea_2019 <- Burkina_ea_2019 %>%
          mutate(across(as_factor(SCI_var)))
```




```r
Burkina_ea_2020 <- Burkina_ea_2020 %>%
           mutate(across(as_factor(SCI_var)))
```




```r
#SCIAideIntraCom
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIAideIntraCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIAideIntraCom)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIAideIntraCom = case_when(
    as.character(SCIAideIntraCom) == "1" ~ 1,
    as.character(SCIAideIntraCom) == "2" ~ 2,
    as.character(SCIAideIntraCom) == "3" ~ 3,
    as.character(SCIAideIntraCom) == "4" ~ 4,
    as.character(SCIAideIntraCom) == "888" ~ 888,
    as.character(SCIAideIntraCom) == "8888" ~ 8888
  ))

#SCIAideDehorsCom
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIAideDehorsCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIAideDehorsCom)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIAideDehorsCom = case_when(
    as.character(SCIAideDehorsCom) == "1" ~ 1,
    as.character(SCIAideDehorsCom) == "2" ~ 2,
    as.character(SCIAideDehorsCom) == "3" ~ 3,
    as.character(SCIAideDehorsCom) == "4" ~ 4,
    as.character(SCIAideDehorsCom) == "888" ~ 888,
    as.character(SCIAideDehorsCom) == "8888" ~ 8888
  ))
#SCIEvolRessSociales
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIEvolRessSociales, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIEvolRessSociales)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIEvolRessSociales = case_when(
    as.character(SCIEvolRessSociales) == "1" ~ 1,
    as.character(SCIEvolRessSociales) == "2" ~ 2,
    as.character(SCIEvolRessSociales) == "3" ~ 3,
    as.character(SCIEvolRessSociales) == "888" ~ 8,
    as.character(SCIEvolRessSociales) == "8888" ~ 9
  ))

#SCIPersAAiderCom
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIPersAAiderCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIPersAAiderCom)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIPersAAiderCom = case_when(
    as.character(SCIPersAAiderCom) == "1" ~ 1,
    as.character(SCIPersAAiderCom) == "2" ~ 2,
    as.character(SCIPersAAiderCom) == "3" ~ 3,
    as.character(SCIPersAAiderCom) == "4" ~ 4,
    as.character(SCIPersAAiderCom) == "5" ~ 5,
    as.character(SCIPersAAiderCom) == "888" ~ 888,
    as.character(SCIPersAAiderCom) == "8888" ~ 8888,
    TRUE ~ 5
  ))

#SCIPersAAiderEnDehorsCom
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIPersAAiderEnDehorsCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIPersAAiderEnDehorsCom)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIPersAAiderEnDehorsCom = case_when(
    as.character(SCIPersAAiderEnDehorsCom) == "1" ~ 1,
    as.character(SCIPersAAiderEnDehorsCom) == "2" ~ 2,
    as.character(SCIPersAAiderEnDehorsCom) == "3" ~ 3,
    as.character(SCIPersAAiderEnDehorsCom) == "4" ~ 4,
    as.character(SCIPersAAiderEnDehorsCom) == "5" ~ 5,
    as.character(SCIPersAAiderEnDehorsCom) == "888" ~ 888,
    as.character(SCIPersAAiderEnDehorsCom) == "8888" ~ 8888,
  ))

#SCIConMembreGvrnmt"
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIConMembreGvrnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIConMembreGvrnmt)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIConMembreGvrnmt = case_when(
    as.character(SCIConMembreGvrnmt) == "1" ~ 1,
    as.character(SCIConMembreGvrnmt) == "0" ~ 0,
    as.character(SCIConMembreGvrnmt) == "888" ~ 888))

#SCIPersConMembreGvrnmt"
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIPersConMembreGvrnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-7.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIPersConMembreGvrnmt)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIPersConMembreGvrnmt = case_when(
    as.character(SCIPersConMembreGvrnmt) == "1" ~ 1,
    as.character(SCIPersConMembreGvrnmt) == "2" ~ 2,
    as.character(SCIPersConMembreGvrnmt) == "3" ~ 3,
    as.character(SCIPersConMembreGvrnmt) == "4" ~ 4,
    as.character(SCIPersConMembreGvrnmt) == "888" ~ 8,
    as.character(SCIPersConMembreGvrnmt) == "8888" ~ 9
  ))


#SCICapAideGvnmt
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCICapAideGvnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-8.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCICapAideGvnmt)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCICapAideGvnmt = case_when(
    as.character(SCICapAideGvnmt) == "1" ~ 1,
    as.character(SCICapAideGvnmt) == "0" ~ 0,
    as.character(SCICapAideGvnmt) == "888" ~ 888
  ))

#SCIConMembreNGO"
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIConMembreNGO, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIConMembreNGO)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIConMembreNGO = case_when(
    as.character(SCIConMembreNGO) == "1" ~ 1,
    as.character(SCIConMembreNGO) == "0" ~ 0,      
    as.character(SCIConMembreNGO) == "888" ~ 888
  ))


#SCIPersConMembreNGO
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIPersConMembreNGO, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIPersConMembreNGO)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIPersConMembreNGO = case_when(
    as.character(SCIPersConMembreNGO) == "1" ~ 1,
    as.character(SCIPersConMembreNGO) == "2" ~ 2,
    as.character(SCIPersConMembreNGO) == "3" ~ 3,
    as.character(SCIPersConMembreNGO) == "4" ~ 4,
    as.character(SCIPersConMembreNGO) == "888" ~ 8,
    as.character(SCIPersConMembreNGO) == "8888" ~ 9
  ))


#SCIAideAubesoin
Burkina_ea_2021 %>%
  plot_frq(coord.flip =T,SCIAideAubesoin, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2021-11.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$SCIAideAubesoin)
```

```
## NULL
```

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% 
  dplyr::mutate(SCIAideAubesoin = case_when(
    as.character(SCIAideAubesoin) == "1" ~ 1,
    as.character(SCIAideAubesoin) == "0" ~ 0,
    as.character(SCIAideAubesoin) == "888" ~ 888,
    as.character(SCIAideAubesoin) == "8888" ~ 8888
  ))
```




```r
#SCIAideIntraCom
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIAideIntraCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIAideIntraCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIAideIntraCom = case_when(
    as.character(SCIAideIntraCom) == "1" ~ 1,
    as.character(SCIAideIntraCom) == "2" ~ 2,
    as.character(SCIAideIntraCom) == "3" ~ 3,
    as.character(SCIAideIntraCom) == "4" ~ 4,
    as.character(SCIAideIntraCom) == "888" ~ 888,
    as.character(SCIAideIntraCom) == "8888" ~ 8888
  ))

#SCIAideDehorsCom
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIAideDehorsCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIAideDehorsCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIAideDehorsCom = case_when(
    as.character(SCIAideDehorsCom) == "1" ~ 1,
    as.character(SCIAideDehorsCom) == "2" ~ 2,
    as.character(SCIAideDehorsCom) == "3" ~ 3,
    as.character(SCIAideDehorsCom) == "4" ~ 4,
    as.character(SCIAideDehorsCom) == "888" ~ 888,
    as.character(SCIAideDehorsCom) == "8888" ~ 8888
  ))

#SCIEvolRessSociales
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIEvolRessSociales, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIEvolRessSociales)
```

```
##           Augmenté  Est resté le même          A diminué        Ne sait pas 
##                  1                  2                  3                888 
## Refuse de répondre 
##               8888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIEvolRessSociales = case_when(
    as.character(SCIEvolRessSociales) == "1" ~ 1,
    as.character(SCIEvolRessSociales) == "2" ~ 2,
    as.character(SCIEvolRessSociales) == "3" ~ 3,
    as.character(SCIEvolRessSociales) == "888" ~ 8,
    as.character(SCIEvolRessSociales) == "8888" ~ 9
  ))

#SCIPersAAiderCom
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIPersAAiderCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIPersAAiderCom)
```

```
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         0 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         0 
##                                                  Personne 
##                                                         0 
##                                               Ne sait pas 
##                                                         0 
##                                        Refuse de répondre 
##                                                         0 
##                                                   Parents 
##                                                         0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIPersAAiderCom = case_when(
    as.character(SCIPersAAiderCom) == "1" ~ 1,
    as.character(SCIPersAAiderCom) == "2" ~ 2,
    as.character(SCIPersAAiderCom) == "3" ~ 3,
    as.character(SCIPersAAiderCom) == "4" ~ 4,
    as.character(SCIPersAAiderCom) == "888" ~ 888,
    as.character(SCIPersAAiderCom) == "8888" ~ 8888
  ))


#SCIPersAAiderEnDehorsCom
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIPersAAiderEnDehorsCom, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-5.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIPersAAiderEnDehorsCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIPersAAiderEnDehorsCom = case_when(
    as.character(SCIPersAAiderEnDehorsCom) == "1" ~ 1,
    as.character(SCIPersAAiderEnDehorsCom) == "2" ~ 2,
    as.character(SCIPersAAiderEnDehorsCom) == "3" ~ 3,
    as.character(SCIPersAAiderEnDehorsCom) == "4" ~ 4,
    as.character(SCIPersAAiderEnDehorsCom) == "888" ~ 888,
    as.character(SCIPersAAiderEnDehorsCom) == "8888" ~ 8888
  ))


#SCIConMembreGvrnmt
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIConMembreGvrnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-6.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIConMembreGvrnmt)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIPersAAiderEnDehorsCom = case_when(
    as.character(SCIPersAAiderEnDehorsCom) == "1" ~ 1,
    as.character(SCIPersAAiderEnDehorsCom) == "0" ~ 0,
    as.character(SCIPersAAiderEnDehorsCom) == "888" ~ 888))

#SCIPersConMembreGvrnmt
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIPersConMembreGvrnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-7.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIPersConMembreGvrnmt)
```

```
##                                                Ami(e) 
##                                                     0 
##                                                Voisin 
##                                                     0 
## Connaissance (membre d'un groupe, ami d'un ami, etc.) 
##                                                     0 
##                                           Ne sait pas 
##                                                     0 
##                                   Refuse de répondre. 
##                                                     0 
##                                                 Other 
##                                                     0 
##                  Un membre de la famille ou un parent 
##                                                     0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIPersConMembreGvrnmt = case_when(
    as.character(SCIPersConMembreGvrnmt) == "1" ~ 1,
    as.character(SCIPersConMembreGvrnmt) == "2" ~ 2,
    as.character(SCIPersConMembreGvrnmt) == "3" ~ 3,
    as.character(SCIPersConMembreGvrnmt) == "4" ~ 4,
    as.character(SCIPersConMembreGvrnmt) == "8888" ~ 9
  ))

#SCICapAideGvnmt
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCICapAideGvnmt, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-8.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCICapAideGvnmt)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCICapAideGvnmt = case_when(
    as.character(SCICapAideGvnmt) == "1" ~ 1,
    as.character(SCICapAideGvnmt) == "0" ~ 0,
    as.character(SCICapAideGvnmt) == "888" ~ 888))

#SCIConMembreNGO
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIConMembreNGO, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-9.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIConMembreNGO)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIConMembreNGO = case_when(
    as.character(SCIConMembreNGO) == "1" ~ 1,
    as.character(SCIConMembreNGO) == "0" ~ 0,
    as.character(SCIConMembreNGO) == "888" ~ 888))


#SCIPersConMembreNGO
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIPersConMembreNGO, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-10.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIPersConMembreNGO)
```

```
##                                                Ami(e) 
##                                                     0 
##                                                Voisin 
##                                                     0 
## Connaissance (membre d'un groupe, ami d'un ami, etc.) 
##                                                     0 
##                                           Ne sait pas 
##                                                     0 
##                                   Refuse de répondre. 
##                                                     0 
##                                                 Other 
##                                                     0 
##                  Un membre de la famille ou un parent 
##                                                     0
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIPersConMembreNGO = case_when(
    as.character(SCIPersConMembreNGO) == "1" ~ 1,
    as.character(SCIPersConMembreNGO) == "2" ~ 2,
    as.character(SCIPersConMembreNGO) == "3" ~ 3,
    as.character(SCIPersConMembreNGO) == "4" ~ 4,
    as.character(SCIPersConMembreNGO) == "8888" ~ 9
  ))

#SCIAideAubesoin
Burkina_ea_2022 %>%
  plot_frq(coord.flip =T,SCIAideAubesoin, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/sci variables Burkina_ea_2022-11.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$SCIAideAubesoin)
```

```
##                         Non                         Oui 
##                           0                           1 
##              Je ne sais pas Je ne souhaite pas répondre 
##                         888                        8888
```

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% 
  dplyr::mutate(SCIAideAubesoin = case_when(
    as.character(SCIAideAubesoin) == "1" ~ 1,
    as.character(SCIAideAubesoin) == "0" ~ 0,
    as.character(SCIAideAubesoin) == "888" ~ 888,
    as.character(SCIAideAubesoin) == "8888" ~ 8888
  ))
```





```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>%
           mutate(across(as_factor(SCI_var)))
```


# Social capital index (Indice de capital social)




# DIVERSITE ALIMENTAIRE DES FEMMES 


```r
PWMDDW_variables = Burkina_baseline_2018 %>% dplyr::select(gtsummary::starts_with("PWMDD")) %>% names()

# df <-Burkina_baseline_2018 %>%
#    dplyr::select(PWMDDW_variables)
Burkina_baseline_2018$MDDW_resp_age <- as_numeric(Burkina_baseline_2018$MDDW_resp_age)

################################################
expss::val_lab(Burkina_baseline_2018$PWMDDWStapRoo)
```

```
## NULL
```

```r
Burkina_baseline_2018 %>%
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-1.png)<!-- -->

```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  dplyr::mutate(across(PWMDDW_variables,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "888" = 888
                 )))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  dplyr::mutate(across(PWMDDW_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sais pas" = 888
              ))))
expss::val_lab(Burkina_baseline_2018$PWMDDWStapRoo)
```

```
##         Non         Oui Ne sais pas 
##           0           1         888
```

```r
Burkina_baseline_2018 %>%
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-2.png)<!-- -->

```r
################################################


################################################
#Burkina_ea_2019
Burkina_ea_2019$MDDW_resp_age <- as_numeric(Burkina_ea_2019$MDDW_resp_age)
# # df <-Burkina_ea_2019 %>%
# #    dplyr::select(PWMDDW_variables)
expss::val_lab(Burkina_ea_2019$PWMDDWStapRoo)
```

```
## NULL
```

```r
Burkina_ea_2019 %>%
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-3.png)<!-- -->

```r
Burkina_ea_2019 <- Burkina_ea_2019 %>%
  dplyr::mutate(across(PWMDDW_variables,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "888" = 888
                 )))
Burkina_ea_2019 <- Burkina_ea_2019 %>%
  dplyr::mutate(across(PWMDDW_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sais pas" = 888))))
expss::val_lab(Burkina_ea_2019$PWMDDWStapRoo)
```

```
##         Non         Oui Ne sais pas 
##           0           1         888
```

```r
Burkina_ea_2019 %>%
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-4.png)<!-- -->

```r
################################################


################################################
# df <-Burkina_ea_2020 %>%
#    dplyr::select(PWMDDW_variables)
Burkina_ea_2020$MDDW_resp_age <- as_numeric(Burkina_ea_2020$MDDW_resp_age)
expss::val_lab(Burkina_ea_2020$PWMDDWStapRoo)
```

```
## Non Oui NSP 
##   0   1   8
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-5.png)<!-- -->

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(PWMDDW_variables,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "8" = 888
                 )))
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(PWMDDW_variables,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sais pas" = 888))))

expss::val_lab(Burkina_ea_2020$PWMDDWStapRoo)
```

```
##         Non         Oui Ne sais pas 
##           0           1         888
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-6.png)<!-- -->

```r
################################################

################################################
#Burkina_ea_2021

# df <-Burkina_ea_2021 %>%
#    dplyr::select(PWMDDW_variables)
Burkina_ea_2021$MDDW_resp_age <- ifelse(Burkina_ea_2021$MDDW_resp_age == 1979, 42,
                               ifelse(Burkina_ea_2021$MDDW_resp_age == 1986, 35,
                                      Burkina_ea_2021$MDDW_resp_age))
Burkina_ea_2021$MDDW_resp_age <- as_numeric(Burkina_ea_2021$MDDW_resp_age)
expss::val_lab(Burkina_ea_2021$PWMDDWStapRoo)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-7.png)<!-- -->

```r
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(PWMDDW_variables, ~recode(., 
                    "0" = 0,
                    "1" = 1)))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(PWMDDW_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sais pas" = 888))))
#Burkina_ea_2022
# df <-Burkina_ea_2022 %>%
#    dplyr::select(PWMDDW_variables)
Burkina_ea_2022$MDDW_resp_age <- as_numeric(Burkina_ea_2022$MDDW_resp_age)
expss::val_lab(Burkina_ea_2022$PWMDDWStapRoo)
```

```
## NULL
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-8.png)<!-- -->

```r
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(PWMDDW_variables, ~recode(., 
                    "0" = 0,
                    "1" = 1)))
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(PWMDDW_variables,
            ~labelled(., labels = c(
              "Non" = 0,
              "Oui" = 1,
              "Ne sais pas" = 888))))

################################################
# Burkina_pdm_2021
# df <-Burkina_pdm_2021 %>%
#    dplyr::select(PWMDDW_variables)
Burkina_pdm_2021$MDDW_resp_age <- as_numeric(Burkina_pdm_2021$MDDW_resp_age)
expss::val_lab(Burkina_pdm_2021$PWMDDWStapRoo)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-9.png)<!-- -->

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(PWMDDW_variables,
                       ~recode(.,
                               "1" = 1,
                               "2" = 0,
                               "99" = 888
                       )))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(PWMDDW_variables,
                       ~labelled(., labels = c(
                         "Non" = 0,
                         "Oui" = 1,
                         "Ne sais pas" = 888
                       )
                       )))
expss::val_lab(Burkina_pdm_2021$PWMDDWStapRoo)
```

```
##         Non         Oui Ne sais pas 
##           0           1         888
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,PWMDDWStapRoo, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/DIVERSITE ALIMENTAIRE DES FEMMES-10.png)<!-- -->

# Régime alimentaire minimum acceptable (MAD)


```r
mad_variables = c("MAD_sex",
"MAD_dob",
"MAD_resp_age",
"EverBreastF",
"PCIYCBreastF",
"PCIYCInfFormNb",
"PCIYCDairyMiNb",
"PCIYCDairyYoNb",
"PCIYCStapPoNb",
"MAD_module",
"PCMADStapCer",
"PCMADVegOrg",
"PCMADStapRoo",
"PCMADVegGre",
"PCMADFruitOrg",
"PCMADVegFruitOth",
"PCMADPrMeatO",
"PCMADPrMeatF",
"PCMADPrEgg",
"PCMADPrFish",
"PCMADPulse",
"PCMADDairy",
"PCMADFatRpalm",
"PCMADSnfChild",
"PCMADSnfPowd",
"PCMADSnfLns",
"PCIYCMeals"
)

mad_variables_har = c(
"EverBreastF",
"PCIYCBreastF",
"MAD_module",
"PCMADStapCer",
"PCMADVegOrg",
"PCMADStapRoo",
"PCMADVegGre",
"PCMADFruitOrg",
"PCMADVegFruitOth",
"PCMADPrMeatO",
"PCMADPrMeatF",
"PCMADPrEgg",
"PCMADPrFish",
"PCMADPulse",
"PCMADDairy",
"PCMADFatRpalm",
"PCMADSnfChild",
"PCMADSnfPowd",
"PCMADSnfLns"
)

PCI_Num <- c("PCIYCInfFormNb",
"PCIYCDairyMiNb",
"PCIYCDairyYoNb",
"PCIYCStapPoNb",
"PCIYCMeals"
)


#Burkina_baseline_2018

# df <-Burkina_baseline_2018 %>%
#    dplyr::select(mad_variables)
Burkina_baseline_2018$MAD_resp_age <- as_numeric(Burkina_baseline_2018$MAD_resp_age)
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(as_numeric((across(PCI_Num))))

Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))


#Burkina_ea_2019

# df <-Burkina_ea_2019 %>%
#    dplyr::select(mad_variables)

Burkina_ea_2019$MAD_resp_age <- as_numeric(Burkina_ea_2019$MAD_resp_age)
Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(as_numeric((across(PCI_Num))))
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate(MAD_sex = dplyr::recode(MAD_sex,"1"=1,"2"=0))

expss::val_lab(Burkina_ea_2019$PCIYCBreastF)
```

```
## Oui Non NSP 
##   1   2   3
```

```r
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))
expss::val_lab(Burkina_ea_2019$PCIYCBreastF)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,PCIYCBreastF, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Régime alimentaire minimum acceptable (MAD)-1.png)<!-- -->

```r
#Burkina_ea_2020

# df <-Burkina_ea_2020 %>%
#    dplyr::select(mad_variables)
Burkina_ea_2020$MAD_resp_age <- as_numeric(Burkina_ea_2020$MAD_resp_age)
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(as_numeric((across(PCI_Num))))

Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))
#Burkina_ea_2021

# df <-Burkina_ea_2021 %>%
#    dplyr::select(mad_variables)

Burkina_ea_2021$MAD_resp_age <- as_numeric(Burkina_ea_2021$MAD_resp_age)
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(as_numeric((across(PCI_Num))))
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate(MAD_sex = dplyr::recode(MAD_sex,"1"=1,"2"=0))

expss::val_lab(Burkina_ea_2021$PCIYCBreastF)
```

```
## NULL
```

```r
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "888" = 888
                 )))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))
expss::val_lab(Burkina_ea_2021$PCIYCBreastF)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,PCIYCBreastF, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Régime alimentaire minimum acceptable (MAD)-2.png)<!-- -->

```r
#Burkina_ea_2022

# df <-Burkina_ea_2022 %>%
#    dplyr::select(mad_variables)
Burkina_ea_2022$MAD_resp_age <- as_numeric(Burkina_ea_2022$MAD_resp_age)
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(as_numeric((across(PCI_Num))))

Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "2" = 0,
                  "1" = 1,
                  "3" = 888
                 )))
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))

#Burkina_pdm_2021

# df <-Burkina_pdm_2021 %>%
#    dplyr::select(mad_variables)

Burkina_pdm_2021$MAD_resp_age <- as_numeric(Burkina_pdm_2021$MAD_resp_age)
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(as_numeric((across(PCI_Num))))

Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate(MAD_sex = dplyr::recode(MAD_sex,"1"=1,"2"=0))

expss::val_lab(Burkina_pdm_2021$PCIYCBreastF)
```

```
## NULL
```

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "99" = 888
                 )))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(mad_variables_har,
                ~labelled(., labels = c(
                  "Non" = 0,
                  "Oui" = 1,
                  "Ne sait pas" = 888))))
expss::val_lab(Burkina_pdm_2021$PCIYCBreastF)
```

```
##         Non         Oui Ne sait pas 
##           0           1         888
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,PCIYCBreastF, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Régime alimentaire minimum acceptable (MAD)-3.png)<!-- -->


# Date format check 


```r
#as.Date(19213, origin = "1970-01-01")
#as.Date(43791, origin = "1899-12-30")

Burkina_baseline_2018$SvyDatePDM<-as.Date(Burkina_baseline_2018$SvyDatePDM)

Burkina_ea_2019$SvyDatePDM<-as.Date(Burkina_ea_2019$SvyDatePDM)

#Burkina_pdm_2019


Burkina_ea_2020$SvyDatePDM <- sub("T.*", "", Burkina_ea_2020$SvyDatePDM)
Burkina_ea_2020$SvyDatePDM<-as.Date(Burkina_ea_2020$SvyDatePDM)

Burkina_ea_2021$SvyDatePDM<-as.Date(Burkina_ea_2021$SvyDatePDM)

Burkina_pdm_2021$SvyDatePDM<-as.Date(Burkina_pdm_2021$SvyDatePDM)

Burkina_ea_2022$SvyDatePDM<-as.Date(Burkina_ea_2022$SvyDatePDM)
```

#Household size check

```r
Burkina_baseline_2018%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-1.png)<!-- -->

```r
#Not problem ok

Burkina_ea_2019%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-2.png)<!-- -->

```r
#NA's found in variable

Burkina_ea_2020%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-3.png)<!-- -->

```r
#NA's found in variable

Burkina_ea_2021%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-4.png)<!-- -->

```r
#NA's found in variable

Burkina_ea_2022%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-5.png)<!-- -->

```r
#Not problem ok

# Burkina_pdm_2019%>% 
#   plot_frq(coord.flip =T,HHSize, show.na = T)

Burkina_pdm_2021%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size check-6.png)<!-- -->

```r
#Not problem ok
```

#Household size calculation 

```r
HHvars <- c("HHSize05M","HHSize23M","HHSize59M","HHSize5114M","HHSize1549M","HHSize5064M","HHSize65AboveM","HHSize05F","HHSize23F","HHSize59F","HHSize5114F","HHSize1549F","HHSize5064F","HHSize65AboveF")
HH_data <- select(Burkina_baseline_2018, HHvars)
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% mutate(across(HHvars, as.numeric))

HH_data <- select(Burkina_pdm_2021, HHvars)
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% mutate(across(HHvars, as.numeric))

HH_data <- select(Burkina_ea_2022, HHvars)
Burkina_ea_2022 <- Burkina_ea_2022 %>% mutate(across(HHvars, as.numeric))

# Burkina_ea_2019

HH_data <- select(Burkina_ea_2019, HHvars)
Burkina_ea_2019 <- Burkina_ea_2019 %>% mutate(across(HHvars, as.numeric))
HH_data <- mutate_all(HH_data, as.numeric)
Burkina_ea_2019$HHSize <- rowSums(HH_data, na.rm = TRUE)
Burkina_ea_2019%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size calculation-1.png)<!-- -->

```r
#Burkina_ea_2020

HH_data <- select(Burkina_ea_2020, HHvars)
Burkina_ea_2020 <- Burkina_ea_2020 %>% mutate(across(HHvars, as.numeric))
HH_data <- mutate_all(HH_data, as.numeric)
Burkina_ea_2020$HHSize <- rowSums(HH_data, na.rm = TRUE)
Burkina_ea_2020%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size calculation-2.png)<!-- -->

```r
#Burkina_ea_2021
condition = Burkina_ea_2021['ID'] == 156
Burkina_ea_2021[condition, 'HHSize65AboveM'] = "7"
HH_data <- select(Burkina_ea_2021, HHvars)
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(across(HHvars, as.numeric))
HH_data <- mutate_all(HH_data, as.numeric)
Burkina_ea_2021$HHSize <- rowSums(HH_data, na.rm = TRUE)
Burkina_ea_2021%>% 
  plot_frq(coord.flip =T,HHSize, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household size calculation-3.png)<!-- -->


# Gender recodification


```r
# We need to recode gender label to:
# 0 = Femme
# 1 = Homme


#View labels
expss::val_lab(Burkina_baseline_2018$HHHSex)
```

```
## Masculin  F?minin 
##        1        2
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-1.png)<!-- -->

```r
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(HHHSex = dplyr::recode(HHHSex,`2` = 0, `1` = 1))
Burkina_baseline_2018$HHHSex <- labelled::labelled(Burkina_baseline_2018$HHHSex, c(Femme = 0, Homme = 1))
#Check new labels
expss::val_lab(Burkina_baseline_2018$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-2.png)<!-- -->

```r
#View labels
expss::val_lab(Burkina_ea_2019$HHHSex)
```

```
## Masculin    Femme 
##        1        2
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-3.png)<!-- -->

```r
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(HHHSex = dplyr::recode(HHHSex,"2" = 0, "1" = 1))
Burkina_ea_2019$HHHSex <- labelled::labelled(Burkina_ea_2019$HHHSex, c(Femme = 0, Homme = 1))

#Check labels
expss::val_lab(Burkina_ea_2019$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-4.png)<!-- -->

```r
#####Burkina_pdm_2019

#View labels
expss::val_lab(Burkina_ea_2020$HHHSex)
```

```
## Masculin  Feminin 
##        1        2
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-5.png)<!-- -->

```r
Burkina_ea_2020$HHHSex<-dplyr::recode(Burkina_ea_2020$HHHSex, "1" = 1, "2" = 0)
Burkina_ea_2020$HHHSex <- labelled::labelled(Burkina_ea_2020$HHHSex, c(Femme = 0, Homme = 1))
#Check new labels
expss::val_lab(Burkina_ea_2020$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-6.png)<!-- -->

```r
#View labels
expss::val_lab(Burkina_ea_2021$HHHSex)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-7.png)<!-- -->

```r
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(HHHSex = dplyr::recode(HHHSex,`1` = 1, `2` = 0))

Burkina_ea_2021$HHHSex <- labelled::labelled(Burkina_ea_2021$HHHSex, c(Femme = 0, Homme = 1))

#Check labels
expss::val_lab(Burkina_ea_2021$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-8.png)<!-- -->

```r
#View labels
expss::val_lab(Burkina_ea_2022$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-9.png)<!-- -->

```r
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(HHHSex = dplyr::recode(HHHSex,`1` = 1, `0` = 0))

Burkina_ea_2022$HHHSex <- labelled::labelled(Burkina_ea_2022$HHHSex, c(Femme = 0, Homme = 1))
#Check labels
expss::val_lab(Burkina_ea_2022$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-10.png)<!-- -->

```r
#View labels
expss::val_lab(Burkina_pdm_2021$HHHSex)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-11.png)<!-- -->

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(HHHSex = dplyr::recode(HHHSex,`2` = 0, `1` = 1))

Burkina_pdm_2021$HHHSex <- labelled::labelled(Burkina_pdm_2021$HHHSex, c(Femme = 0, Homme = 1))

#Check labels
expss::val_lab(Burkina_pdm_2021$HHHSex)
```

```
## Femme Homme 
##     0     1
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,HHHSex)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Gender recodification-12.png)<!-- -->


# Household head education level


```r
expss::val_lab(Burkina_baseline_2018$HHHEdu)
```

```
##       Aucun Alphab?tis?   Coranique    Primaire  Secondaire   Sup?rieur 
##           1           2           3           4           5           6
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-1.png)<!-- -->

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate(HHHEdu = dplyr::recode(HHHEdu,"1"=1,"2"=2,"3"=2,"4"=3,"5"=4, "6"=5))

Burkina_baseline_2018$HHHEdu <- labelled::labelled(Burkina_baseline_2018$HHHEdu, c(Aucune = 1, `Alphabétisé ou Coranique` = 2, Primaire= 3,Secondaire=4, Superieur=5))
#check labels
expss::val_lab(Burkina_baseline_2018$HHHEdu)
```

```
##                   Aucune Alphabétisé ou Coranique                 Primaire 
##                        1                        2                        3 
##               Secondaire                Superieur 
##                        4                        5
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-2.png)<!-- -->

```r
##
expss::val_lab(Burkina_ea_2019$HHHEdu)
```

```
##        Aucun  Alphabétisé    Coranique     Primaire   Secondaire    Supérieur 
##            1            2            3            4            5            6 
## Franco-arabe 
##            7
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-3.png)<!-- -->

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate(HHHEdu = dplyr::recode(HHHEdu,"1"=1,"2"=2,"3"=2,"4"=3,"5"=4, "6"=5, "7" = 2))


Burkina_ea_2019$HHHEdu <- labelled::labelled(Burkina_ea_2019$HHHEdu, c(Aucune = 1, `Alphabétisé ou Coranique` = 2, Primaire= 3,Secondaire=4, Superieur=5))
expss::val_lab(Burkina_ea_2019$HHHEdu)
```

```
##                   Aucune Alphabétisé ou Coranique                 Primaire 
##                        1                        2                        3 
##               Secondaire                Superieur 
##                        4                        5
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-4.png)<!-- -->

```r
#### Burkina_pdm_2019

expss::val_lab(Burkina_ea_2020$HHHEdu)
```

```
##       Aucun Alphabétisé   Coranique    Primaire  Secondaire   Supérieur 
##           1           2           3           4           5           6
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-5.png)<!-- -->

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate(HHHEdu = dplyr::recode(HHHEdu,"1"=1,"2"=2,"3"=2,"4"=3,"5"=4, "6"=5))
Burkina_ea_2020$HHHEdu <- labelled::labelled(Burkina_ea_2020$HHHEdu, c(Aucune = 1, `Alphabétisé ou Coranique` = 2, Primaire= 3,Secondaire=4, Superieur=5))
expss::val_lab(Burkina_ea_2020$HHHEdu)
```

```
##                   Aucune Alphabétisé ou Coranique                 Primaire 
##                        1                        2                        3 
##               Secondaire                Superieur 
##                        4                        5
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-6.png)<!-- -->

```r
## EA 2021 not available (only NAs)
expss::val_lab(Burkina_ea_2021$HHHEdu)
```

```
## NULL
```

```r
Burkina_ea_2021$HHHEdu<-as.factor(Burkina_ea_2021$HHHEdu)

expss::val_lab(Burkina_ea_2022$HHHEdu)
```

```
##                    Aucun Alphabétisé ou Coranique                 Primaire 
##                        1                        2                        3 
##               Secondaire                Supérieur 
##                        4                        5
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-7.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate(HHHEdu = dplyr::recode(HHHEdu,"1"=1,"2"=2,"3"=3,"4"=4))
Burkina_ea_2022$HHHEdu <- labelled::labelled(Burkina_ea_2022$HHHEdu, c(Aucune = 1, `Alphabétisé ou Coranique` = 2, Primaire= 3,Secondaire=4))
expss::val_lab(Burkina_ea_2022$HHHEdu)
```

```
##                   Aucune Alphabétisé ou Coranique                 Primaire 
##                        1                        2                        3 
##               Secondaire 
##                        4
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,HHHEdu)
```

![](01_BFA_LabelsHarmonization_files/figure-html/Household head education level-8.png)<!-- -->

```r
##

## PDM 2021 not available (only NAs)
expss::val_lab(Burkina_pdm_2021$HHHEdu)
```

```
## NULL
```

```r
Burkina_pdm_2021$HHHEdu<-as.factor(Burkina_pdm_2021$HHHEdu)
```

#TransfBenef


```r
#view(table(Burkina_baseline_2018$TransfBenef))
#No observations
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0))
Burkina_baseline_2018$TransfBenef <- labelled::labelled(Burkina_baseline_2018$TransfBenef, c(Oui = 1, `Non` = 0)) 

Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,TransfBenef)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-15-1.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$TransfBenef)
```

```
## Oui Non 
##   1   2
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0))
Burkina_ea_2019$TransfBenef <- labelled::labelled(Burkina_ea_2019$TransfBenef, c(Oui = 1, `Non` = 0))
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,TransfBenef)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-15-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$TransfBenef)
```

```
## Oui Non 
##   1   0
```

```r
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,TransfBenef)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-15-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2019$TransfBenef)
```

```
## Oui Non 
##   1   0
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0))
Burkina_ea_2020$TransfBenef <- labelled::labelled(Burkina_ea_2020$TransfBenef, c(Oui = 1, `Non` = 0))
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,TransfBenef)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-15-4.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2020$TransfBenef)
```

```
## Oui Non 
##   1   0
```

```r
#view(table(Burkina_ea_2021$TransfBenef))
#No observations
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0,
              .default = 1))
Burkina_ea_2021$TransfBenef <- labelled::labelled(Burkina_ea_2021$TransfBenef, c(Oui = 1, `Non` = 0)) 

#view(table(Burkina_ea_2022$TransfBenef))
#No observations
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0))
Burkina_ea_2022$TransfBenef <- labelled::labelled(Burkina_ea_2022$TransfBenef, c(Oui = 1, `Non` = 0)) 

#view(table(Burkina_pdm_2021$TransfBenef))
#No observations
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate(TransfBenef = dplyr::recode(TransfBenef,
              "1"=1,
              "2"=0))
Burkina_pdm_2021$TransfBenef <- labelled::labelled(Burkina_pdm_2021$TransfBenef, c(Oui = 1, `Non` = 0)) 
```

# HHHMatrimonial


```r
# Monogame    Polygame     Divorcé(e)   Veuf/Veuve    Célibataire   
#   1           2           3              4           5               
expss::val_lab(Burkina_baseline_2018$HHHMatrimonial)
```

```
## Mari?(e) monogame Mari?(e) polygame        Divorc?(e)        Veuf/Veuve 
##                 1                 2                 3                 4 
##       C?libataire       Concubinage 
##                 5                 6
```

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate(HHHMatrimonial = dplyr::recode(HHHMatrimonial,"1"=1,"2"=2,"3"=3,"4"=4,"5"=5, "6"=5))
Burkina_baseline_2018$HHHMatrimonial <- labelled::labelled(Burkina_baseline_2018$HHHMatrimonial, c(Monogame = 1, `Polygame` = 2, `Divorcé(e)`= 3,`Veuf/Veuve`=4, `Célibataire`=5))
expss::val_lab(Burkina_baseline_2018$HHHMatrimonial)
```

```
##    Monogame    Polygame  Divorcé(e)  Veuf/Veuve Célibataire 
##           1           2           3           4           5
```

```r
Burkina_baseline_2018 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-1.png)<!-- -->

```r
##Burkina_pdm_2019

expss::val_lab(Burkina_ea_2019$HHHMatrimonial)
```

```
## Marié monogame Marié polygame        Divorcé     Veuf/Veuve    Célibataire 
##              1              2              3              4              5 
##    Concubinage 
##              6
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate(HHHMatrimonial = dplyr::recode(HHHMatrimonial,"1"=1,"2"=2,"3"=3,"4"=4,"5"=5,"6"=5))
Burkina_ea_2019$HHHMatrimonial <- labelled::labelled(Burkina_ea_2019$HHHMatrimonial, c(Monogame = 1, Polygame = 2, `Divorcé(e)`= 3,`Veuf/Veuve`=4, `Célibataire`=5))
expss::val_lab(Burkina_ea_2019$HHHMatrimonial)
```

```
##    Monogame    Polygame  Divorcé(e)  Veuf/Veuve Célibataire 
##           1           2           3           4           5
```

```r
Burkina_ea_2019 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-2.png)<!-- -->

```r
#no observations 
expss::val_lab(Burkina_ea_2020$HHHMatrimonial)
```

```
##  Marié monogame  Marié polygame Divorcé /Séparé      Veuf/Veuve     Célibataire 
##               1               2               3               4               5
```

```r
Burkina_ea_2020$HHHMatrimonial<-as.factor(Burkina_ea_2020$HHHMatrimonial)
Burkina_ea_2020 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-3.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2021$HHHMatrimonial)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-4.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate(HHHMatrimonial = dplyr::recode(HHHMatrimonial,"1"=1,"2"=2,"3"=3,"4"=4,"5"=5))
Burkina_ea_2021$HHHMatrimonial <- labelled::labelled(Burkina_ea_2021$HHHMatrimonial, c(Monogame = 1, Polygame = 2, `Divorcé(e)`= 3,`Veuf/Veuve`=4, `Célibataire`=5))
expss::val_lab(Burkina_ea_2021$HHHMatrimonial)
```

```
##    Monogame    Polygame  Divorcé(e)  Veuf/Veuve Célibataire 
##           1           2           3           4           5
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-5.png)<!-- -->

```r
expss::val_lab(Burkina_pdm_2021$HHHMatrimonial)
```

```
## NULL
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-6.png)<!-- -->

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate(HHHMatrimonial = dplyr::recode(HHHMatrimonial,"1"=1,"2"=2,"3"=3,"4"=4,"5"=5))
Burkina_pdm_2021$HHHMatrimonial <- labelled::labelled(Burkina_pdm_2021$HHHMatrimonial, c(Monogame = 1, Polygame = 2, `Divorcé(e)`= 3,`Veuf/Veuve`=4, `Célibataire`=5))
expss::val_lab(Burkina_pdm_2021$HHHMatrimonial)
```

```
##    Monogame    Polygame  Divorcé(e)  Veuf/Veuve Célibataire 
##           1           2           3           4           5
```

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-7.png)<!-- -->

```r
#no observations
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,HHHMatrimonial, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-16-8.png)<!-- -->

```r
Burkina_ea_2022$HHHMatrimonial<-as.factor(Burkina_ea_2022$HHHMatrimonial)
```


# HHSourceIncome


```r
expss::val_lab(Burkina_baseline_2018$HHSourceIncome)
```

```
##                     Agriculture vivrière et de rente 
##                                                    1 
##           Elevage de gros bétail et produits dérivés 
##                                                    2 
##                  Elevage de bétail de taille moyenne 
##                                                    3 
##                                  Elevage de volaille 
##                                                    4 
##                                           Maraîchage 
##                                                    5 
##                                            Artisanat 
##                                                    6 
##                               Ressources forestières 
##                                                    7 
##                                                Pêche 
##                                                    8 
##                     Commerce de produits alimentaire 
##                                                    9 
##                           Commerce informel/ambulant 
##                                                   10 
##                      Transport (y compris taxi-moto) 
##                                                   11 
## Travail spécialisé (maçon, peintre, menuisier, etc.) 
##                                                   12 
##                      Travail journalier non agricole 
##                                                   13 
##                                  Salarié/Contractuel 
##                                                   14 
##                                Retraité/Pensionnaire 
##                                                   15 
##                                  Transferts d'argent 
##                                                   16 
##                                           Dons/Aides 
##                                                   17 
##                                    Chasse/cueillette 
##                                                   18 
##                                               Autres 
##                                                   19
```

```r
#expss::val_lab(Burkina_pdm_2019$HHSourceIncome)
expss::val_lab(Burkina_ea_2019$HHSourceIncome)  #No observations
```

```
## NULL
```

```r
expss::val_lab(Burkina_ea_2020$HHSourceIncome)
```

```
## NULL
```

```r
expss::val_lab(Burkina_ea_2021$HHSourceIncome)  #No observations
```

```
## NULL
```

```r
expss::val_lab(Burkina_pdm_2021$HHSourceIncome) #No observations
```

```
## NULL
```

```r
expss::val_lab(Burkina_ea_2022$HHSourceIncome)  #No observations
```

```
## NULL
```


# Assistance

## Date assistance check 


```r
#View(table(Burkina_baseline_2018$DebutAssistance))
#No observations
Burkina_baseline_2018$DebutAssistance<-as.Date(Burkina_baseline_2018$DebutAssistance)

#No observations
#View(table(Burkina_ea_2019$DebutAssistance))
Burkina_ea_2019$DebutAssistance<-as.Date(Burkina_ea_2019$DebutAssistance)


#Burkina_pdm_2019


#View(table(Burkina_ea_2020$DebutAssistance))
Burkina_ea_2020$DebutAssistance<-as.Date(Burkina_ea_2020$DebutAssistance)

#View(table(Burkina_ea_2021$DebutAssistance))
Burkina_ea_2021$DebutAssistance<-as.Date(Burkina_ea_2021$DebutAssistance)

#No observations
#View(table(Burkina_pdm_2021$DebutAssistance))
Burkina_pdm_2021$DebutAssistance<-as.factor(Burkina_pdm_2021$DebutAssistance)

#View(table(Burkina_ea_2022$DebutAssistance))
Burkina_ea_2022$DebutAssistance<-as.Date(Burkina_ea_2022$DebutAssistance)
```

## Date last assistance check 


```r
expss::val_lab(Burkina_baseline_2018$DateDerniereAssist)
```

```
## NULL
```

```r
Burkina_baseline_2018 <- 
  Burkina_baseline_2018 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"other"=NA_real_))
Burkina_baseline_2018$DateDerniereAssist <- labelled::labelled(Burkina_baseline_2018$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3))

#expss::val_lab(Burkina_pdm_2019$DateDerniereAssist)

expss::val_lab(Burkina_ea_2019$DateDerniereAssist)
```

```
## NULL
```

```r
Burkina_ea_2019 <- 
  Burkina_ea_2019 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"other"=NA_real_))
Burkina_ea_2019$DateDerniereAssist <- labelled::labelled(Burkina_ea_2019$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3))

expss::val_lab(Burkina_ea_2020$DateDerniereAssist)
```

```
## NULL
```

```r
Burkina_ea_2020 <- 
  Burkina_ea_2020 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"other"=NA_real_))
Burkina_ea_2020$DateDerniereAssist <- labelled::labelled(Burkina_ea_2020$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3)) 

expss::val_lab(Burkina_ea_2021$DateDerniereAssist)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,DateDerniereAssist,show.na =T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-19-1.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"other"=NA_real_))
Burkina_ea_2021$DateDerniereAssist <- labelled::labelled(Burkina_ea_2021$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3))
expss::val_lab(Burkina_ea_2021$DateDerniereAssist)
```

```
##   moins d’une semaine entre 1 et 3 semaines    plus de 3 semaines 
##                     1                     2                     3
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,DateDerniereAssist,show.na =T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-19-2.png)<!-- -->

```r
expss::val_lab(Burkina_ea_2022$DateDerniereAssist)
```

```
## entre 1 et 3 semaines    plus de 3 semaines                 Other 
##                     0                     0                     0 
##   Moins d'une semaine 
##                     0
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,DateDerniereAssist,show.na =T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-19-3.png)<!-- -->

```r
Burkina_ea_2022 <- 
  Burkina_ea_2022 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"other"=NA_real_))
Burkina_ea_2022$DateDerniereAssist <- labelled::labelled(Burkina_ea_2022$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3))
expss::val_lab(Burkina_ea_2022$DateDerniereAssist)
```

```
##   moins d’une semaine entre 1 et 3 semaines    plus de 3 semaines 
##                     1                     2                     3
```

```r
Burkina_ea_2022 %>% 
  plot_frq(coord.flip =T,DateDerniereAssist,show.na =T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-19-4.png)<!-- -->

```r
Burkina_pdm_2021 %>% 
  plot_frq(coord.flip =T,DateDerniereAssist,show.na =T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-19-5.png)<!-- -->

```r
expss::val_lab(Burkina_pdm_2021$DateDerniereAssist)
```

```
## NULL
```

```r
Burkina_pdm_2021 <- 
  Burkina_pdm_2021 %>% dplyr::mutate(DateDerniereAssist = dplyr::recode(DateDerniereAssist,"1"=1,"2"=2,"3"=3,"245"=3, "other"=NA_real_))
Burkina_pdm_2021$DateDerniereAssist <- labelled::labelled(Burkina_pdm_2021$DateDerniereAssist, c(`moins d’une semaine` = 1, `entre 1 et 3 semaines` = 2,`plus de 3 semaines`=3))
```
 

## Type d'assistance

```r
var_type_assistance = c("BanqueCerealiere",
"VivreContreTravail",
"ArgentContreTravail",
"ArgentetVivreContreTravail",
"DistribVivresSoudure",
"DistribArgentSoudure",
"BoursesAdo",
"BlanketFeedingChildren",
"BlanketFeedingWomen",
"MAMChildren",
"MASChildren",
"MAMPLWomen",
"FARNcommunaut",
"FormationRenfCapacite",
"CashTransfert",
"CantineScolaire",
"AutreTransferts"
)

#1=Oui, PAM  2=Oui, Autre  3=NSP

labels_var_type_assistance <- c(`Oui, PAM` = 1, `Oui, Autre` = 2, `NSP` = 3, `NA` = NA)

#Burkina_baseline_2018

#No observations
# df <-Burkina_baseline_2018 %>%
#     dplyr::select(var_type_assistance)
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "1" = 0,
                  "2" = 1,
                  "3" = 3
                 )))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_baseline_2018$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

```r
#Burkina_pdm_2019

#Burkina_ea_2019

# df <-Burkina_ea_2019 %>%
#    dplyr::select(var_type_assistance)
#No observations
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "1" = 1,
                  "2" = 2,
                  "3" = 3
                 )))
Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_ea_2019$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

```r
#Burkina_ea_2020

# df <-Burkina_ea_2020 %>%
#   dplyr::select(var_type_assistance)
expss::val_lab(Burkina_ea_2020$BanqueCerealiere)
```

```
##         PAM       Autre Ne sait pas 
##           1           2           3
```

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "1" = 1,
                  "2" = 2,
                  "3" = 3
                 )))
Burkina_ea_2020 <- Burkina_ea_2020 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_ea_2020$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

```r
#Burkina_ea_2021
# df <-Burkina_ea_2021 %>%
#   dplyr::select(var_type_assistance)
Burkina_ea_2021 <- Burkina_ea_2021 %>% mutate(across(var_type_assistance,
                ~recode(.,
                        .default = 0)))
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "0" = 1,
                  "2" = 2,
                  "3" = 3
                 )))
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_ea_2021$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

```r
# df <-Burkina_pdm_2021 %>%
#   dplyr::select(var_type_assistance)
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "1" = 1,
                  "2" = 2,
                  "3" = 3
                 )))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_pdm_2021$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

```r
# df <-Burkina_ea_2022 %>%
#   dplyr::select(var_type_assistance)
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(var_type_assistance,
                ~recode(.,
                  "1" = 1,
                  "2" = 2,
                  "3" = 3
                 )))
Burkina_ea_2022 <- Burkina_ea_2022 %>%
  mutate(across(all_of(var_type_assistance),
                ~labelled(., labels = labels_var_type_assistance)))
expss::val_lab(Burkina_ea_2022$BanqueCerealiere)
```

```
##   Oui, PAM Oui, Autre        NSP         NA 
##          1          2          3         NA
```

## Epargne

```r
var_epargne = c("ExistGroupeEpargne",
"MembreGroupeEpargne",
"EpargneAvantPam",
"EpargneSansPam",
"PossibilitePret",
"AutreSourcePret",
"EpargnePieds"
)

#1=Oui  0=Non  888= Ne sait pas

labels_var_epargne<- c(`Oui` = 1, `Non` = 0, `Ne sait pas` = 888,`NA` = NA)

#Burkina_baseline_2018

#No observations
# df <-Burkina_baseline_2018 %>%
#     dplyr::select(var_epargne)
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "0" = 0,
                  "1" = 1,
                  "888" = 888,
                  "8888" = 0
                 )))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_baseline_2018$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

```r
#Burkina_pdm_2019

#Burkina_ea_2019

# df <-Burkina_ea_2019 %>%
#    dplyr::select(var_epargne)
#No observations
Burkina_ea_2019 <- Burkina_ea_2019 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "1" = 1,
                  "0" = 0,
                  "888"= 888,
                  "8888" = 0
                 )))
Burkina_ea_2019 <- Burkina_ea_2019 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_ea_2019$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

```r
#Burkina_ea_2020

# df <-Burkina_ea_2020 %>%
#   dplyr::select(var_epargne)
expss::val_lab(Burkina_ea_2020$MembreGroupeEpargne)
```

```
## NULL
```

```r
Burkina_ea_2020 <- Burkina_ea_2020 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "1" = 1,
                  "2" = 0,
                  "888" = 888,
                  "8888" = 0
                 )))
Burkina_ea_2020 <- Burkina_ea_2020 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_ea_2020$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

```r
#Burkina_ea_2021
# df <-Burkina_ea_2021 %>%
#   dplyr::select(var_epargne)
Burkina_ea_2021 <- Burkina_ea_2021 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "1" = 1,
                  "2" = 0,
                  "888" = 888,
                  "8888"=0
                 )))
Burkina_ea_2021 <- Burkina_ea_2021 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_ea_2021$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

```r
# df <-Burkina_pdm_2021 %>%
#   dplyr::select(var_epargne)
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "1" = 1,
                  "0" = 0,
                  "888" = 888,
                  "8888"=0
                 )))
Burkina_pdm_2021 <- Burkina_pdm_2021 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_pdm_2021$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

```r
# df <-Burkina_ea_2022 %>%
#   dplyr::select(var_epargne)
Burkina_ea_2022 <- Burkina_ea_2022 %>% 
  dplyr::mutate(across(var_epargne,
                ~recode(.,
                  "1" = 1,
                  "2" = 0,
                  "888" = 888,
                  "8888"=0
                 )))
Burkina_ea_2022 <- Burkina_ea_2022 %>%
  mutate(across(all_of(var_epargne),
                ~labelled(., labels = labels_var_epargne)))
expss::val_lab(Burkina_ea_2022$MembreGroupeEpargne)
```

```
##         Oui         Non Ne sait pas          NA 
##           1           0         888          NA
```

# HHHMainActivity


```r
##not modality for these variables


expss::val_lab(Burkina_ea_2021$HHHMainActivity)
```

```
## NULL
```

```r
Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHMainActivity)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-20-1.png)<!-- -->

```r
Burkina_ea_2021 <- 
  Burkina_ea_2021 %>% dplyr::mutate(HHHMainActivity = dplyr::recode(HHHMainActivity,
              "1"=1,"2"=2,"3"=3,
              "4"=4, "5"=5,"6"=6,
              "7"=7, "8"=8, "9"=9,
              "10"=10, "11"=11, "12"=12,
              "13"=13))

Burkina_ea_2021 %>% 
  plot_frq(coord.flip =T,HHHMainActivity)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-20-2.png)<!-- -->

```r
Burkina_ea_2021$HHHMainActivity <- as_numeric(Burkina_ea_2021$HHHMainActivity)
expss::val_lab(Burkina_ea_2021$HHHMainActivity)
```

```
## NULL
```

```r
Burkina_pdm_2021 <- Burkina_pdm_2021 %>% dplyr::mutate(HHHMainActivity = as_factor(HHHMainActivity))
Burkina_ea_2022 <- Burkina_ea_2022 %>% dplyr::mutate(HHHMainActivity = as_factor(HHHMainActivity))
Burkina_ea_2020 <- Burkina_ea_2020 %>% dplyr::mutate(HHHMainActivity = as_factor(HHHMainActivity))
Burkina_baseline_2018 <- Burkina_baseline_2018 %>% dplyr::mutate(HHHMainActivity = as_factor(HHHMainActivity))
Burkina_ea_2019 <- Burkina_ea_2019 %>% dplyr::mutate(HHHMainActivity = as_factor(HHHMainActivity))
```

# Merging all data


```r
WFP_BFA<-plyr::rbind.fill(Burkina_baseline_2018,
#Burkina_pdm_2019,
Burkina_ea_2019,
Burkina_ea_2020,
Burkina_ea_2021,
Burkina_pdm_2021,
Burkina_ea_2022)
WFP_BFA$ID<-as.numeric(WFP_BFA$ID)
WFP_BFA$Longitude<-as.numeric(WFP_BFA$Longitude)
WFP_BFA$Latitude<-as.numeric(WFP_BFA$Latitude)
WFP_BFA$Longitude_precision<-as.numeric(WFP_BFA$Longitude_precision)
WFP_BFA$Latitude_precision<-as.numeric(WFP_BFA$Latitude_precision)
WFP_BFA$DebutAssistance<-as.Date(WFP_BFA$DebutAssistance)
WFP_BFA$SvyDatePDM <-as.Date(WFP_BFA$SvyDatePDM)
WFP_BFA$HHHAge<-as.numeric(WFP_BFA$HHHAge)
WFP_BFA <- WFP_BFA  %>% filter(HHHSex != 19632773)
WFP_BFA$MAD_dob <-as_date(WFP_BFA$MAD_dob)  
WFP_BFA$MAD_sex <- labelled::labelled(WFP_BFA$MAD_sex, c(`Homme`= 1, `Femme`=0))
```


### FCS: Viande, poisson et oeufs - Sources label


```r
WFP_BFA$FCSPrSRf <- as_numeric(WFP_BFA$FCSPrSRf) 
WFP_BFA$FCSPrSRf <- labelled::labelled(WFP_BFA$FCSPrSRf, c(`Production propre (récoltes, élevage)` = 1, `Pêche / Chasse` = 2,`Cueillette` = 3,`Prêts`=4,`Marché (achat avec des espèces)`=5,`Marché (achat à crédit)`=6,`Mendicité`=7, `Troc travail ou biens contre des aliments`=8,`Dons (aliments) de membres de la famille ou d’amis`=9,`Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc`=10))
#check labels
expss::val_lab(WFP_BFA$FCSPrSRf)
```

```
##                              Production propre (récoltes, élevage) 
##                                                                  1 
##                                                     Pêche / Chasse 
##                                                                  2 
##                                                         Cueillette 
##                                                                  3 
##                                                              Prêts 
##                                                                  4 
##                                    Marché (achat avec des espèces) 
##                                                                  5 
##                                            Marché (achat à crédit) 
##                                                                  6 
##                                                          Mendicité 
##                                                                  7 
##                          Troc travail ou biens contre des aliments 
##                                                                  8 
##                 Dons (aliments) de membres de la famille ou d’amis 
##                                                                  9 
## Aide alimentaire de la société civile, ONG, gouvernement, PAM, etc 
##                                                                 10
```

```r
WFP_BFA %>% 
  plot_frq(coord.flip =T,FCSPrSRf,show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/FCSPr Sources label-1.png)<!-- -->


# DEPART EN EXODE ET MIGRATION  


```r
#MigrationEmploi
WFP_BFA$MigrationEmploi <- as_numeric(WFP_BFA$MigrationEmploi)
WFP_BFA$MigrationEmploi <- 
  labelled::labelled(WFP_BFA$MigrationEmploi, c(`Oui` = 1, `Non` = 0))
expss::val_lab(WFP_BFA$MigrationEmploi)
```

```
## Oui Non 
##   1   0
```

```r
#NbMigrants
WFP_BFA$NbMigrants <- as_numeric(WFP_BFA$NbMigrants)

#RaisonMigration
WFP_BFA$RaisonMigration <- as_numeric(WFP_BFA$RaisonMigration)
WFP_BFA$RaisonMigration <- 
  labelled::labelled(
    WFP_BFA$RaisonMigration,
    c(`Recherche d’opportunités économiques` = 1,
      `Catastrophes naturelles (par ex., inondations, sécheresse, etc.)`
                                              =2,
      `Accès aux services de base (santé, éducation…)` = 3,
      `Difficultés alimentaires conjoncturelles` = 4, 
      `Uniquement en année de crise alimentaire` = 5,
      `La migration fait désormais partie des moyens d’existence classique`
                                                  = 6,
      `Guerre/conflit` = 7,
      `Violence ciblée ou persécution` = 8,
      `Autres à préciser` = 9))
expss::val_lab(WFP_BFA$RaisonMigration)
```

```
##                                Recherche d’opportunités économiques 
##                                                                   1 
##    Catastrophes naturelles (par ex., inondations, sécheresse, etc.) 
##                                                                   2 
##                      Accès aux services de base (santé, éducation…) 
##                                                                   3 
##                            Difficultés alimentaires conjoncturelles 
##                                                                   4 
##                            Uniquement en année de crise alimentaire 
##                                                                   5 
## La migration fait désormais partie des moyens d’existence classique 
##                                                                   6 
##                                                      Guerre/conflit 
##                                                                   7 
##                                      Violence ciblée ou persécution 
##                                                                   8 
##                                                   Autres à préciser 
##                                                                   9
```

```r
#AutreRaisonEconomiques

WFP_BFA$AutreRaisonEconomiques <- as_numeric(WFP_BFA$AutreRaisonEconomiques)
WFP_BFA$AutreRaisonEconomiques <- 
  labelled::labelled(
    WFP_BFA$AutreRaisonEconomiques,
    c(
      `Affaires (marché, vente/achat)` = 1,
      `Déplacements quotidiens/hebdomadaires pour le travail` = 2,
      `Activité agricole et pastorale (transhumance, migration 
                                       saisonnière)` = 3,
      `Recherche d'opportunités d'emploi à l'étranger` = 4,
      `Autre, précisez` = 5
    ))
expss::val_lab(WFP_BFA$AutreRaisonEconomiques)
```

```
##                                                                                Affaires (marché, vente/achat) 
##                                                                                                             1 
##                                                         Déplacements quotidiens/hebdomadaires pour le travail 
##                                                                                                             2 
## Activité agricole et pastorale (transhumance, migration \n                                       saisonnière) 
##                                                                                                             3 
##                                                                Recherche d'opportunités d'emploi à l'étranger 
##                                                                                                             4 
##                                                                                               Autre, précisez 
##                                                                                                             5
```

```r
#RaisonAccesServices
WFP_BFA$RaisonAccesServices <- as_numeric(WFP_BFA$RaisonAccesServices)
WFP_BFA$RaisonAccesServices <- 
  labelled::labelled(
    WFP_BFA$RaisonAccesServices,
    c(
      `Accès à la nourriture, à l'eau` = 1,
      `L''accès aux services de base (éducation primaire, soins de santé 
      primaires)` = 2,
      `Accès aux services humanitaires` = 3,
      `Enseignement supérieur (lycée et niveaux supérieurs)` = 4,
      `Santé (soins médicaux spécialisés)` = 5,
      `Autres services (préciser)` = 6
    ))
expss::val_lab(WFP_BFA$RaisonAccesServices)
```

```
##                                                       Accès à la nourriture, à l'eau 
##                                                                                    1 
## L''accès aux services de base (éducation primaire, soins de santé \n      primaires) 
##                                                                                    2 
##                                                      Accès aux services humanitaires 
##                                                                                    3 
##                                 Enseignement supérieur (lycée et niveaux supérieurs) 
##                                                                                    4 
##                                                   Santé (soins médicaux spécialisés) 
##                                                                                    5 
##                                                           Autres services (préciser) 
##                                                                                    6
```

```r
#DestinationMigration
WFP_BFA$DestinationMigration <- as_numeric(WFP_BFA$DestinationMigration)
WFP_BFA$DestinationMigration <- 
  labelled::labelled(
    WFP_BFA$DestinationMigration,
    c(`Ville/Capitale` = 1,
      `Un autre pays d’Afrique` = 2,
      `Hors Afrique` = 3))
expss::val_lab(WFP_BFA$DestinationMigration)
```

```
##          Ville/Capitale Un autre pays d’Afrique            Hors Afrique 
##                       1                       2                       3
```

```r
# DureeMigration
WFP_BFA$DureeMigration <- as_numeric(WFP_BFA$DureeMigration)
WFP_BFA$DureeMigration <- 
  labelled::labelled(
    WFP_BFA$DureeMigration,
    c(`Moins d’un mois ` = 1,
      `1 à 3 mois` = 2,
      `3 à 6 mois` = 3,
      `6 à 9 mois` = 4,
      `10 à 12 mois` = 5,
      `Plus de 12 mois` = 6))
expss::val_lab(WFP_BFA$DureeMigration)
```

```
## Moins d’un mois        1 à 3 mois       3 à 6 mois       6 à 9 mois 
##                1                2                3                4 
##     10 à 12 mois  Plus de 12 mois 
##                5                6
```

```r
# TendanceMigration
WFP_BFA$TendanceMigration <- as_numeric(WFP_BFA$TendanceMigration)
WFP_BFA$TendanceMigration <- 
  labelled::labelled(
    WFP_BFA$TendanceMigration,
    c(`Beaucoup augmenté` = 1,
      `Légèrement augmenté` = 2,
      `Stable` = 3,
      `Beaucoup baissé` = 4,
      `Légèrement baissé` = 5,
      `Ne sait pas` = 6))
expss::val_lab(WFP_BFA$TendanceMigration)
```

```
##   Beaucoup augmenté Légèrement augmenté              Stable     Beaucoup baissé 
##                   1                   2                   3                   4 
##   Légèrement baissé         Ne sait pas 
##                   5                   6
```

```r
#RaisonHausseMig
WFP_BFA$RaisonHausseMig <- as_numeric(WFP_BFA$RaisonHausseMig)
WFP_BFA$RaisonHausseMig <- 
  labelled::labelled(
    WFP_BFA$RaisonHausseMig,
    c(
      `Difficultés alimentaires conjoncturelles` = 1,
      `Manque d’opportunités économiques` = 2,
      `Dégradation de l’environnement (pertes de bétail, baisse de la 
       production et du rendement à cause de la sécheresse, et des faibles 
       précipitations, etc.)` = 3,
      `La migration fait désormais partie des moyens d’existence classique`
      = 4, 
      `Autres à préciser` = 5 
    ))
expss::val_lab(WFP_BFA$RaisonHausseMig)
```

```
##                                                                                                                                   Difficultés alimentaires conjoncturelles 
##                                                                                                                                                                          1 
##                                                                                                                                          Manque d’opportunités économiques 
##                                                                                                                                                                          2 
## Dégradation de l’environnement (pertes de bétail, baisse de la \n       production et du rendement à cause de la sécheresse, et des faibles \n       précipitations, etc.) 
##                                                                                                                                                                          3 
##                                                                                                        La migration fait désormais partie des moyens d’existence classique 
##                                                                                                                                                                          4 
##                                                                                                                                                          Autres à préciser 
##                                                                                                                                                                          5
```

```r
#RaisonBaisseMig
WFP_BFA$RaisonBaisseMig <- as_numeric(WFP_BFA$RaisonBaisseMig)
WFP_BFA$RaisonBaisseMig <- 
  labelled::labelled(
    WFP_BFA$RaisonBaisseMig,
    c(
      `Moins d’opportunités économiques ou insécurité au Nigéria ou en 
      Lybie` = 1,
      `Voyage vers la Lybie/ Nigeria devenu trop dangereux/ couteux` = 2,
      `Les ménages pauvres ont accès à une assistance régulière/ les bras 
      valides sont occupés par les travaux FFA` = 3,
      `La situation alimentaire générale du village s’est améliorée` = 4,
      `La migration fait désormais partie des moyens d’existence classique`
      = 5,
      `Emergence d’opportunités économiques grâce aux actifs 
      créés/réhabilités` = 6,
      `Autres à préciser` = 7 
    ))
expss::val_lab(WFP_BFA$RaisonBaisseMig)
```

```
##                                       Moins d’opportunités économiques ou insécurité au Nigéria ou en \n      Lybie 
##                                                                                                                   1 
##                                                        Voyage vers la Lybie/ Nigeria devenu trop dangereux/ couteux 
##                                                                                                                   2 
## Les ménages pauvres ont accès à une assistance régulière/ les bras \n      valides sont occupés par les travaux FFA 
##                                                                                                                   3 
##                                                        La situation alimentaire générale du village s’est améliorée 
##                                                                                                                   4 
##                                                 La migration fait désormais partie des moyens d’existence classique 
##                                                                                                                   5 
##                                     Emergence d’opportunités économiques grâce aux actifs \n      créés/réhabilités 
##                                                                                                                   6 
##                                                                                                   Autres à préciser 
##                                                                                                                   7
```
 
# Social capital index (Indice de capital social)


```r
#SCIAideIntraCom
WFP_BFA$SCIAideIntraCom <- as_numeric(WFP_BFA$SCIAideIntraCom)
WFP_BFA$SCIAideIntraCom <- 
  labelled::labelled(
    WFP_BFA$SCIAideIntraCom,
    c(
      `Parents` = 1,
      `Les personnes non apparentées de mon groupe ethnique/clan` = 2,
      `Non parents dans un autre groupe ethnique/clan` = 3,
      `Personne` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 888 , 
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIAideIntraCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                          Autre (précisez) 
##                                                         5 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
#SCIAideDehorsCom
WFP_BFA$SCIAideDehorsCom <- as_numeric(WFP_BFA$SCIAideDehorsCom)
WFP_BFA$SCIAideDehorsCom <- 
  labelled::labelled(
    WFP_BFA$SCIAideDehorsCom,
    c(
      `Parents` = 1,
      `Les personnes non apparentées de mon groupe ethnique/clan` = 2,
      `Non parents dans un autre groupe ethnique/clan` = 3,
      `Personne` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 888 , 
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIAideDehorsCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                          Autre (précisez) 
##                                                         5 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
#SCIEvolRessSociales
WFP_BFA$SCIEvolRessSociales <- as_numeric(WFP_BFA$SCIEvolRessSociales)
WFP_BFA$SCIEvolRessSociales <- 
  labelled::labelled(
    WFP_BFA$SCIEvolRessSociales,
    c(
      `Augmenté` = 1,
      `Est resté le même` = 2,
      ` A diminué` = 3,
      `Ne sait pas` = 8 , 
      `Refuse de répondre` = 9
    ))
expss::val_lab(WFP_BFA$SCIEvolRessSociales)
```

```
##           Augmenté  Est resté le même          A diminué        Ne sait pas 
##                  1                  2                  3                  8 
## Refuse de répondre 
##                  9
```

```r
#SCIPersAAiderCom
WFP_BFA$SCIPersAAiderCom <- as_numeric(WFP_BFA$SCIPersAAiderCom)
WFP_BFA$SCIPersAAiderCom <- 
  labelled::labelled(
    WFP_BFA$SCIPersAAiderCom,
    c(
      `Parents` = 1,
      `Les personnes non apparentées de mon groupe ethnique/clan` = 2,
      `Non parents dans un autre groupe ethnique/clan` = 3,
      `Personne` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 888 , 
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIPersAAiderCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                          Autre (précisez) 
##                                                         5 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
#SCIPersAAiderEnDehorsCom
WFP_BFA$SCIPersAAiderEnDehorsCom <- as_numeric(WFP_BFA$SCIPersAAiderEnDehorsCom)
WFP_BFA$SCIPersAAiderEnDehorsCom <- 
  labelled::labelled(
    WFP_BFA$SCIPersAAiderEnDehorsCom,
    c(
      `Parents` = 1,
      `Les personnes non apparentées de mon groupe ethnique/clan` = 2,
      `Non parents dans un autre groupe ethnique/clan` = 3,
      `Personne` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 888 , 
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIPersAAiderEnDehorsCom)
```

```
##                                                   Parents 
##                                                         1 
## Les personnes non apparentées de mon groupe ethnique/clan 
##                                                         2 
##            Non parents dans un autre groupe ethnique/clan 
##                                                         3 
##                                                  Personne 
##                                                         4 
##                                          Autre (précisez) 
##                                                         5 
##                                               Ne sait pas 
##                                                       888 
##                                        Refuse de répondre 
##                                                      8888
```

```r
#SCIConMembreGvrnmt
WFP_BFA$SCIConMembreGvrnmt <- as_numeric(WFP_BFA$SCIConMembreGvrnmt)
WFP_BFA$SCIConMembreGvrnmt <- 
  labelled::labelled(
    WFP_BFA$SCIConMembreGvrnmt,
    c(
      `Oui` = 1,
      `Non` = 0,
      `Ne sait pas` = 888 , 
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIConMembreGvrnmt)
```

```
##                Oui                Non        Ne sait pas Refuse de répondre 
##                  1                  0                888               8888
```

```r
#SCIPersConMembreGvrnmt
WFP_BFA$SCIPersConMembreGvrnmt <- as_numeric(WFP_BFA$SCIPersConMembreGvrnmt)
WFP_BFA$SCIPersConMembreGvrnmt <- 
  labelled::labelled(
    WFP_BFA$SCIPersConMembreGvrnmt,
    c(
      `Un membre de la famille ou un parent` = 1,
      `Ami(e)` = 2,
      `Voisin` = 3 , 
      `Connaissance (membre d'un groupe, ami d'un ami, etc.)` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 8,
      `Refuse de répondre` = 9
    ))
expss::val_lab(WFP_BFA$SCIPersConMembreGvrnmt)
```

```
##                  Un membre de la famille ou un parent 
##                                                     1 
##                                                Ami(e) 
##                                                     2 
##                                                Voisin 
##                                                     3 
## Connaissance (membre d'un groupe, ami d'un ami, etc.) 
##                                                     4 
##                                      Autre (précisez) 
##                                                     5 
##                                           Ne sait pas 
##                                                     8 
##                                    Refuse de répondre 
##                                                     9
```

```r
#SCICapAideGvnmt
WFP_BFA$SCICapAideGvnmt <- as_numeric(WFP_BFA$SCICapAideGvnmt)
WFP_BFA$SCICapAideGvnmt <- 
  labelled::labelled(
    WFP_BFA$SCICapAideGvnmt,
    c(
      `Oui` = 1,
      `Non` = 0,
      `Ne sait pas` = 888,
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCICapAideGvnmt)
```

```
##                Oui                Non        Ne sait pas Refuse de répondre 
##                  1                  0                888               8888
```

```r
#SCIConMembreNGO
WFP_BFA$SCIConMembreNGO <- as_numeric(WFP_BFA$SCIConMembreNGO)
WFP_BFA$SCIConMembreNGO <- 
  labelled::labelled(
    WFP_BFA$SCIConMembreNGO,
    c(
      `Oui` = 1,
      `Non` = 0,
      `Ne sait pas` = 888,
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIConMembreNGO)
```

```
##                Oui                Non        Ne sait pas Refuse de répondre 
##                  1                  0                888               8888
```

```r
#SCIPersConMembreNGO
WFP_BFA$SCIPersConMembreNGO <- as_numeric(WFP_BFA$SCIPersConMembreNGO)
WFP_BFA$SCIPersConMembreNGO <- 
  labelled::labelled(
    WFP_BFA$SCIPersConMembreNGO,
    c(
      `Un membre de la famille ou un parent` = 1,
      `Ami(e)` = 2,
      `Voisin` = 3 , 
      `Connaissance (membre d'un groupe, ami d'un ami, etc.)` = 4,
      `Autre (précisez)` = 5,
      `Ne sait pas` = 8,
      `Refuse de répondre` = 9
    ))
expss::val_lab(WFP_BFA$SCIPersConMembreNGO)
```

```
##                  Un membre de la famille ou un parent 
##                                                     1 
##                                                Ami(e) 
##                                                     2 
##                                                Voisin 
##                                                     3 
## Connaissance (membre d'un groupe, ami d'un ami, etc.) 
##                                                     4 
##                                      Autre (précisez) 
##                                                     5 
##                                           Ne sait pas 
##                                                     8 
##                                    Refuse de répondre 
##                                                     9
```

```r
#SCIAideAubesoin
WFP_BFA$SCIAideAubesoin <- as_numeric(WFP_BFA$SCIAideAubesoin)
WFP_BFA$SCIAideAubesoin <- 
  labelled::labelled(
    WFP_BFA$SCIAideAubesoin,
    c(
      `Oui` = 1,
      `Non` = 0,
      `Ne sait pas` = 888,
      `Refuse de répondre` = 8888
    ))
expss::val_lab(WFP_BFA$SCIAideAubesoin)
```

```
##                Oui                Non        Ne sait pas Refuse de répondre 
##                  1                  0                888               8888
```
  
  
# ABISexparticipant


```r
WFP_BFA$ABISexparticipant <-as.numeric(WFP_BFA$ABISexparticipant)
WFP_BFA$ABISexparticipant <- labelled::labelled(WFP_BFA$ABISexparticipant,c(`Homme` = 1, `Femme` = 0))
expss::val_lab(WFP_BFA$ABISexparticipant)
```

```
## Homme Femme 
##     1     0
```

```r
WFP_BFA %>% 
  plot_frq(coord.flip =T,ABISexparticipant, show.na = T)
```

![](01_BFA_LabelsHarmonization_files/figure-html/unnamed-chunk-21-1.png)<!-- -->
# HHHMainActivity

```r
WFP_BFA$HHHMainActivity <- as_factor(WFP_BFA$HHHMainActivity)
WFP_BFA$HHHMainActivity <- labelled::labelled(WFP_BFA$HHHMainActivity, c(Salarié = 1, `Agriculteur` = 2, `Eleveur` = 3, `Ouvrier journalier` = 4, `Commerce` = 5, `Ménagère` = 6, `Marabout` = 7, `Artisanat` = 8, `Chasse/Peche` = 9, `Recolte bois/Paille` = 10, `Retraité` = 11, `Sans emploi` = 12, `Autre à préciser` = 13 ))
```

# Actifcreesrehabi

```r
Actifcreesrehabi_var <- c("Actifcreesrehabi_1", "Actifcreesrehabi_2", "Actifcreesrehabi_3")
WFP_BFA <- WFP_BFA %>% mutate(across(Actifcreesrehabi_var, as.numeric))
WFP_BFA <- WFP_BFA %>% 
  dplyr::mutate(across(Actifcreesrehabi_var,
                       ~labelled(., labels = c(
                         "Non" = 0,
                         "Oui" = 1
                       )
                       )))
expss::val_lab(WFP_BFA$Actifcreesrehabi_1)
```

```
## Non Oui 
##   0   1
```


```r
WFP_BFA.sub<- WFP_BFA  %>% dplyr::select(ID,adm0_ocha,ADMIN0Name,adm1_ocha,ADMIN1Name,adm2_ocha,ADMIN2Name,SURVEY,YEAR,SvyDatePDM,HHHSex ,HHHAge, HHHEdu,everything())

WFP_BFA <- copy_labels(WFP_BFA.sub, WFP_BFA)
```


```r
HHvar <- c("HHSize","HHSize05M","HHSize23M","HHSize59M","HHSize5114M","HHSize1549M","HHSize5064M","HHSize65AboveM","HHSize05F","HHSize23F","HHSize59F","HHSize5114F","HHSize1549F","HHSize5064F","HHSize65AboveF")
WFP_BFA <- WFP_BFA %>% mutate(across(HHvar, as.numeric))
```


# Cleaning dirty variables


## drop variables not needed


```r
var_to_drop = c("RESPConsent",
                "ADMIN3Name",
                "RESPAge",
                "RESPSex",
                "RelationWith_HHH",
                "MAD_module",
                "HHHMainActivity",
                #"HHHMatrimonial",
                "HHSourceIncome"
)
WFP_BFA <- WFP_BFA  %>% dplyr::select(-var_to_drop)
```

## Remove empty rows and/or columns



## Remove constant columns


#Labélisation


```r
var_label(WFP_BFA$ID) <- "Identifiant de l'enquêté"
var_label(WFP_BFA$adm1_ocha) <- "Admin 1 ID"
var_label(WFP_BFA$ADMIN1Name) <- "Decoupage administrative 1"
var_label(WFP_BFA$ADMIN2Name) <- "Decoupage administrative 2"
var_label(WFP_BFA$adm2_ocha) <- "Admin 2 ID"
var_label(WFP_BFA$SURVEY) <- "Type d'enquête"
var_label(WFP_BFA$YEAR) <- "Année de l'enquête"
var_label(WFP_BFA$SvyDatePDM) <- "Date de l’Interview"
var_label(WFP_BFA$HHHSex) <- "Sexe du chef du ménage"
var_label(WFP_BFA$HHHAge) <- "Age du chef du ménage"
var_label(WFP_BFA$HHHEdu) <- "Niveau d'éducation atteint par le chef de ménage"
var_label(WFP_BFA$Longitude) <- "Longitude"
var_label(WFP_BFA$Latitude) <- "Latitude"
#var_label(WFP_BFA$HHHMainActivity) <- "Activité principale"
var_label(WFP_BFA$HHHMatrimonial) <- "Situation matrimoniale du chef de ménage"
var_label(WFP_BFA$HHHMatrimonial) <- "Situation matrimoniale"
var_label(WFP_BFA$HHSize) <- "Taille du ménage"
var_label(WFP_BFA$HHSize05M) <- "Nombre de filles de 0 à 5 mois"
var_label(WFP_BFA$HHSize23M) <- "Nombre de filles de 6 à 23 mois"
var_label(WFP_BFA$HHSize59M) <- "Nombre de filles de 24 à 59 mois"
var_label(WFP_BFA$HHSize5114M) <- "Nombre de filles de 5 à 14 ans mois"
var_label(WFP_BFA$HHSize1549M) <- "Nombre de filles de 15 à 49 ans mois"
var_label(WFP_BFA$HHSize5064M) <- "Nombre de filles de 50 à 64 ans mois"
var_label(WFP_BFA$HHSize65AboveM) <- "Nombre de filles de 65 ans ou plus"
var_label(WFP_BFA$HHSize05F) <- "Nombre de filles de 0 à 5 mois"
var_label(WFP_BFA$HHSize23F) <- "Nombre de filles de 6 à 23 mois"
var_label(WFP_BFA$HHSize59F) <- "Nombre de filles de 24 à 59 mois"
var_label(WFP_BFA$HHSize5114F) <- "Nombre de filles de 5 à 14 ans mois"
var_label(WFP_BFA$HHSize1549F) <- "Nombre de filles de 15 à 49 ans mois"
var_label(WFP_BFA$HHSize5064F) <- "Nombre de filles de 50 à 64 ans mois"
var_label(WFP_BFA$HHSize65AboveF) <- "Nombre de filles de 65 ans ou plus"
var_label(WFP_BFA$FCSStap) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des céréales et tubercules"
var_label(WFP_BFA$FCSStapSRf) <- "la source principale des céréales et tubercules au cours des 7 derniers jours"
var_label(WFP_BFA$FCSPulse) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Légumineuses"
var_label(WFP_BFA$FCSPulseSRf) <- "la source principale des Légumineuses au cours des 7 derniers jours"
var_label(WFP_BFA$FCSDairy) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé/bu du Lait et produits laitiers"
var_label(WFP_BFA$FCSDairySRf) <- "la source principale du lait et des produits laitiers au cours des 7 derniers jours"
var_label(WFP_BFA$FCSPr) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé de la Viande, poisson et œufs"
var_label(WFP_BFA$FCSPrSRf) <- "la source principale de la viande, poisson, œufs au cours des 7 derniers jours"
var_label(WFP_BFA$FCSPrMeatF) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé de la Chair/viande rouge"
var_label(WFP_BFA$FCSPrMeatO) <- "la source principale de la Viande d'organe au cours des 7 derniers jours"
var_label(WFP_BFA$FCSPrFish) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé du Poissons et coquillage"
var_label(WFP_BFA$FCSPrEgg) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Oeufs"
var_label(WFP_BFA$FCSVeg) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Légumes et feuilles"
var_label(WFP_BFA$FCSVegSRf) <- "la source principale des Légumes et feuilles au cours des 7 derniers jours"
var_label(WFP_BFA$FCSVegOrg) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Légumes oranges (légumes riches en Vitamine A)"
var_label(WFP_BFA$FCSVegGre) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Légumes à feuilles vertes"
var_label(WFP_BFA$FCSFruit) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Fruits"
var_label(WFP_BFA$FCSFruitSRf) <- "la source principale des fruits au cours des 7 derniers jours"
var_label(WFP_BFA$FCSFruitOrg) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Fruits oranges (Fruits riches en Vitamine A)"
var_label(WFP_BFA$FCSFat) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé des Huiles et graisses"
var_label(WFP_BFA$FCSFatSRf) <- "la source principale des Huiles et graisses au cours des 7 derniers jours"
var_label(WFP_BFA$FCSSugar) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé/buvé du sucre ou sucreries"
var_label(WFP_BFA$FCSSugarSRf) <- "la source principale du sucre ou sucreries au cours des 7 derniers jours"
var_label(WFP_BFA$FCSCond) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage ont mangé/buvé des condiments/épices"
var_label(WFP_BFA$FCSCondSRf) <- "la source principale des condiments/épices au cours des 7 derniers jours"
var_label(WFP_BFA$DebutAssistance) <- "Depuis quand le ménage est-il bénéficiaire de l’assistance FFA/CFA du PAM ?"
var_label(WFP_BFA$DateDerniereAssist) <- "Dernière assistance reçue du PAM "
var_label(WFP_BFA$TransfBenef) <- "Le ménage, ou un membre de votre ménage, a-t-il bénéficié au cours des 12 derniers mois de ..."
var_label(WFP_BFA$BanqueCerealiere) <- "Banque céréalière"
var_label(WFP_BFA$VivreContreTravail) <- "Vivre contre travail/ Food assistance for asset"
var_label(WFP_BFA$ArgentContreTravail) <- "Argent contre travail/ Cash assistance for asset"
var_label(WFP_BFA$DistribVivresSoudure) <- "Distribution gratuite de vivres (p. ex. pendant la période de soudure)"
var_label(WFP_BFA$DistribArgentSoudure) <- "Distribution gratuite d’argent (p.ex. pendant la période de soudure)"
var_label(WFP_BFA$BoursesAdo) <- "Bourses scolaires pour adolescentes" 
var_label(WFP_BFA$BlanketFeedingChildren) <- "Blanket feeding - NSPAMM (enfants 6 -23 mois)"
var_label(WFP_BFA$BlanketFeedingWomen) <- "Blanket feeding-NSPAMM (Femmes enceintes et allaitantes)"
var_label(WFP_BFA$ArgentetVivreContreTravail) <- "Argent vivre contre travail/ Cash assistance for asset"
var_label(WFP_BFA$MASChildren) <- "Prise en charge malnutrition aigüe sévère des enfants de 6 à 59 mois au niveau du centre de santé"
var_label(WFP_BFA$MAMChildren) <- "Prise en charge malnutrition aigüe modérée des enfants de 6 à 59 mois au niveau du centre de santé" 
var_label(WFP_BFA$MAMPLWomen) <- "Prise en charge malnutrition aigüe femme enceinte ou allaitante au niveau du centre de santé"
var_label(WFP_BFA$FARNcommunaut) <- "FARN/ nutrition communautaire"
var_label(WFP_BFA$FormationRenfCapacite) <- "Formation/renforcement de capacités"
var_label(WFP_BFA$CashTransfert) <- "Cash transfert (filets sociaux ou autres structures)"
var_label(WFP_BFA$CantineScolaire) <- "Cantine scolaire pour les enfants ou take home ration" 
var_label(WFP_BFA$AutreTransferts) <- "Autres à préciser"
var_label(WFP_BFA$ExistGroupeEpargne) <- "Groupe d'épargne et de crédit ou une tontine"
var_label(WFP_BFA$MembreGroupeEpargne) <- "Est-ce que vous ou un autre membre du ménage êtes membre de ce groupe ?"
var_label(WFP_BFA$EpargneAvantPam) <- "Participation à une tontine ou un groupe d‘épargne et de crédit avant d’être bénéficiaires du PAM"
var_label(WFP_BFA$EpargneSansPam) <- "Participation à cette tontine ou groupe d’épargne et de crédit en l'absence de l’assistance du PAM"
var_label(WFP_BFA$PossibilitePret) <- "Possibilité d’avoir un prêt à partir de la tontine ou du groupe d’épargne et de crédit en cas de besoin d'argent"
var_label(WFP_BFA$AutreSourcePret) <- "Possibilité d’avoir un prêt à partir d’une autre source en cas de besoin d'argent"
var_label(WFP_BFA$EpargnePieds) <- "Bétail acheté pour la vente de vos récoltes qui peut servir cas difficultés économiques ou financières"
var_label(WFP_BFA$SERSRebondir) <- "Votre ménage peut rebondir à tout défi d’ordre climatique, économique ou lié aux troubles sociopolitiques que la vie pourrait lui lancer"
var_label(WFP_BFA$SERSRevenue) <- "S’il est affecté par un problème d’ordre climatique, économique ou lié aux troubles sociopolitiques, Votre ménage pourra changer ou adapter sa source de revenu primaire pour faire face aux difficultés que les autres membres de votre communauté"
var_label(WFP_BFA$SERSMoyen) <- "Si les menaces d’ordre climatique, économique ou lié aux troubles sociopolitiques pesant sur votre ménage devenaient plus fréquentes et intenses, vous trouveriez toujours un moyen de  s’en sortir"
var_label(WFP_BFA$SERSDifficultes) <- "Votre ménage pourrait accéder facilement à l’appui financier dont il aurait besoin s’il est affecté par un problème d’ordre climatique, économique ou lié aux troubles sociopolitiques, qui lui causerait des difficultés"
var_label(WFP_BFA$SERSSurvivre) <- "Votre ménage peut s'offrir tout ce dont il a besoin pour survivre et prospérer"
var_label(WFP_BFA$SERSFamAmis) <- "En cas de besoins essentiels non satisfaits en raison d'événements/chocs/stress (climatiques OU économiques OU conflits OU autres), votre ménage peut compter sur le soutien de la famille et des amis."
var_label(WFP_BFA$SERSPoliticiens) <- "En cas de besoins essentiels non satisfaits en raison d'événements/chocs/stress (climatiques OU économiques OU conflits OU autres), votre ménage peut compter sur le soutien de l'administration publique/gouvernementale ou d'autres institutions."
var_label(WFP_BFA$SERSLecons) <- "Votre ménage a tiré des leçons importantes des difficultés passées causées par des événements/chocs/stress (climatiques OU économiques OU conflits OU autres) qui vous aident à mieux vous préparer à des menaces similaires dans un avenir proche."
var_label(WFP_BFA$SERSPreparerFuture) <- "Votre ménage est entièrement préparé à tout événement/choc/stress futur (climatique OU économique OU conflit OU autre) qui pourrait se produire dans votre région."
var_label(WFP_BFA$SERSAvertissementEven) <- "Votre ménage reçoit à l'avance des informations l'avertissant de la variabilité future (climatique OU économique OU conflit OU autre) et des risques météorologiques qui l'aident à se préparer et à se protéger des chocs/stress futurs."
var_label(WFP_BFA$ABIParticipation) <- "Vous ou un membre du ménage a-t-il participé aux activités de création d’actifs ?"
var_label(WFP_BFA$ABItransferts) <- "Vous ou un membre du ménage a-t-il reçu un transfert d’une aide alimentaire ?"
var_label(WFP_BFA$Actifcreesrehabi) <- "Ouvrages créés/réhabilité dans la communauté par le programme de résilience"
var_label(WFP_BFA$Actifcreesrehabi_1) <- "Récupération de terres en Demi-lune, banquette, zaï, cordons pierreux, tranchée de reboisement"
var_label(WFP_BFA$Actifcreesrehabi_2) <- "Fixation des dunes"
var_label(WFP_BFA$Actifcreesrehabi_3) <- "Aménagement de mare (surcreusement, faucardage etc.)"
var_label(WFP_BFA$Actifcreesrehabi_other) <- "Autres"
var_label(WFP_BFA$ABISexparticipant) <- "Sexe du participant aux activités de création d’actifs"
var_label(WFP_BFA$ABIProteger) <- "Pensez-vous que les actifs qui ont été créés ou réhabilités dans votre communauté sont de nature à protéger votre ménage, ses biens et ses capacités de production (champs, équipement, etc.) contre les inondations / sécheresse / catastrophes ?"
var_label(WFP_BFA$ABIProduction) <- "Pensez-vous que les actifs qui ont été créés ou réhabilités dans votre communauté ont permis à votre ménage d’augmenter ou de diversifier sa production (agriculture / élevage / autre) ?"
var_label(WFP_BFA$ABIdifficultes) <- "Pensez-vous que les actifs qui ont été créés ou réhabilités dans votre communauté ont diminué les difficultés quotidiennes, réduire la charge et la durée des travaux domestiques : (le temps pour la collecte de l'eau/bois de chauffe, les travaux de puisage d’eau des femmes, préparation de nourriture) ?"
var_label(WFP_BFA$ABIMarches) <- "Pensez-vous que les actifs qui ont été créés ou réhabilités dans votre communauté ont amélioré la capacité des membres de votre ménage à l’accès aux marchés et/ou aux services de base (eau, assainissement, santé, éducation, etc.) ?"
var_label(WFP_BFA$ABIGererActifs) <- "Pensez-vous que les formations et autres formes de soutien dispensés dans votre communauté ont amélioré la capacité de votre ménage pour gérer et maintenir les actifs ?"
var_label(WFP_BFA$ABIEnvironnement) <- "Pensez-vous que les actifs qui ont été construits ou réhabilités dans votre communauté ont amélioré votre environnement naturel (par exemple plus couverture végétale, nappe phréatique augmenté, moins d’érosion, etc.) ?"
var_label(WFP_BFA$ABIutiliseractifs) <- "Pensez-vous que les travaux réalisés dans votre communauté ont restauré votre capacité à accéder et/ou utiliser les actifs ?"
var_label(WFP_BFA$ABITensions) <- "Pensez-vous que les actifs créés/réhabilités ont aidé réduire les tensions au sein sur l'accès et l'utilisation des ressources naturelles dans votre communauté ?"
var_label(WFP_BFA$ActifCreationEmploi) <- "Pensez-vous que les actifs réhabilité/créé ont généré des opportunités d’emploi dans votre communauté ?"
var_label(WFP_BFA$BeneficieEmploi) <- "Est-ce que vous ou un membre de votre ménage a une fois eu la possibilité de travailler grâce aux actifs créés ou réhabilités dans votre communauté ?"
var_label(WFP_BFA$TRavailMaintienActif) <- "Avez-vous ou un membre de votre ménage eu du travail dans le maintien et la gestion des actifs créés ou réhabilités dans votre communauté ?"
var_label(WFP_BFA$MigrationEmploi) <- "Nombre de personnes du ménage ayant migré à la recherche d’un emploi au cours des 12 derniers mois"
var_label(WFP_BFA$NbMigrants) <- "Nombre de personnes du ménage ayant migré ou allé en exode pendant les 12 derniers mois"
var_label(WFP_BFA$RaisonMigration) <- "Principale raison qui a motivé certains membres du ménage à migrer ou à aller en exode"
var_label(WFP_BFA$AutreRaisonEconomiques) <- "Si vous vous déplacez pour la Recherche d’opportunités économiques, quelles sont ces raisons ?"
var_label(WFP_BFA$RaisonAccesServices) <- "Si vous vous déplacez pour accéder à des services de base, quels sont ces services ?"
var_label(WFP_BFA$DestinationMigration) <- "Destinations des migrants membre du ménage ?"
var_label(WFP_BFA$DureeMigration) <- "Nombre de mois d'absence, en moyenne, dans l’année des migrants saisonniers du ménage  ?"
var_label(WFP_BFA$TendanceMigration) <- "Comment évaluez-vous la tendance à la migration chez les membres de votre ménage ?"
var_label(WFP_BFA$RaisonHausseMig) <- "Si la tendance est à la hausse, quelle en est la principale raison ?"
var_label(WFP_BFA$RaisonBaisseMig) <- "Si la tendance est à la baisse, quelle en est la principale raison ?"
var_label(WFP_BFA$SCIAideIntraCom) <- "Si votre ménage avait un problème et avait besoin d'une aide urgente (par exemple, de la nourriture, de l'argent, de la main-d'œuvre, du transport, etc.), à qui, DANS CETTE COMMUNAUTÉ, pourriez-vous demander de l'aide ?"
var_label(WFP_BFA$SCIAideDehorsCom) <- "Si votre ménage avait un problème et avait besoin d'une aide urgente (par exemple, de la nourriture, de l'argent, du travail, du transport, etc.), vers qui, en DEHORS DE CE VILLAGE, pourriez-vous vous tourner pour obtenir de l'aide ?"
var_label(WFP_BFA$SCIEvolRessSociales) <- "Par rapport à il y a un an, est-ce que votre capacité à obtenir de l'aide de quelqu'un à l'intérieur ou à l'extérieur de votre village : a) a été améliorée ? ou en dehors de votre village"
var_label(WFP_BFA$SCIPersAAiderCom) <- "Qui, DANS CETTE COMMUNAUTÉ, pourriez-vous aider s'ils avaient besoin d'une aide urgente (par ex. nourriture, argent, travail, transport, etc.) (lisez la liste ; sélectionnez toutes les réponses qui s'appliquent) ?"
var_label(WFP_BFA$SCIPersAAiderEnDehorsCom) <- "Qui, EN DEHORS DE CETTE COMMUNAUTÉ, pourriez-vous aider s'il avait besoin d'une aide urgente (par exemple de la nourriture, de l'argent, du travail, du transport, etc.) (lisez la liste ; sélectionnez toutes les réponses qui s'appliquent) ?"
var_label(WFP_BFA$SCIConMembreGvrnmt) <- "Est-ce que vous ou quelqu'un d'autre dans votre foyer connaît personnellement un élu du gouvernement ?"
var_label(WFP_BFA$SCIPersConMembreGvrnmt) <- "Comment vous (ou un autre membre du foyer) connaissez-vous ce représentant du gouvernement ? Est-il ou est-elle un(e)... (lisez la liste ; sélectionnez toutes les réponses qui s'appliquent) ?"
var_label(WFP_BFA$SCICapAideGvnmt) <- "Pourriez-vous demander au fonctionnaire d'aider votre famille ou votre communauté si une aide était nécessaire ?"
var_label(WFP_BFA$SCIConMembreNGO) <- "Est-ce que vous ou quelqu'un d'autre dans votre foyer connaît personnellement un membre du personnel d'une ONG [OU d'une organisation communautaire, d'une agence des Nations Unies, de la Croix Rouge/Croissant Rouge...] ?"
var_label(WFP_BFA$SCIPersConMembreNGO) <- "Comment connaissez-vous (ou un autre membre du ménage) le membre du personnel de l'[AGENCE] ? Est-il ou est-elle un(e)... ?"
var_label(WFP_BFA$SCIAideAubesoin) <- "Pourriez-vous demander au membre du personnel de [l'AGENCE] d'aider votre famille ou votre communauté si de l'aide était nécessaire ?"
var_label(WFP_BFA$MDDW_resp_age) <- "Âge en années révolues de la femme"
var_label(WFP_BFA$PWMDDWStapCer) <- "Tous les aliments à base de céréales, comme : Mil/sorgho, riz, maïs, pâtes alimentaires (macaronis), couscous, pain, céréales frits, millet etc. ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWStapRoo) <- "Toutes les racines et tubercules blancs ou plantains, tels que : Patate douce à chair blanche, pomme de terre, igname, taros, manioc (gari, tapioca), banane plantain, arbre à pain ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWPulse) <- "Tous les haricots, niébés ou les pois, tels que : Haricots (niébé), petits pois, pois chiches, lentilles, autres légumes secs, autres haricots ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWNuts) <- "Des noix ou des graines, comme : Fruit secs, arachide (en pâte ou autre), soja, noix de cajou, noix sauvages, graines de palme ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWDairy) <- "Tout lait ou produit laitier, tel que : Lait frais, lait en poudre, lait concentré (sucré ou non), yaourt, fromage, crème fraîche, Lait fermenté ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWPrMeatO) <- "Toute viande à base d'organes d'animaux, comme : Foie (veau, mouton, chèvre, volailles,), abats pleins (cœur, reins, rate, poumon), boudin noir, œuf de poisson ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWPrMeatF) <- "Viandes et volailles : Bœuf, mouton, chèvre, porc (y compris charcuterie), langue, lapin, viande de brousse, Poulet, pintades, dindon, caille, pigeon, chien, chat, singe ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWPrFish) <- "Tout poisson ou fruit de mer, qu'il soit frais ou séché : Poisson frais, poisson fumé, salé, séché (sauf pincée de poudre), conserves (sardines, thon.), tous fruits de mer, crabes, crevettes fraiches, fumées ou séchées ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWPrEgg) <- "Les œufs : Œufs de poule, pintade, caille, de canard, de dinde, … ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWVegGre) <- "Tous les légumes à feuilles vert foncé, tels que : Oseille, amarante, salade, feuilles de baobab, corète potagère, épinards, feuilles d’oignon, de haricot, de manioc, de patates douces, de carottes, etc. + toutes feuilles sauvages ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWVegOrg) <- "Tous les légumes ou racines qui sont de couleur orange à l'intérieur, comme : Courge, carotte, poivron rouge, patate douce à chair orange ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWVegOth) <- "Tout autre légume : Tomates (sauf concentré), gombo frais, aubergines, concombres, choux, navets, oignons, poivrons verts, haricots verts… ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PWMDDWFruitOrg)	<- "Tous les fruits qui sont jaune foncé ou orange à l'intérieur, comme :	Mangue, papaye, melon, orange" 
var_label(WFP_BFA$PWMDDWFruitOth)	<- "Tout autre fruit :	Ananas, banane, goyave, dattes, pastèque, canne à sucre, pomme cannelle, orange, citron, jus de fruits frais (fruits pressés sans conservateurs), raisins, fruits sauvages (tamarin, ...), fruit de baobab "
var_label(WFP_BFA$PWMDDWSnf) <- "Super-céréales ou autres produits fortifiés : Super-Cereal or Plumpy Sup et autres SNF distribues par le PAM"
var_label(WFP_BFA$PWMDDWCond) <- "Tous les condiments et assaisonnements, tels que : Concentré de tomates, piment, poudre de poisson, sel, cube Maggi"
var_label(WFP_BFA$PWMDDWOth1) <- "Toute autre boisson et tout autre aliment: Café ou thé non sucré, Bouillon clair, alcool, Cornichon, olive et produits similaires"
var_label(WFP_BFA$PWMDDWInsects) <- "Insectes, larves et larves d'insectes, œufs d'insectes et escargots terrestres et marins"
var_label(WFP_BFA$PWMDDWFatRpalm) <- "Huile de palme rouge"
var_label(WFP_BFA$PWMDDWFatOth) <- "Huile ; graisses ou beurre ajoutés aux aliments ou utilisés pour la cuisson, y compris les huiles extraites des noix, des fruits et des graines ; et toutes les graisses animales"
var_label(WFP_BFA$PWMDDWSnack) <- "Chips et frites, pâte frite ou autres snacks frits"
var_label(WFP_BFA$PWMDDWSugarFood) <- "Les aliments sucrés, comme les chocolats, les bonbons, les biscuits et les gâteaux, les pâtisseries sucrées ou les glaces"
var_label(WFP_BFA$PWMDDWSugarBev) <- "Jus de fruits sucrés et 'boissons au jus', boissons gazeuses, boissons chocolatées, boissons au malt, boissons au yaourt ou thé ou café sucré avec du sucre"
var_label(WFP_BFA$MAD_dob) <-"Date de naissance de (MAD_name)"
var_label(WFP_BFA$MAD_sex) <- "Sexe de l'enfant de (MAD_name)"
var_label(WFP_BFA$MAD_resp_age) <- "Âge en mois de (MAD_name)"
var_label(WFP_BFA$EverBreastF) <- "Est-ce que l’enfant n’a jamais été nourri(e) au sein ?"
var_label(WFP_BFA$PCIYCBreastF) <- "Parfois les enfants sont nourris au lait maternel par d’autres moyens (cuillère, tasse, biberon) ; parfois une autre femme allaite l’enfant. Est-ce que l’enfant a été nourri(e) au lait maternel hier par l’une ou l’autre de ces méthodes dans la journée ou dans la nuit ?"
var_label(WFP_BFA$PCIYCInfFormNb) <- "Combien de fois au cours de la journée ou de la nuit (MAD_name) a-t-il consommé une formule infantile"
var_label(WFP_BFA$PCIYCDairyMiNb) <- "Combien de fois au cours de la journée ou de la nuit (MAD_name) a-t-il consommé du lait (en poudre, lait frais d’animaux, autre)"
var_label(WFP_BFA$PCIYCDairyYoNb) <- "Combien de fois au cours de la journée ou de la nuit (MAD_name) a-t-il consommé Yaourt, lait caillé"
var_label(WFP_BFA$PCIYCStapPoNb) <- "Combien de fois au cours de la journée ou de la nuit (MAD_name) a-t-il consommé uen préparation pour bébé – type bouillie légère"
var_label(WFP_BFA$PCMADStapCer) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, de la bouillie (mil, riz,..), pain, riz, tô, couscous ou d’autres aliments à base de céréales ?"
var_label(WFP_BFA$PCMADVegOrg) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison du potiron, carottes, courges, patates douces à chair jaune ou orange ?"
var_label(WFP_BFA$PCMADStapRoo) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison des ommes de terre à chair blanches, igname, manioc blanc, manioc, ou d’autres aliments à base de racines ou tubercules ?"
var_label(WFP_BFA$PCMADVegGre) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des légumes à feuilles vertes foncées ?"
var_label(WFP_BFA$PCMADFruitOrg) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des fruits à couleur orange (mangues, papayes etc.) ?"
var_label(WFP_BFA$PCMADVegFruitOth) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des autres fruits et légumes : oignon, tomates, concombre, haricot vert, petit pois, banane, pomme, citron, mandarine, orange, goyave etc ?"
var_label(WFP_BFA$PCMADPrMeatO) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, du foie, rognon, cœur et/ou autres abats rouges ?"
var_label(WFP_BFA$PCMADPrMeatF) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, de la viande : chèvres, moutons, agneau, bœuf, poulet, chameaux ?"
var_label(WFP_BFA$PCMADPrEgg) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des Œufs ?"
var_label(WFP_BFA$PCMADPrFish) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, du poisson frais ou séché, fruits de mer, coquillages, crustacés ?"
var_label(WFP_BFA$PCMADPulse) <- "Plats ou aliments contenant des haricots, pois, lentilles, noix ou graines ajouter / remplacer des exemples basés sur le pays/la région"
var_label(WFP_BFA$PCMADDairy) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, du fromage, yahourt, lait ou autres produits laitiers ?"
var_label(WFP_BFA$PCMADFatRpalm) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des aliments à base d’huile de palme rouge, noix de palme rouge ou pulpe de noix de palme rouge ?"
var_label(WFP_BFA$PCMADSnfChild) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, des aliments fortifiés ?"
var_label(WFP_BFA$PCMADSnfPowd) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, de la poudre de micronutriments ?"
var_label(WFP_BFA$PCMADSnfLns) <- "(MAD_name) a t-il mangé hier au cours de la journée ou de la nuit, que ce soit à la maison ou à l’extérieur de la maison, une formule enrichie pour enfants ?"
var_label(WFP_BFA$PCIYCMeals) <- "Combien de fois l’enfant a consommé des aliments solides, semi-solides ou mous hier, pendant la journée ou la nuit ?"
label(WFP_BFA$rCSILessQlty) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage dû consommer des aliments moins préférés et moins chers parce qu'ils n'avaient pas assez de nourriture ou de l'argent pour acheter de la nourriture"
label(WFP_BFA$rCSIBorrow) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage dû emprunter de la nourriture ou compter sur l’aide des parents/amis parce qu'ils n'avaient pas assez de nourriture ou de l'argent pour acheter de la nourriture"
label(WFP_BFA$rCSIMealSize) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage dû diminuer la quantité consommée pendant les repas parce qu'ils n'avaient pas assez de nourriture ou de l'argent pour acheter de la nourriture"
label(WFP_BFA$rCSIMealAdult) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage dû restreindre la consommation des adultes pour nourrir les enfants parce qu'ils n'avaient pas assez de nourriture ou de l'argent pour acheter de la nourriture"
label(WFP_BFA$rCSIMealNb) <- "Nombre de de jours, au cours des 7 derniers jours, lesquels les membres du ménage dû diminuer le nombre de repas par jour parce qu'ils n'avaient pas assez de nourriture ou de l'argent pour acheter de la nourriture"
label(WFP_BFA$LhCSIStress1) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû vendre des actifs/biens non productifs du ménage (radio, meuble, réfrigérateur, télévision, bijoux, etc.) en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSIStress2) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû vendre plus d’animaux (non-productifs) que d’habitude en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSIStress3) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû dépenser l’épargne en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSIStress4) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû emprunter de l’argent / nourriture auprès d’un prêteur formel / banque en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSICrisis1) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû réduire les dépenses non alimentaires essentielles telles que l’éducation, la santé (dont de médicaments) en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSICrisis2) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû vendre des biens productifs ou des moyens de transport (machine à coudre, brouette, vélo, car, etc.) en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSICrisis3) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû retirer les enfants de l’école en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
label(WFP_BFA$LhCSIEmergency1) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû vendre la maison ou des terrains en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"

label(WFP_BFA$LhCSIEmergency2) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû mendier en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"

label(WFP_BFA$LhCSIEmergency3) <- "Au cours des 30 derniers jours, est-ce qu’un membre de votre ménage a dû vendre les derniers animaux femelles reproductrices en raison d'un manque de nourriture ou d'argent pour acheter de la nourriture ?"
```


# Data exportation 

## Variables labels







```r
#FP_BFA <- labelled::to_factor(WFP_BFA)
```


```r
FP_BFA <-WFP_BFA
colonnes_caracteres <- sapply(FP_BFA, function(x) !is.numeric(x))
FP_BFA[colonnes_caracteres] <- lapply(FP_BFA[colonnes_caracteres], to_factor)
haven::write_dta(FP_BFA,"WFP_BFA.dta")
```



```r
#devtools::install_github("pcctc/croquet")
library(croquet)
library(openxlsx)

wb <- createWorkbook()
add_labelled_sheet(FP_BFA)
saveWorkbook(wb, "WFP_BFA.xlsx",overwrite = TRUE)
```




<!-- ```{r remove final environment variables} -->
<!-- rm(list = ls()) -->
<!-- ``` -->

