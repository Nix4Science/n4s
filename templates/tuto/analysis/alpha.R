library(tidyverse)

args = commandArgs(trailingOnly=TRUE)
n = length(args)
files = args[1:(n-1)]
outfile = args[n]


plot <- files %>%
    map_df(function(x) read_csv(x, col_names=T)) %>%
    mutate(alpha = alpha * 180 / pi) %>%
    filter(v0 == 1 & planet == "earth") %>%
    ggplot(aes(x = x, y = y, color = factor(alpha))) +
    geom_point() +
    xlab("x(t)") +
    ylab("y(t)") +
    scale_color_discrete("Initial Angle (degree)") +
    ggtitle("Trajectory through time") +
    theme_bw() +
    theme(legend.position = "bottom")
ggsave(plot = plot, outfile)

