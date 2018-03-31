---
layout: "post"
title: "How I start a bioinformatics project"
subtitle: "or: Where are my files???"
date: 2018-03-26 10:00:00 +0100
categories: "blog"
image: "/img/new_project.png"
tags: [RMarkdown, projectTemplate, sequencing, organization]
comments: "true"
show-share: "true"
show-subscribe: "true"
categories: "new_project"
description: "A simple guide for newbies in sequencing or general bioinformatics to do reproducible research"
sitemap: 
  lastmod: 2017-08-18
  priority: 1
  changefreq: 'monthly'
---

I started analyzing sequencing data just over one year ago. In the beginning it was so exciting to finally receive the first reads, do some quality checks and start further analysis, that I didn´t think about reproducibility. I ended up with multiple distinct versions of mapped reads, adapter/quality trimmed reads from scripts using different parameters. **It was bad...** <i class="em em-anguished"></i>   
So I had to force myself to rethink my workflow, which I will show you (*in a simplifed way*) in the following.  

<h2>My personal workflow</h2>  
Of course I`m not the first one who had this problem and if you are new to *bioinformatics* and *sequencing* you will probably encounter similar difficulties when starting your analysis. There are probably many ways you can achieve a certain level of organization without the need for any advanced technique, like <a target="_blank" href="https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control">version control</a>. Sooner or later you´ll get there automatically. Trust me.   
Here, I will show you how to organize yourself using <a target = "_blank" href="https://www.rstudio.com">RStudio</a>.   
First, open a new window and create a new project.  
<br>
<div>
  <img src="/img/new_project_rproject1.png" style="width: 31%;"/>
  <img src="/img/new_project_rproject2.png" style="width: 31%;"/>
  <img src="/img/new_project_rproject3.png" style="width: 31%;"/>
</div>
<br>
Within the new RStudio window switch to the embedded **terminal** (new feature since version 1.1). If you are not sure about the version you are actually using you can check this with typing ```RStudio.Version()``` in the RStudio **console**.  
Since you are already in your new project folder, we can start be making folders for your analysis.  

``` bash
# in RStudio terminal
project_folder=${PWD}
mkdir -p ${project_folder}/{data,scripts,results,doc}    
```



A bit more complicated :
Using Rmarkdown and Rproject package


data_folder=$project_folder"/data"
mkdir -p $data_folder/{test_data,raw_data,clean_data,genome_data,mapping_data,qc_data}           
mkdir -p $data_folder"/mapping_data/"{star,segemehl}
mkdir -p $data_folder"/genome_data/"{star,segemehl}


``` r
# in R
install.packages("ProjectTemplate")
library("ProjectTemplate")
create.project("../test_project", merge.strategy = "allow.non.conflict")
setwd("/Users/f/Documents/R/test_project")
library('ProjectTemplate')
load.project()
```


paper published in PLOS computationsl biology
<a target="_blank" href="http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424">




veriosn control



<link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">
