library(tidyverse)

args = commandArgs(trailingOnly=TRUE)
n = length(args)
files = args[1:(n-1)]
outfile = args[n]

files %>%
    map_df(function(x) read_csv(x, col_names=T)) %>%
    write_csv(path=outfile)
