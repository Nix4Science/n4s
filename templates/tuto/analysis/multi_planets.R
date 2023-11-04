library(tidyverse)

args = commandArgs(trailingOnly=TRUE)
n = length(args)
files = args[1:(n-1)]
outfile = args[n]


plot <- files %>%
    map_df(function(x) read_csv(x, col_names=T)) %>%
    mutate(alpha = alpha * 180 / pi) %>%
    filter(v0 == 1 & alpha == 45) %>%
    ggplot(aes(x = x, y = y, color = factor(planet))) +
    geom_point() +
    xlab("x(t)") +
    ylab("y(t)") +
    scale_color_discrete("Planet") +
    ggtitle("Trajectory through time") +
    theme_bw() +
    theme(legend.position = "bottom")
ggsave(plot = plot, outfile)

