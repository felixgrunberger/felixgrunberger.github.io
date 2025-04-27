---
title: "The power of interactive plots"
subtitle: "Learn about interactive visualizations with R and plotly"
collection: portfolio
permalink: /portfolio/2017-08-18-animated-bargraph
last_modified_at: 2017-08-18
tags: [ggplot2,plotly]
comments: true
read_time: true
---

At the beginning of the year, I remember myself staring at the screen, sitting on a bunch of genomic data and thinking:
<br> "Man, it would be really helpful to hover over my data points and check what properties they have..."
<br> As this may seem a bit nerdy, nowadays dynamic content has become quite natural and offers a whole new range of possibilities especially when dealing with large, complex data sets.

<h2>
(Sometimes) Do not be static!
</h2>
Don´t get me wrong. Static graphics can be great and are inevitable for print media.  
And as long as you are working on two-dimensional data, it is not a problem at all and in fact more or less the only reasonable option you have.
But, imagine adding another layer of information. And another one. And so on... (I think you get the point here)  
Unfortunately, our imagination is not made for multi-dimensional data. How is it possible to include all of the additional information in your plot?
In this case, it is common practice to use different colors, sizes, transparencies, shapes or to split up your plot.  
However, building a meaningful and informative static plot from multi-dimensional data can be quite hard. Why not consider how to make graphics interactive and benefit from all the clicking and zooming we are used to?  
Actually, it is not that hard using <a target="_blank" href="https://www.r-project.org">R</a> and the <a target="_blank" href="https://plot.ly/r/">Plotly R library</a>. This package is built upon the amazing <a target="_blank" href="https://d3js.org">D3.js</a>, which requires at least some skills in HTML, CSS and JavaScript. Therefore, <strong>Plotly</strong> brings major benefits, because it is easy to use and compatible with a number of languages (R, Python, MATLAB..).  
I will try to convince you, that interactive visualization can make a huge difference during exploratory data analysis. <br> <br>
<h2>
Example data set: Most profitable movies of all time
</h2>
For the first analysis steps of the movie data set from <a target="_blank" href="https://www.kaggle.com">KAGGLE</a>, please go back to <a target="_blank" href = "https://felixgrunberger.com/2017-08-02-use_R/">my last article</a>.

``` r
# 1. step: Load all packages we need ----------------------------------------------------------------------------

library(dplyr)
library(ggplot2)
library(plotly)
library(viridis)
library(gganimate)
library(webshot)
```

``` r
# 2. step: Load data (CSV file) from KAGGLE ---------------------------------------------------------------------

movie_file <- path_to_file            # download first then specify absolute or relative filepath in "/.../.."
imdb_data <- read.csv(movie_file)     # base function of R to read a CommaSeparatedFile
```

<br> What is the most profitable movie of all time? Plot budget on the x-axis and profit on the y-axis, colored by release-year of the movie. <br>

``` r
# 3. step: Calculate profit and plot movies ---------------------------------------------------------------------

gg_profit <- imdb_data %>%
  mutate(profit = gross - budget) %>%
  arrange(desc(profit)) %>%
  top_n(3500, profit) %>%
  ggplot(aes(x = budget/1000000, y = profit/1000000,
             col = title_year,
             text = sprintf("%s<br>%s", movie_title, title_year))) +  # text will be displayed in plotly
    geom_point(size = 5, alpha = 0.3) +
    theme_minimal() +
    scale_color_gradientn(colours = rev(viridis_pal(option = "viridis")(40))) +
    labs(x = "budget (MIO $)", y = "profit (MIO $)") +
    guides(col=guide_legend(title="Year")) +
    ggtitle("3500 most profitable movies")

print(gg_profit)
```

<img src="/images/dotplot.png" style="display: block; margin: auto;" /> <br> <br> Can you guess what this highest point on the x-axis is representing?
As we are already plotting three-dimensional data (profit, budget, year), the best thing we can do is to make the plot interactive. <br>

``` r
# 4. step: Let´s make it interactive ----------------------------------------------------------------------------

ggplotly(gg_profit, tooltip = "text")           # yes, that´s all you need!
```
<br> <br>
<div>
    <a href="https://plot.ly/~FelixGrunberger/35/?share_key=TgU9Hbh1SMkZ30ZB7D4WFZ" target="_blank" title="plotly_movies" style="display: block; text-align: center;"><img src="https://plot.ly/~FelixGrunberger/35.png?share_key=TgU9Hbh1SMkZ30ZB7D4WFZ" alt="plotly_movies" style="max-width: 100%;width: 800px;"  width="800" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="FelixGrunberger:35" sharekey-plotly="TgU9Hbh1SMkZ30ZB7D4WFZ" src="https://plot.ly/embed.js" async></script>
</div>


 <br> <br> That was easy. When you hover over the data points you can read every single movie title (Best way to experience interactivity is of course not on your smartphone). <br> If you even want to go one step further, you can add an animation slider, to split up your movie data set. <br>

``` r
# Alternative: Interactive & dynamic plot using plotly?  --------------------------------------------------------

gg_profit_dynamic <- imdb_data %>%
  mutate(profit = gross - budget) %>%
  arrange(desc(profit)) %>%
  top_n(3500, profit) %>% 
  ggplot(aes(x = budget/1000000, y = profit/1000000,
             text = sprintf("%s<br>%s", movie_title, title_year),
             frame = title_year)) +         # add a frame; everything else stays the same
    geom_point(size = 5, alpha = 0.5, color = "lightblue") +
    theme_minimal() +
    labs(x = "budget (MIO $)", y = "profit (MIO $)") +
    guides(col=guide_legend(title="Year")) +
    ggtitle("3500 most profitable movies")


ggplotly(gg_profit_dynamic, tooltip = "text") %>%
  animation_opts(
    frame = 100, transition = 0, easing = "elastic", redraw = FALSE
  ) %>%
  animation_slider(
    currentvalue = list(prefix = "YEAR ")
  )
```
<br> <br>
<div>
    <a href="https://plot.ly/~FelixGrunberger/37/?share_key=jCTGskexxAN217YQcoPojW" target="_blank" title="plotly_movies_animated" style="display: block; text-align: center;"><img src="https://plot.ly/~FelixGrunberger/37.png?share_key=jCTGskexxAN217YQcoPojW" alt="plotly_movies_animated" style="max-width: 100%;width: 800px;"  width="800" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="FelixGrunberger:37" sharekey-plotly="jCTGskexxAN217YQcoPojW" src="https://plot.ly/embed.js" async></script>
</div>
<br>

<br> <br>
<h2>
Takeaway: Make use of those two extra lines
</h2>
Why is it not more common to use interactive graphs?  
Probably because we have never learned how to do it, programming seems to be hard and eventually they cannot be used for publishing or printing.  
But as the way we are communicating is changing, I am sure that the proportion of interactive graphics will also change dramatically. So, if you are already using R and ggplot graphics package for exploratory data analysis, keep in mind:  
You will only need to add <strong>two extra lines of code</strong> to make your graphics interactive.
<br> <br> <br> <br>
<h3>
Learn Plotly or read some more about visualization?
</h3>
<div id="aboutme-section">
<p class="about-text">
<span class="fa fa-code about-icon"></span> Find examples on how to make any kind of plot with the <a target="_blank" href="https://plot.ly/r/">Plotly R library</a>. 
</p>
<p class="about-text">
<span class="fa fa-link about-icon"></span> Read about why nobody is using interactive infographics <a target="_blank" href="https://medium.com/@dominikus/the-end-of-interactive-visualizations-52c585dcafcb">here</a>. 
</p>



<br> <br> <br><br> <br> <br>
