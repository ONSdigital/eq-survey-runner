# Profiling

## cProfile
cProfile is a deterministic profiler in which trace functions are executed at various points of interest (e.g. function call, function return, exceptions), and precise timings of these events are recorded.

To profile the application using cProfile, run `make profile`. 
Profiling information will be collected per-request in the `profiling` directory where it can be examined using the pstats interactive browser.

To load the file into the interactive browser where it can be sorted and queried as required run:
```bash
python -m pstats [filename].prof
```

The profiles can also be combined to give an overview of the profile between all requests.

Combine all the profiles in the 'profiling' directory using:
```bash
pipenv run python scripts/merge_profiles.py
```
Ensure you delete all the files in this directory before starting your profiling session.
This will create a file called `combined_profile.prof`

To visualise this profile, `snakeviz` or `gprof2dot` can be used.


### Visualisation
There are many handy profilers, but they lack a nice visualisation interface. We use `snakeviz` and `gprof2dot` for this.

---

#### SnakeViz
[SnakeViz](https://jiffyclub.github.io/snakeviz/#snakeviz) is a browser-based graphical visualisation tool to display profiles using Icicle and Sunburst plots. 
It also includes IPython line and cell magics that can help profile a single line or code blocks directly and then visualise them. 

Install using:
```bash
pip install snakeviz
```
##### Visualise a profile:
```bash
snakeviz profiling/[filename].prof
```
For example:
```bash
snakeviz profiling/GET.questionnaire.31ms.1571053121.prof
```

---

#### gprof2dot
Converts profiler data into call graphs. It allows to filter functions based on metrics threshold and colour them nicely with hotspots.

First install `graphviz` and `gprof2dot`:
```bash
brew install graphviz
pip install gprof2dot
```
##### Visualise a profile:
```bash
pipenv run gprof2dot -f pstats profiling/[filename].prof | dot -Tpng -o output.png
```
For example:
```bash
pipenv run gprof2dot -f pstats profiling/GET.questionnaire.31ms.1571053121.prof | dot -Tpng -o profile.png
```
To visualise the combined profile run:
```bash
pipenv run gprof2dot -f pstats combined_profile.prof | dot -Tpng -o combined_profile.png
```

---

## Py-Spy
[Py-Spy](https://github.com/benfred/py-spy) is a sampling profiler where instead of tracking every event (e.g. function call), the application is periodically interrupted, and stack snapshots are collected. 
The function call stack is then analysed to deduce the execution time of different parts of the application. 

Deterministic profilers modify application execution in some way: profiling code is typically run inside the target Python process, which often slows down application execution. 
To avoid this performance impact, Py-Spy doesn’t run in the same process as the profiled Python program. Because of this, Py-Spy can be used in a production environment with little overhead.

Py
First, install `Py-Spy`:
```bash
pip install py-spy
```

Run survey runner using `make run` and get the process id.

Run `Py-Spy` using:
```bash
sudo py-spy record -o profile.svg --pid 12345
```
This will sample the application until the process is terminated. Once terminated, it will display a flame graph for the sampled profiles.

[Why do you need to run Py-Spy as sudo?](https://github.com/benfred/py-spy#when-do-you-need-to-run-as-sudo)

---

More info: [Python profiling tools](http://pramodkumbhar.com/2019/05/summary-of-python-profiling-tools-part-i/)
