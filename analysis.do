local data `"**omitted here**"'
local direc `"**omitted here**"'

insheet using `"`data'"', clear
set more off

sort numthread rtime
replace rtime = rtime/60

drop if stime >16


by numthread: egen min_rtime = min(rtime)
by numthread: egen max_rtime = max(rtime)
by numthread: egen min_stime = min(stime)
by numthread: egen max_stime = max(stime)
by numthread: egen avg_stime = mean(stime)

egen max_rtime_tag = tag(numthread max_rtime)
egen avg_stime_tag = tag(numthread avg_stime)


graph twoway scatter max_rtime numthread if (max_rtime_tag == 1), ///
title("Time taken to finish scraping") ///
ytitle("Time taken to finish" "(minutes, rtime for last scrape to finish)") ///
xtitle("Threadcount") ///
ylabel(0(30)150)
graph export `"`direc'/finish.pdf"', replace

graph close _all


graph twoway scatter avg_stime numthread if (avg_stime_tag == 1), ///
title("Average scrape time per query") ///
ytitle("Seconds") ///
xtitle("Threadcount")
graph export `"`direc'/average.pdf"', replace

graph close _all


forvalues i = 1(2)17 {
sum stime if numthread == `i'
}



gen rounded_stime = round(stime, 0.001)

forvalues i = 1(2)17 {
graph twoway histogram rounded_stime if numthread == `i', fraction ///
title("Threadcount = `i'") ///
ytitle("") ///
xtitle("time (seconds)") ///
ylabel(0(0.05)0.25) ///
yscale(range(0,0.25)) ///
name(tc`i', replace)
}
graph combine tc1 tc3 tc5 tc7 tc9 tc11 tc13 tc15 tc17, ///
graphregion(fcolor(white)) cols(3)
graph export `"`direc'/histogram.pdf"', replace

graph close _all


