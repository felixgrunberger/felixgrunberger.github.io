---
title: "How I start a bioinformatics project"
description: "A simple guide for newbies in sequencing or general bioinformatics to do reproducible research"
collection: portfolio
permalink: /portfolio/2018-04-01-new-project
last_modified_at: 2018-04-01
tags: [RMarkdown,projectTemplate,sequencing,organization]
comments: true
read_time: true
---


I started analyzing sequencing data just over one year ago. In the beginning it was so exciting to finally receive the first reads, do some quality checks and start further analysis, that I didn´t think about reproducibility. I ended up with multiple distinct versions of mapped reads, adapter/quality trimmed reads from scripts using different parameters. **It was bad...** <i class="em em-anguished"></i>   
So I had to force myself to rethink my workflow, which I will show you (*in a simplifed way*) in the following.  

<h2>My personal workflow</h2>  
Of course I`m not the first one who had this problem and if you are new to *bioinformatics* and *sequencing* you will probably encounter similar difficulties when starting your analysis. There are probably many ways you can achieve a certain level of organization without the need for any advanced technique, like <a target="_blank" href="https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control">version control</a>. Sooner or later you´ll get there automatically. Trust me.   
Here, I will show you how to organize yourself using <a target = "_blank" href="https://www.rstudio.com">RStudio</a>.   
First, open a new window and create a new project.  
<br>
<div>
  <img src="/images/new_project_rproject1.png" style="width: 31%;"/>
  <img src="/images/new_project_rproject2.png" style="width: 31%;"/>
  <img src="/images/new_project_rproject3.png" style="width: 31%;"/>
</div>
<br>
Within the new RStudio window switch to the embedded **terminal** (new feature since version 1.1). If you are not sure about the version you are actually using you can check this with typing ```RStudio.Version()``` in the RStudio **console**.  
Since you are already in your new project folder, we can start be making **4** folders for your analysis.  

``` bash
# in RStudio terminal
project_folder=${PWD}
mkdir -p ${project_folder}/{data,scripts,results,doc}    
```
<br>  
Once you have done that, simply save your input sequencing data in ```data``` and so on. For example you can put genome annotation data you use for your analysis in ```data/genome_data```.  
Since you´re already in RStudio it is quite easy to open an *RMarkdown* document to keep track of your code and also thoughts about the different steps (```doc```). The remaining two folder ```scripts``` and ```results``` are self-explanatory, but important for your organization so that input files do not get mixed up with annotation or any other results files of a following step.   

<h2>Using Rmarkdown and Rproject package</h2>   
Actually there is an Rpackage called <a target="_blank" href ="http://projecttemplate.net/getting_started.html">```ProjectTemplate```</a> that is perfectly suited to start any data analysis project. In case you do not want to read full documentation here is how you get started:  

``` r
# in R
install.packages("ProjectTemplate")
library("ProjectTemplate")
create.project("../test_project", merge.strategy = "allow.non.conflict")
setwd("~/test_project")
library('ProjectTemplate')
load.project()
```

<h2> Key message</h2>  
I keep it simple: Make folders or you get lost...  
In case you want to get more information you can start by reading a <a target="_blank" href="http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424">paper published in PLOS computationsl biology</a>. Feel free to comment on my workflow.  



<link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">

