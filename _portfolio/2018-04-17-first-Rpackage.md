---
title: "Write your first R package"
collection: portfolio
permalink: /portfolio/2018-04-17-first-Rpackage
last_modified_at: 2018-04-17
tags: [RPackage,roxygen2,RStudio,devtools]
comments: true
read_time: true
---

In my opinion **packages** are one of the main reasons why `R` is so successfull. They add a whole new level of functionality and reproducibility and also increase the productivity of every user by reusable R functions, their documentation and sample data.  

<h2> When and how shoud I use packages? </h2>  
The workflow behind finding and using new packages is almost too natural to write about, but here is how I do it:  
<br>
<ul>
  <li>Step 1: I have a problem in `R`, which I can´t solve in 10 seconds</li>
  <li>Step 2: I google if there is already a solution to this problem</li>
  <li>Step 3: In ~99 % there is actually a package dealing with this problem</li>
  <li>Step 4: I look at the documentation</li>
  <li>Step 5: I download the package</li>
  <li>Step 6: I use it on my own data</li>  
  <li>Step 7: Problem solved!</li>
</ul>

As you can see there is no way to avoid packages and no reason to.   
**But have you ever written your own package?**  
I am just curious. Because until recently I myself actually did not. It came up to my mind when I was working on quality control plots of Nanopore sequencing data, where I had some functions written, but I had to reload them every single time before using. I was so sick of it. And that´s why I decided to package the functions.  
In this post I do not want to show you my NanoporeQC package (*I will cover this topic in a future post*), but simply share my thoughts in writing your first **R package** with a very easy (and useless) example.  
A warning: It will not be perfect, but hey what is perfect anyway? And you have to start somewhere. For those interested, I highly recommend this awesome <a target= "_blank" href="http://r-pkgs.had.co.nz">book</a> by Hadley Wickham.  
Let´s get started:  

<h2> Example task </h2>  
Imagine there are no arithmetic functions in `R`. We want to write our own `sum` function that takes a vector of numbers as input and simply sums them up.     

```r
# set seed
set.seed(seed = 1)

# generate example data
example_numbers <- sample(x = 10,size = 10, replace = T)

# take a quick glance at the example numbers generated
example_numbers
```
> 3  4  6 10  3  9 10  7  7  1  

```r
# usual way to sum up numbers in R
sum(example_numbers)
```
> 60  

```r
# own function to sum up numeric values
sum_numbers <- function(input_data){
  sum <- 0
  for(i in 1:(length(input_data))){
    sum <- sum + input_data[i]
  }
  return(sum)
}

# with own function
sum_numbers(example_numbers)
```
> 60  

<br>
We want to use this pretty useful function over and over again, without reloading it from source every single time. You could also think about using more arithmetic functionalities like `mean`, `median` or `prod`, which would make re-loading even more complicated. If there only was a simple workflow for building a package?!... (*I know these functions already exist, let´s just pretend..*)

<h2> How to package it? </h2>  
Open a new project in RStudio with *project type* `R package` (with the option to create a git repository). Automatically a few files are generated: *DESCRIPTION*, *NAMESPACE* and two folders *man* and *R*. You can check out all of these files in my <a target="_blank" href="https://github.com/felixgrunberger/sumR">github repository</a> so you know what I am talking about.  
Witout proper documentation, users won´t know how to use our package and you probably want to make life easier not only for yourself. The goal of <a href="https://cran.r-project.org/web/packages/roxygen2/vignettes/roxygen2.html" target="_blank">roxygen2</a> is to make documentation as simple as possible.  
First, you have to create the `R` file containing the function `sum_numbers` we wrote in the upper part. The `.R` file in the **R** folder should look something like this:  

```r
#!/usr/bin/Rscript

# sumR version 1.0
# Copyright (C) 2018 Felix Grünberger
#
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# supress warnings
options(warn=-1)

#' sums up a vector of numeric data
#' Takes in a vector of numeric data and sums them up
#' @param input_data vector of numeric data
#' @return sum of numeric data
#' @export
sum_numbers <- function(input_data){
  sum <- 0
  for(i in 1:(length(input_data))){
    sum <- sum + input_data[i]
  }
  return(sum)
}
```
<br>
Lines starting with `#'` are roxygen comments to the source files. Full documentation can be found <a target="_blank" href="https://cran.r-project.org/web/packages/roxygen2/vignettes/rd.html">here</a>.  
Second, you have to run `roxygen::roxygenize()` to convert roxygen comments to *.Rd* files.  
You should also edit the *DESCRIPTION* file which could look something like this:  
```r
Package: sumR
Type: Package
Title: Write the basic arithmetic function `sum` for yourself
Version: 1.0.0
Author: Felix Grünberger
Maintainer: The package maintainer <yourself@somewhere.net>
Description: More about what it does (maybe more than one line)
    Use four spaces when indenting paragraphs within the Description.
License: What license is it under?
Encoding: UTF-8
LazyData: true
RoxygenNote: 6.0.1
```
<br>
Once you´re done, check the functions in the upper right **Build** corner of RStudio. Then you can go on by pushing it to github.  

<h2> Push to github </h2>  
Create a new repository in github.    
<br>
<div>
  <img src="/images/package_github.png" style="width: 100%;"/>
</div>
<br>

Clone your github repository and add all the existing files from the package. (Some help <a target="_blank" href="https://help.github.com/articles/cloning-a-repository/">here</a>)
```r
# clone you repository (be sure the package files you created are in this folder)
git clone https://github.com/felixgrunberger/sumR

# Stage the file for commit to your local repository.
git add .

# Commit the file that you've staged in your local repository.
git commit -m "Add sumR files"

# Push the changes in your local repository to GitHub.
git push origin master
```

<h2> Use your package</h2>  
Packages from your github repository can be used with  
```r
library(devtools)
devtools::install_github("felixgrunberger/sumR")

# example from the beginning
set.seed(seed = 1)
example_numbers <- sample(x = 10,size = 10, replace = T)
example_numbers
```
>  3  4  6 10  3  9 10  7  7  1  

```r
sumR::sum_numbers(example_numbers)
```
> 60    

<br>
And that´s it!  
I started my first package by copying an existing one from github, modifying the functions, adding comments and adding it to my own github. Maybe some of you can also follow this workflow and then dig deeper into making packages with R!

