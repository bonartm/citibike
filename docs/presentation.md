---
author: Malte Bonart
title: Citibike Classification Challenge
date: October 16, 2019
header-includes:
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css" />
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="www/funs.js"></script> 
---

---

<div class="smallfont">
<p>This work and the underlying source code is available on <a href="https://github.com/bonartm/citibike"> <i class="fab fa-github-square"></i>GitHub</a>.</p>
 
<p>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.</p>

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />
</div>

### moderately imbalanced data

&nbsp; | Day Pass/ Three Day Pass | Annual Membership
:---| :---: | :---:
<i class="fas fa-user"></i> | *Customer (11%)* | *Subscriber (89%)*
<i class="fas fa-dollar-sign"></i> | 12.00$ / day | 169.00$ / year
<i class="fas fa-clock"></i> | max 30 min | max 45 min
<i class="fas fa-plus"></i> | 4.00$ / 15 min | 2.50$ / 15 min


### customers bike for a longer period

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/tripduration.html" height="450" width="100%"></iframe>

<div class="smallfont">
Trips with a duration > 2 hours and < 20 seconds have been removed from the analysis (~0.3%). Customer ride on average
1441, Subscribers 721 seconds.
</div>

### {data-background-iframe="figures/map.html"}

### anomaly in the *age distribution* for customers

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/age.html" height="450" width="100%"></iframe>

<div class="smallfont">
6% of all trips from *customers* have an age value of 49.
</div>

### *gender* is mostly unknown for customers

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/gender.html" height="500" width="100%"></iframe>

### more customers on the weekend

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/weekday.html" height="450" width="100%"></iframe>


<div class="smallfont">
0:Sunday - 6:Saturday.
</div>

### more clients during summer *months*

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/month.html" height="500" width="100%"></iframe>

### more subscribers during rush *hour*

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/hour.html" height="500" width="100%"></iframe>




### model features

- tripduration
- starttime, stoptime
- hour, weekday, month
- start (lat,lon), end (lat,lon)
- age, close_to_fifty
- gender
- NYC neighbourhoods (via <i class="fab fa-google"></i> geocoding API)

### the baseline performs well - nearest neighbour classifier is worse

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/results.html" height="350" width="100%"></iframe>

<div class="smallfont">
The baseline was constructed by classifying all trips with `unknown` gender as `customers`. Nearest neighbour classification is based on `time`, `start location`, `end location` and `tripduration`.
</div>

### classification does **not** outperform baseline

<div class="smalltable">
features | dimensions | logistic regression (f-score)
:---| :---: | :---: 
tripduration | 1 | 0.15
+ gender | 3 | 0.70
+ age | 5 | 0.71
+ time | 45 | 0.71
+ area | 173 | 0.72
</div>


<div class="smallfont">
The training is based on a random sample of n=5000000 trips, due to ressource and time constraints.
</div>

### *random forrest* does not improve the classification

<iframe scrolling="no" style="border:none;" seamless="seamless" data-src="figures/results_classification.html" height="450" width="100%"></iframe>

### comparisson of trip duration with biking

*biking vs.* | driving | driving (traffic) | transit
:---| --- | --- | --- | ---
Average differences |  <i class="fas fa-arrow-circle-down"></i> -107 | <i class="fas fa-arrow-circle-down"></i> -105 | <i class="fas fa-arrow-circle-up"></i> 209
Median differences | <i class="fas fa-arrow-circle-right"></i> 2 | <i class="fas fa-arrow-circle-right"></i> -9 | <i class="fas fa-arrow-circle-up"></i> 263
Biking faster | <i class="fas fa-arrow-circle-right"></i> 50% | <i class="fas fa-arrow-circle-right"></i> 48% | <i class="fas fa-arrow-circle-up"></i> 83%

<div class="smallfont">
Based on a n=2000 random sample of trips, collected with the GoogleMaps Directions API. Wilcoxon signed-rank test and t-test for pairs are both significant.
<i class="fas fa-arrow-circle-up"></i> biking faster | <i class="fas fa-arrow-circle-down"></i> biking slower
</div>
