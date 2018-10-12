# Bin Packing Problem

This repository contains python implemented solutions to approximate solutions to the traditional 
bin packing problem.

## Problem Overview

Different variations of the traditional bin packing problem are adressed in this repository.

The traditional bin packing problem seeks to sort a predetermined number of items of different sizes 
(weights) into a minimal number of bins. Each bin has the same has a cutoff of how much total weight 
can be stored in the bin. For the sake of simplicity, this code assumes this cutoff is the same for 
all bins. This problem is solved by the BinPacking.py file.

The variation of this problem addressed by the genetic algorithm is similar in nature: one is
looking to pack the bins as efficiently as possible; however, the number of bins to use is 
predetermined and there is no cap on the bins. Instead, in this variation, one is looking to 
minimize the weight of the heaviest bin (i.e. pack the bins in such a way that their total weights
are as similar as possible. 