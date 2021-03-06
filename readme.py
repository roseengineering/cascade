
import os, subprocess 

def run(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    buf = proc.stdout.read().decode()
    proc.wait()
    return f"""
```
$ {command}
{buf}\
```
"""

print(f"""
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

{ run("< 2n5179_5ma.s2p cascade") }

Display the result as ABCD matrices.

{ run("< 2n5179_5ma.s2p cascade -a") }

Summarize the network.  GU is not in dB.

{ run("< 2n5179_5ma.s2p cascade -z") }

Shunt a 330 ohm resistor across the output of the two-port network.  This makes the transistor unconditionally stable.

{ run("< 2n5179_5ma.s2p cascade -shunt 330") }

Cascade a series 20 ohm resistor with the output of the two-port network.

{ run("< 2n5179_5ma.s2p cascade -series 20") }

Lift terminal 3, the port connected to ground, and add a 10nH inductor.  Then cascade the result
with a shunt 100 ohm resistor to stabilize the result.

{ run("< 2n5179_5ma.s2p cascade -lift 10e-9h -shunt 100") }

Insert a one ohm resistor at the emitter to provide shunt feedback.

{ run("< 2n5179_5ma.s2p cascade -lift 1") }

Transform the common emitter s-parameter input into a common-base.

{ run("< 2n5179_5ma.s2p cascade -cbg | tee cb.s2p") }

Create a cascode amplifier.  S12 is significantly reduced compared to a CE amp.

{ run("< 2n5179_5ma.s2p cascade -f cb.s2p -cascade") }

Stabilize the cascode amp with a 100 ohm resistor across the output.

{ run("< 2n5179_5ma.s2p cascade -f cb.s2p -cascade -shunt 100") }

Summarize the stabilized cascode amp.

{ run("< 2n5179_5ma.s2p cascade -f cb.s2p -cascade -shunt 100 -z") }

Show impedance matching information.

{ run("< example2.s2p cascade -m") }

Show gamma matching information.

{ run("< example2.s2p cascade -g") }

A stub match example.  Stub lengths are in degrees.

{ run("< example2.s2p cascade -stub1") }

A L-section match example.

{ run("< example2.s2p cascade -lmatch1") }

A quarter wave transformer with a series section example.

{ run("< example2.s2p cascade -qwt1") }

A quarter wave transformer and stub match example.

{ run("< example2.s2p cascade -qwt2") }

A quarter wave transformer and 72 ohm stub match example.

{ run("< example2.s2p cascade -qwt3 72") }

Match using a short transformer section.  (See Rizzi p132)

{ run("< 2n5179_5ma.s2p cascade -sec1") }

## More examples

Match a network for maximum gain.

{ run("< example3.s2p cascade -qwt2") }

Create a network of this match.

{ run("< example3.s2p cascade -pass -tline 65.39/90 -open 11.78/45 -swap -cascade -open 70.89/135 -tline 398.7/90") }

Match using double stubs.  LBAL gives the balanced stub length.

{ run("< example3.s2p cascade -stub2") }

Add 29.3 degrees of 50 ohm transmission line to the amplifier in HP Application Note 967 and on page 340 of Gonzalezi's Microwave Transistor Amplifiers.  Gonzalez has a corrected value 
for the load reflection coefficient in AN967.

{ run("< example3.s2p cascade -gs .475/166 -unilateral -tline 50/29.3") }

Use Gonzalez's analytic method on p.318, drawing a straight line from Gopt to Gms, to select GS.

{ run("< example4.s2p cascade -gnoise 5") }
{ run("< example4.s2p cascade -znoise 5") }

""")

os.unlink("cb.s2p")

