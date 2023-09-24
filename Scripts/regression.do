import delimited using "D:\Aalto University\B.Sc Econ - Immigration & Public Transportation\Immigrant Pattern & Public Transport Accessibility\Data\extrapolated.csv", clear

encode id, gen(district_id)
xtset district_id year

* Create a binary variable for original data years
gen original_data = (year == 2013 | year == 2015 | year == 2018)

* Focus only on main CBD / Helsinki City Centre (both simple and log)
xtreg non_official_lang_percentage v20, fe
xtreg non_official_lang_percentage v20 if original_data == 1, fe
xtreg non_official_lang_percentage v20, fe vce(robust)
xtreg non_official_lang_percentage v20 if original_data == 1, fe vce(robust)

gen log_main = log(v20 + 1)
xtreg non_official_lang_percentage log_main, fe
xtreg non_official_lang_percentage log_main if original_data == 1, fe
xtreg non_official_lang_percentage log_main, fe vce(robust)
xtreg non_official_lang_percentage log_main if original_data == 1, fe vce(cluster district_id)

* Focus only on time_to_fastest_cbd (both simple and log)
xtreg non_official_lang_percentage time_to_fastest_cbd, fe
xtreg non_official_lang_percentage time_to_fastest_cbd if original_data == 1, fe
xtreg non_official_lang_percentage time_to_fastest_cbd, fe vce(robust)
xtreg non_official_lang_percentage time_to_fastest_cbd if original_data == 1, fe vce(robust)
xtreg non_official_lang_percentage time_to_fastest_cbd, fe vce(cluster district_id)
xtreg non_official_lang_percentage time_to_fastest_cbd if original_data == 1, fe vce(cluster district_id)

gen log_fastest = log(time_to_fastest_cbd + 1)
xtreg non_official_lang_percentage log_fastest, fe
xtreg non_official_lang_percentage log_fastest if original_data == 1, fe
xtreg non_official_lang_percentage log_fastest, fe vce(robust)
xtreg non_official_lang_percentage log_fastest if original_data == 1, fe vce(robust)
xtreg non_official_lang_percentage log_fastest, fe vce(cluster district_id)
xtreg non_official_lang_percentage log_fastest if original_data == 1, fe vce(cluster district_id)

* Multiple regression with all CBDs
xtreg non_official_lang_percentage v9-v23, fe vce(cluster district_id)
xtreg non_official_lang_percentage v9-v23 if original_data == 1, fe vce(cluster district_id)
xtreg non_official_lang_percentage v9-v23, fe vce(robust)
xtreg non_official_lang_percentage v9-v23 if original_data == 1, fe vce(robust)

* Log transformation of all travel times
foreach var of varlist v9-v23 {
    gen log_`var' = log(`var' + 1)
}
xtreg non_official_lang_percentage log_v9-log_v23, fe
xtreg non_official_lang_percentage log_v9-log_v23 if original_data == 1, fe
xtreg non_official_lang_percentage log_v9-log_v23, fe vce(robust)
xtreg non_official_lang_percentage log_v9-log_v23 if original_data == 1, fe vce(cluster district_id)