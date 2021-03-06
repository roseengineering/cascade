
Cascade
-------
Software utility to manipulate touchstone s-parameter files.

Features
--------
The utility takes a touchstone file as standard input
and outputs a new touchstone file (or other formats)
to standard output.  Cascade provides the following
input transformations as command line options:

```
-cascade             : cascade together the two networks on top of stack
-deembed             : de-embed the top two networks on the stack
-swap                : swap the top two networks on the stack

-cbg                 : transform top network into a common-base arrangement
-ccd                 : transform top network into a common-collector arrangement
-unilateral          : match top network and isolate its input and output
-lift <el>           : lift top network from ground and insert a Z/inductor/capacitor element
-series <el>         : cascade top network with a series Z/inductor/capacitor element
-shunt <el>          : cascade top network with a shunt Z/inductor/capacitor element
-short <complex>     : cascade top network with a short shunt stub 
-open <complex>      : cascade top network with an open shunt stub 
-tline <complex>     : cascade top network with a transmission line
-flip                : flip top network, swapping S11 with S22 and S21 with S12

-gs <complex>        : set the source gamma for matching
-zs <complex>        : set the source impedance for matching
-gl <complex>        : set the load gamma for matching
-zl <complex>        : set the load impedance for matching

-pass                : push a pass-through network onto stack
-block               : push an isolation network onto stack
-copy                : push a copy of top network onto stack
-f <filename>        : push a touchstone file onto stack
```

Complex numbers can also be entered in 'polar' notation.  Use a '/' to separate the magnitude and 
angle in degrees, for example '10/90'.  

Transmission lines are given in complex form, with the magnitude setting the impedance and the angle 
setting the length.  Open or shunt stubs are given the same way.
A component element can be entered as an impedance using the complex form.  It can also be entered as an inductance or capacitance.  To do so add a 'h' suffix for inductance or a 'f' for capacitance.

After the '-unilateral' operator is used, it resets gs, gl, zs, and zl.

By default the utility writes out the network on the top of
the stack in touchstone format with GUM and stability information 
as comments.  It can also output the network in following alternative formats:

```
-a            : display the network as ABCD matrices
-z            : summarize the network in terms of impedance, stability and gain (dB) values
-m            : show matching solutions in impedance
-g            : show matching solutions in gamma
-gnoise <int> : show matching solutions in gamma from Gopt to Gms in int steps
-znoise <int> : show matching solutions in impedance from Gopt to Gms in int steps
-lmatch1      : match with lumped l-section networks
-lmatch2      : match with transmission line l-section networks
-sec1         : match with a short section of transmission line
-stub1        : match with a single shunt stub network
-stub2        : match with a double shunt stub network
-qwt1         : match with a quarter wavelength with series section
-qwt2         : match with a quarter wavelength and shunt stub
-qwt3 <real>  : match with a quarter wavelength and shunt stub of given impedance
-line <real>  : line impedance to match to
```

Only 50 ohm networks are supported.

Installation
------------
```
$ cd <repo_directory>
$ pip install .
$ sh test.sh       # to run unit tests
```

Examples
--------

Add GUM (dB), K and mu as comments to touchstone file.


```
$ < 2n5179_5ma.s2p cascade
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00       6.78  180.00          0    0.00      0.844    0.00 !  23.13       inf     1.185
100         0.471  -90.00       6.78  122.00      0.023   64.00      0.844  -51.00 !  23.13    0.4623    0.8889
200         0.314 -145.00        4.2  100.00      0.034   58.00       0.78  -93.00 !  16.99     1.109     1.021
300          0.23  156.00       2.76   91.00      0.043   65.00      0.768 -134.00 !  12.92     1.819     1.145
400         0.171  108.00       2.17   86.00      0.056   63.00      0.756 -177.00 !  10.54     1.874     1.157
500         0.168   54.00       1.86   79.00      0.062   62.00      0.741  140.00 !   8.97     1.883     1.147
600         0.149   -9.00       1.53   71.00      0.069   66.00       0.74   98.00 !   7.24     2.074     1.164
700         0.137  -72.00       1.31   67.00      0.073   71.00      0.739   54.00 !   5.86     2.469     1.213
800         0.119 -129.00       1.18   64.00      0.092   74.00      0.744    8.00 !   5.00     2.098     1.174
900         0.153 -174.00       1.13   58.00      0.101   68.00      0.742  -38.00 !   4.64     1.875     1.142
1000        0.171  122.00      0.979   49.00      0.106   71.00      0.749  -82.00 !   3.52     2.083     1.164
```


Display the result as ABCD matrices.


```
$ < 2n5179_5ma.s2p cascade -a
# MHZ A MA
! MHZ                   A                  B                  C                  D
0         0.01692 -180.00         10 -180.00  0.0001217 -180.00    0.07194 -180.00
100       0.05534  -88.08      7.139 -166.65   0.001397  -51.43     0.1243 -120.34
200         0.107  -70.35      6.367 -148.80   0.004076  -59.44       0.17 -131.82
300        0.2218  -60.14      6.235 -130.84   0.007505  -77.69     0.1408 -149.65
400        0.3684  -72.05      4.008  -95.97   0.009134  -94.89    0.03424  -93.31
500        0.4608  -86.97      9.595  -33.46   0.008633 -105.44     0.1543  -28.46
600        0.4624 -105.15      22.05  -37.35   0.008063 -103.97     0.3211  -24.06
700        0.2943 -122.15      32.17  -54.24   0.006801 -106.18     0.5633  -33.08
800       0.06799  -81.22      36.07  -68.63    0.00344  -87.15     0.7668  -53.02
900         0.246    0.28         33  -77.79   0.006156  -18.70     0.8021  -71.03
1000       0.5662    4.77      33.48  -76.44    0.01307  -21.60     0.6974  -89.08
```


Summarize the network.  GU is not in dB.


```
$ < 2n5179_5ma.s2p cascade -z
MHZ                   Z1                Z2    GUI    S21    GUO    GUM   GMSG   GMAG     GU         K         D        MU
0                 139+0j            591+0j   1.09  16.62   5.41  23.13    inf  23.13   1.00       inf    0.3975     1.185
100         31.84-38.55j      22.13-100.9j   1.09  16.62   5.41  23.13  24.70      -      -    0.4623    0.2799    0.8889
200         27.94-11.17j      11.59-46.09j   0.45  12.46   4.07  16.99  20.92  18.91   1.18     1.109    0.1542     1.021
300          32.15+6.35j      7.719-20.79j   0.24   8.82   3.87  12.92  18.07  12.84   0.93     1.819    0.2728     1.145
400         42.77+14.33j      6.952-1.284j   0.13   6.73   3.68  10.54  15.88  10.49   0.94     1.874    0.2371     1.157
500         58.49+16.36j      8.399+17.74j   0.12   5.39   3.46   8.97  14.77   9.36   1.04     1.883    0.1073     1.147
600         67.17-3.202j       12.9+41.79j   0.10   3.69   3.44   7.24  13.46   7.56   1.04     2.074   0.08789     1.164
700         52.52-13.95j       33.5+88.26j   0.08   2.35   3.43   5.86  12.54   5.79   0.96     2.469    0.1926     1.213
800         42.35-7.945j        279+129.4j   0.06   1.44   3.50   5.00  11.08   5.12   0.99     2.098    0.1526     1.174
900         36.78-1.205j      58.96-119.9j   0.10   1.06   3.47   4.64  10.49   5.10   1.06     1.875   0.04344     1.142
1000         40.1+11.98j      16.23-54.84j   0.13  -0.18   3.58   3.52   9.65   3.73   1.01     2.083    0.1502     1.164
```


Shunt a 330 ohm resistor across the output of the two-port network.  This makes the transistor unconditionally stable.


```
$ < 2n5179_5ma.s2p cascade -shunt 330
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00      5.949  180.00          0    0.00      0.618    0.00 !  18.67       inf     1.618
100        0.4695  -88.72      6.069  124.55    0.02059   66.55     0.6577  -53.05 !  19.21     1.557     1.129
200        0.3082 -143.49       3.91  103.15    0.03165   61.15     0.6784  -95.81 !  14.95     1.884     1.182
300        0.2213  155.91      2.664   93.31     0.0415   67.31     0.7377 -135.77 !  12.14     2.142     1.199
400        0.1643  105.92       2.13   86.17    0.05498   63.17     0.7603 -177.12 !  10.44     1.906     1.155
500        0.1675   51.12        1.8   77.00       0.06   60.00     0.7204  141.75 !   8.41     2.151     1.187
600         0.155  -10.66      1.431   68.02    0.06452   63.02     0.6532  101.19 !   5.63         3     1.318
700        0.1428  -70.78      1.181   64.66    0.06579   68.66     0.5781   57.14 !   3.30     4.307     1.543
800        0.1197 -125.52      1.043   63.60     0.0813   73.60     0.5415    8.59 !   1.93     4.169     1.601
900        0.1491 -171.48      1.008   59.77    0.09013   69.77     0.5603  -40.49 !   1.81     3.657     1.501
1000       0.1638  121.96     0.9022   51.97    0.09769   73.97      0.632  -85.31 !   1.44     3.358     1.383
```


Cascade a series 20 ohm resistor with the output of the two-port network.


```
$ < 2n5179_5ma.s2p cascade -series 20
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00      6.575  180.00          0    0.00     0.8487    0.00 !  22.98       inf     1.178
100        0.4714  -93.44      6.155  115.16    0.02088   57.16     0.7407  -46.86 !  20.33     1.194     1.041
200        0.3248 -148.73      3.448   92.65    0.02791   50.65     0.5297  -82.32 !  12.67     3.225      1.49
300         0.248  155.65      2.105   86.17    0.03279   60.17     0.3788 -122.00 !   7.41     5.894     2.244
400         0.185  111.63      1.606   85.66    0.04145   62.66     0.2999 -175.86 !   4.68     6.681     2.792
500        0.1686   59.96      1.412   83.15    0.04708   66.15     0.3478  127.85 !   3.68      6.41     2.351
600        0.1339   -5.65      1.245   77.85    0.05613   72.85     0.4864   85.50 !   3.15      5.38     1.783
700        0.1236  -76.67       1.17   73.13    0.06521   77.13     0.6494   47.27 !   3.81      3.85     1.394
800        0.1201 -138.88      1.121   65.13    0.08738   75.13     0.7539    7.12 !   4.70     2.218     1.171
900         0.163  179.31       1.04   53.18    0.09292   63.18     0.7004  -33.51 !   3.38     2.516     1.229
1000       0.1883  121.15     0.8238   41.83    0.08919   63.83     0.5533  -71.64 !   0.06     4.533     1.568
```


Lift terminal 3, the port connected to ground, and add a 10nH inductor.  Then cascade the result
with a shunt 100 ohm resistor to stabilize the result.


```
$ < 2n5179_5ma.s2p cascade -lift 10e-9h -shunt 100
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00      4.641  180.00  1.187e-18 -180.00     0.2621   -0.00 !  14.73 6.576e+16     3.815
100        0.2894  -31.98       3.67  112.81    0.03295  129.17     0.2602  -55.49 !  11.98     3.527     2.349
200        0.2813    0.15      2.299   91.42     0.1193  112.36     0.2716  -97.16 !   7.92     1.653     1.612
300        0.3553    4.07      1.669   75.50     0.2257   82.69     0.3018 -146.61 !   5.45     1.188       1.2
400        0.3673   -2.21      1.266   61.02     0.2619   55.24     0.2773  162.64 !   3.03     1.297     1.292
500        0.3933   -3.40     0.9646   51.78     0.2325   39.45     0.2338  118.67 !   0.66      1.81     1.675
600        0.3965  -14.35     0.7704   47.45      0.207   37.88     0.2079   80.31 !  -1.33      2.53     2.132
700         0.319  -21.21     0.6623   46.78     0.1807   37.44     0.2023   41.51 !  -2.93     3.631     2.797
800        0.2797   -3.83     0.5861   50.23     0.1252   54.88     0.2335    0.19 !  -4.04     5.997     3.258
900         0.375    0.32     0.6423   57.44     0.2209  100.88     0.3044  -46.80 !  -2.76     2.922     2.412
1000       0.4493  -17.00     0.8127   50.80     0.4842   83.82     0.3872 -103.62 !  -0.12     1.103     1.127
```


Insert a one ohm resistor at the emitter to provide shunt feedback.


```
$ < 2n5179_5ma.s2p cascade -lift 1
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.507   -0.00      6.308  180.00  0.0007679    0.00     0.8541   -0.00 !  22.97     21.18     1.166
100        0.5026  -82.33      6.453  124.47    0.03084   68.45     0.8719  -48.35 !  23.66    0.1972    0.8006
200        0.3182 -135.30      4.084  101.58    0.04909   53.96     0.7981  -89.87 !  17.08    0.6767    0.9192
300         0.207  163.41      2.689   91.88    0.05657   50.07     0.7621 -130.87 !  12.56     1.447     1.098
400        0.1457  109.26      2.112   86.78    0.06327   47.44     0.7312 -174.12 !   9.91     1.872     1.178
500        0.1549   49.71      1.817   79.92    0.06313   48.98     0.7097  142.15 !   8.34     2.119     1.197
600        0.1538  -13.14      1.505   71.80     0.0672   56.96     0.7137   99.11 !   6.75     2.338     1.206
700        0.1477  -71.33      1.295   67.61    0.06973   65.17      0.724   54.26 !   5.56     2.716     1.243
800        0.1235 -123.93      1.171   64.46    0.09085   72.14     0.7409    7.85 !   4.89     2.168     1.183
900        0.1491 -169.65      1.126   58.22     0.1062   66.54     0.7445  -38.10 !   4.64     1.784     1.133
1000       0.1609  123.17     0.9781   48.86     0.1141   66.76     0.7477  -81.82 !   3.48     1.947     1.153
```


Transform the common emitter s-parameter input into a common-base.


```
$ < 2n5179_5ma.s2p cascade -cbg | tee cb.s2p
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0          0.6692  180.00       1.55   -0.00     0.0258    0.00     0.9649   -0.00 !  18.00     1.141     1.011
100        0.7455  173.47      1.673  -11.49    0.08774   75.40      1.046  -10.87 !      -   0.04985    0.7311
200        0.7834  166.09      1.623  -22.23     0.1673   79.26      1.115  -27.69 !      -   -0.1685    0.4953
300         0.798  154.26       1.41  -32.60     0.3239   72.65      1.017  -53.92 !      -   -0.1879    0.3329
400        0.7442  144.59      1.256  -34.55      0.464   48.66     0.6954  -75.56 !   8.36    0.1916    0.3582
500        0.7206  135.76      1.264  -36.70      0.528   27.09     0.3917  -83.59 !   5.94    0.5052    0.3812
600        0.6681  125.60      1.315  -44.49     0.5151    3.26     0.1657  -65.59 !   5.07    0.7577    0.4936
700        0.5996  116.64      1.338  -57.47     0.3734  -19.62     0.2935    7.81 !   4.85    0.9993    0.9977
800        0.5371  109.65      1.212  -74.72     0.1278  -28.04     0.7227   -6.39 !   6.36     1.523     1.194
900        0.4694  105.01     0.9932  -93.71      0.209   81.20      1.083  -40.18 !      -   -0.3312    0.7231
1000        0.414   89.52     0.5058 -123.81     0.5353   63.17      1.108  -80.94 !      -   -0.3771    0.6711
```


Create a cascode amplifier.  S12 is significantly reduced compared to a CE amp.


```
$ < 2n5179_5ma.s2p cascade -f cb.s2p -cascade
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00      6.716  180.00          0    0.00     0.9865    0.00 !  33.34       inf     1.014
100        0.4483  -80.32      7.881  132.15   0.001402  161.04      1.108   -7.70 !      -    -8.698    0.8867
200        0.2328 -128.95      6.756  113.18   0.005638  172.67      1.305  -23.48 !      -    -8.781    0.7421
300        0.0308  150.86      8.191   84.93    0.02932  164.18      1.743  -59.59 !      -    -4.073    0.5058
400       0.07062  168.43      4.502   21.58    0.04292   81.79     0.7419 -136.29 !  16.56     1.237     1.063
500       0.09522   43.22      2.166   12.99    0.03016   59.78    0.07264  127.14 !   6.78     7.577     7.245
600        0.1466  -28.60      1.437   12.42    0.02538   55.17     0.3441   15.47 !   3.79     11.84     2.616
700        0.1725  -78.73      1.218   12.40    0.01894   54.25     0.5338   -5.24 !   3.30     15.13     1.805
800        0.1605 -119.73      1.156    5.91   0.009504   62.59     0.7571  -13.10 !   5.07     19.04     1.304
900        0.1849 -157.40      1.218  -15.35    0.02291  169.56      1.248  -38.84 !      -    -9.861      0.78
1000        0.181  142.01     0.7138  -71.46    0.08179  137.52      1.286  -92.10 !      -    -5.604    0.7372
```


Stabilize the cascode amp with a 100 ohm resistor across the output.


```
$ < 2n5179_5ma.s2p cascade -f cb.s2p -cascade -shunt 100
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
0           0.471    0.00      4.487  180.00          0    0.00     0.3273    0.00 !  14.62       inf     3.055
100        0.4465  -80.38      5.168  133.55  0.0009194  162.44     0.3832   -9.59 !  15.92     71.73     2.554
200        0.2298 -130.26      4.346  117.98   0.003626  177.47     0.4864  -26.26 !  14.17     22.95     1.988
300       0.05872  112.41      5.397   99.27    0.01931  178.52     0.7909  -55.60 !  18.92     1.877     1.122
400       0.06053 -154.28      4.008   28.13    0.03821   88.34     0.6741 -142.93 !  14.70     1.828       1.2
500       0.08392   38.87      1.748   12.32    0.02434   59.11      0.231  170.60 !   5.12     11.08     3.688
600        0.1474  -31.25      1.078   11.43    0.01904   54.18    0.05164   90.05 !   0.76     23.77     13.21
700         0.176  -79.49     0.8808   12.91     0.0137   54.76     0.1107  -13.32 !  -0.91     39.69     8.258
800        0.1624 -119.61     0.8056    7.62   0.006623   64.30     0.2294  -21.30 !  -1.53     86.48     4.271
900        0.1815 -156.44     0.8088   -7.88    0.01521  177.03     0.5032  -43.32 !  -0.43     29.27      1.93
1000       0.1758  145.27      0.558  -56.91    0.06394  152.07     0.7856  -91.95 !  -0.76     5.114     1.209
```


Summarize the stabilized cascode amp.


```
$ < 2n5179_5ma.s2p cascade -f cb.s2p -cascade -shunt 100 -z
MHZ                   Z1                Z2    GUI    S21    GUO    GUM   GMSG   GMAG     GU         K         D        MU
0                 139+0j  98.66+9.406e-17j   1.09  13.04   0.49  14.62    inf  14.62   1.00       inf    0.1542     3.055
100         38.12-41.92j        109-16.32j   0.97  14.27   0.69  15.92  37.50  15.93   1.00     71.73    0.1668     2.554
200         35.09-12.99j       104.8-59.1j   0.24  12.76   1.17  14.17  30.79  14.17   1.00     22.95    0.1134     1.988
300         47.53+5.179j      25.58-89.17j   0.02  14.64   4.27  18.92  24.46  19.06   0.98     1.877    0.1426     1.122
400          44.77-2.36j      10.78-16.06j   0.02  12.06   2.63  14.70  20.21  14.95   1.01     1.828    0.1331       1.2
500         56.65+6.009j      31.36+2.499j   0.03   4.85   0.24   5.12  18.56   5.12   1.00     11.08   0.05842     3.688
600         63.55-9.933j       49.73+5.15j   0.10   0.65   0.01   0.76  17.53   0.76   1.00     23.77     0.013     13.21
700          50.12-17.9j      61.98-3.202j   0.14  -1.10   0.05  -0.91  18.08  -0.91   1.00     39.69   0.03112     8.258
800          41.02-11.9j      75.77-13.33j   0.12  -1.88   0.23  -1.53  20.85  -1.53   1.00     86.48   0.04184     4.271
900         35.41-5.312j      71.67-66.25j   0.15  -1.84   1.27  -0.43  17.26  -0.42   1.00     29.27   0.07917      1.93
1000        36.71+7.588j         11.46-47j   0.14  -5.07   4.17  -0.76   9.41  -0.65   1.02     5.114     0.114     1.209
```


Show impedance matching information.


```
$ < example2.s2p cascade -m
MHZ        QS                ZS  SWRIN   MLIN               ZIN              ZOUT  MLOUT SWROUT                ZL     QL !     GT     NF     NM
2000     1.47      5.124-7.542j   1.00   0.00      5.124+7.542j      33.68-91.48j   0.00   1.00      33.68+91.48j   2.72 !  16.18      -      -
```


Show gamma matching information.


```
$ < example2.s2p cascade -g
MHZ        QS                 GS  SWRIN   MLIN                GIN               GOUT  MLOUT SWROUT                 GL     QL !     GT     NF     NM
2000     1.47     0.8179 -162.67   1.00   0.00     0.8179  162.67     0.7495  -52.57   0.00   1.00     0.7495   52.57   2.72 !  16.18      -      -
```


A stub match example.  Stub lengths are in degrees.


```
$ < example2.s2p cascade -stub1
MHZ     (LBAL)  LSHUNT LSERIES                ZS                ZL LSERIES  LSHUNT (LBAL)
2000     17.93  109.38  153.77      5.124-7.542j      33.68+91.48j   42.99  113.83   20.15 o/o
2000     38.76   19.38  153.77      5.124-7.542j      33.68+91.48j   42.99   23.83   47.65 s/s
2000     35.31   70.62    8.90      5.124-7.542j      33.68+91.48j   84.44   66.17   33.09 o/o
2000     14.48  160.62    8.90      5.124-7.542j      33.68+91.48j   84.44  156.17    5.59 s/s
```


A L-section match example.


```
$ < example2.s2p cascade -lmatch1
MHZ       SHUNT   SERIES !   SERIES    SHUNT                ZS                ZL    SHUNT   SERIES !   SERIES    SHUNT
2000    1.345nH  3.505pF !        -        -      5.124-7.542j      33.68+91.48j   4.61nH  738.6fF !  5.715nH  5.414nH
2000     4.71pF  606.6pH !        -        -      5.124-7.542j      33.68+91.48j  39.99nH  8.574nH !  1.108pF  9.146nH
```


A quarter wave transformer with a series section example.


```
$ < example2.s2p cascade -qwt1
MHZ         ZQWT   ZSERIES LSERIES                ZS                ZL LSERIES   ZSERIES      ZQWT
2000         158        50   81.33      5.124-7.542j      33.68+91.48j  153.72        50     132.1
2000       15.83        50  171.33      5.124-7.542j      33.68+91.48j   63.72        50     18.92
```


A quarter wave transformer and stub match example.


```
$ < example2.s2p cascade -qwt2
MHZ         ZQWT    ZSHUNT  LSHUNT    (ZBAL)                ZS                ZL    (ZBAL)  LSHUNT    ZSHUNT      ZQWT
2000       28.48     11.02   45.00     22.05      5.124-7.542j      33.68+91.48j     207.8  135.00     103.9     118.8 o/o
2000       28.48     11.02  135.00     22.05      5.124-7.542j      33.68+91.48j     207.8   45.00     103.9     118.8 s/s
```


A quarter wave transformer and 72 ohm stub match example.


```
$ < example2.s2p cascade -qwt3 72
MHZ         ZQWT    ZSHUNT  LSHUNT  (LBAL)                ZS                ZL  (LBAL)  LSHUNT    ZSHUNT      ZQWT
2000       28.48        72   81.30   72.98      5.124-7.542j      33.68+91.48j  160.89  145.27        72     118.8 o/o
2000       28.48        72  171.30  162.98      5.124-7.542j      33.68+91.48j   70.89   55.27        72     118.8 s/s
```


Match using a short transformer section.  (See Rizzi p132)


```
$ < 2n5179_5ma.s2p cascade -sec1
MHZ      ZSERIES LSERIES                ZS                ZL LSERIES   ZSERIES
0          83.38   90.00            139+0j            591+0j   90.00     171.9
100            -       -                 -                 -       -         -
200            -       -      9.257+23.75j      4.537+48.96j       -         -
300        38.51  131.63       36.15+9.48j      7.455+21.63j       -         -
400        58.28  109.09      65.42-6.219j     6.595+0.8484j   93.08     18.14
500        74.92  117.61      88.57-30.23j      7.046-18.47j       -         -
600         70.2  107.80      90.36-18.19j      10.99-41.56j       -         -
700        53.75  112.79      56.46-2.915j      32.68-87.82j       -         -
800        40.17   76.13      32.94-3.385j      309.1-137.7j  100.88     138.2
900        34.15   83.40      23.49-2.097j      49.48+126.1j       -         -
1000       36.81   72.08      28.33-5.161j      14.91+56.68j       -         -
```


## More examples

Match a network for maximum gain.


```
$ < example3.s2p cascade -qwt2
MHZ         ZQWT    ZSHUNT  LSHUNT    (ZBAL)                ZS                ZL    (ZBAL)  LSHUNT    ZSHUNT      ZQWT
4000       65.39     11.78   45.00     23.56      1.593-11.56j       1.58+70.85j     141.8  135.00     70.89     398.7 o/o
4000       65.39     11.78  135.00     23.56      1.593-11.56j       1.58+70.85j     141.8   45.00     70.89     398.7 s/s
```


Create a network of this match.


```
$ < example3.s2p cascade -pass -tline 65.39/90 -open 11.78/45 -swap -cascade -open 70.89/135 -tline 398.7/90
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
4000     0.001336   99.41      5.419 -173.66      0.158 -176.66   0.001339   88.91 !  14.68     1.012     1.168
```


Match using double stubs.  LBAL gives the balanced stub length.


```
$ < example3.s2p cascade -stub2
MHZ     (LBAL)  LSHUNT LSERIES  LSHUNT  (LBAL)                ZS                ZL  (LBAL)  LSHUNT LSERIES  LSHUNT  (LBAL)
4000     10.51  158.63   45.00  170.77   34.78      1.593-11.56j       1.58+70.85j  103.76  115.24   45.00  175.33   43.89 ss/ss
4000    121.82   60.93   45.00  167.01   27.26      1.593-11.56j       1.58+70.85j   66.81   96.73   45.00    5.58   11.16 ss/ss
4000     34.32   68.63   45.00   80.77   40.39      1.593-11.56j       1.58+70.85j   12.62   25.24   45.00   85.33   42.67 oo/oo
4000     75.51  150.93   45.00   77.01   38.51      1.593-11.56j       1.58+70.85j    3.36    6.73   45.00   95.58   47.80 oo/oo
4000     10.51  158.63   45.00   80.77   40.39      1.593-11.56j       1.58+70.85j   12.62   25.24   45.00  175.33   43.89 so/os
4000    121.82   60.93   45.00   77.01   38.51      1.593-11.56j       1.58+70.85j    3.36    6.73   45.00    5.58   11.16 so/os
4000     34.32   68.63   45.00  170.77   34.78      1.593-11.56j       1.58+70.85j  103.76  115.24   45.00   85.33   42.67 os/so
4000     75.51  150.93   45.00  167.01   27.26      1.593-11.56j       1.58+70.85j   66.81   96.73   45.00   95.58   47.80 os/so
4000    111.42  119.07  135.00  166.46   26.17      1.593-11.56j       1.58+70.85j   66.38   33.19  135.00  174.42   42.08 ss/ss
4000     42.73   21.37  135.00  156.81    6.86      1.593-11.56j       1.58+70.85j   55.96   27.98  135.00    4.67    9.35 ss/ss
4000     14.53   29.07  135.00   76.46   38.24      1.593-11.56j       1.58+70.85j   61.62  123.19  135.00   84.42   42.22 oo/oo
4000     55.70  111.37  135.00   66.81   33.41      1.593-11.56j       1.58+70.85j   59.01  117.98  135.00   94.67   47.35 oo/oo
4000    111.42  119.07  135.00   76.46   38.24      1.593-11.56j       1.58+70.85j   61.62  123.19  135.00  174.42   42.08 so/os
4000     42.73   21.37  135.00   66.81   33.41      1.593-11.56j       1.58+70.85j   59.01  117.98  135.00    4.67    9.35 so/os
4000     14.53   29.07  135.00  166.46   26.17      1.593-11.56j       1.58+70.85j   66.38   33.19  135.00   84.42   42.22 os/so
4000     55.70  111.37  135.00  156.81    6.86      1.593-11.56j       1.58+70.85j   55.96   27.98  135.00   94.67   47.35 os/so
```


Add 29.3 degrees of 50 ohm transmission line to the amplifier in HP Application Note 967 and on page 340 of Gonzalezi's Microwave Transistor Amplifiers.  Gonzalez has a corrected value 
for the load reflection coefficient in AN967.


```
$ < example3.s2p cascade -gs .475/166 -unilateral -tline 50/29.3
# MHZ S MA R 50
! MHZ                 S11                S21                S12                S22 !    GUM         K        MU
4000       0.7444  157.00      1.681   -3.30          0    0.00     0.8438 -129.04 !  13.43       inf     1.185
```


Use Gonzalez's analytic method on p.318, drawing a straight line from Gopt to Gms, to select GS.


```
$ < example4.s2p cascade -gnoise 5
MHZ        QS                 GS  SWRIN   MLIN                GIN               GOUT  MLOUT SWROUT                 GL     QL !     GT     NF     NM
4000     0.56       0.45 -150.00   2.69  -1.02     0.7524  147.97     0.6227  -62.09   0.00   1.00     0.6227   62.09   1.80 !   9.76   3.00   0.46
4000     0.79     0.5433 -149.17   2.22  -0.67     0.7644  147.95     0.6542  -61.71   0.00   1.00     0.6542   61.71   2.01 !  10.21   3.05   0.52
4000     1.12     0.6367 -148.59   1.79  -0.36     0.7792  147.93     0.6914  -61.31   0.00   1.00     0.6914   61.31   2.32 !  10.63   3.24   0.83
4000     1.65     0.7301 -148.15   1.39  -0.12     0.7983  147.89     0.7361  -60.89   0.00   1.00     0.7361   60.89   2.81 !  10.97   3.64   1.55
4000     2.73     0.8236 -147.82   1.00   0.00     0.8236  147.82     0.7909  -60.46   0.00   1.00     0.7909   60.46   3.67 !  11.14   4.50   2.94
```


```
$ < example4.s2p cascade -znoise 5
MHZ        QS                ZS  SWRIN   MLIN               ZIN              ZOUT  MLOUT SWROUT                ZL     QL !     GT     NF     NM
4000     0.56      20.12-11.35j   2.69  -1.02      7.632+14.04j      38.04-68.38j   0.00   1.00      38.04+68.38j   1.80 !   9.76   3.00   0.46
4000     0.79      15.82-12.49j   2.22  -0.67      7.218+14.08j      35.41-71.31j   0.00   1.00      35.41+71.31j   2.01 !  10.21   3.05   0.52
4000     1.12      11.93-13.31j   1.79  -0.36      6.708+14.13j       32.06-74.5j   0.00   1.00       32.06+74.5j   2.32 !  10.63   3.24   0.83
4000     1.65      8.418-13.89j   1.39  -0.12      6.067+14.19j       27.74-77.9j   0.00   1.00       27.74+77.9j   2.81 !  10.97   3.64   1.55
4000     2.73      5.236-14.28j   1.00   0.00      5.236+14.28j      22.15-81.37j   0.00   1.00      22.15+81.37j   3.67 !  11.14   4.50   2.94
```



