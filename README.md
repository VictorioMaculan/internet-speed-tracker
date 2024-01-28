# trackyournet
 A simple command-line app that runs an internet speedtest in a determined interval of time, ~~so you can blame your internet provider because of their slow internet~~.

 You can install trackyournet with pip:

 ```
 pip install trackyournet
 ```

 ## How to use?
 After installing use the ``trackyournet`` command on your terminal, check the usage above.

 ```
 trackyournet [-h] -u {week, day, hour, min} -f FILE [-r REPEAT] interval
 ```

 ``interval`` is the interval between speedtests. _(Required; Integer)_
 
 ``-u`` or ``--unit`` is the unit of ``interval``: week, day, hour, or min (Minute). _(Required; String)_

 ``-f`` or ``--file`` receives a path pointing to an SQLite database or a directory where the data will be allocated (The database will be created if it doesn't exist). _(Required; String)_

 ``-r`` or ``--repeat`` is the amount of speedtest that will be run before exiting. _(Optional; Integer)_

 ``-h`` or ``--help`` prints the help message.
 
 **After starting, you can stop the application using ``Ctrl + C`` (Or whatever your terminal's abort key biding is). If ``repeat`` is passed it will stop running automatically after running the determined amount of speedstests.** 

 **NOTE**: Stopping the application with ``Ctrl + C`` while a speedtest is being run/registered may cause some problems with the database.

 ## Example
 Let's say you would like to run ten speedtests with an interval of 15 minutes between them:
 
 ```
 trackyournet 15 -u min -f {Your file/dir path here!} -r 10
 ```
 
 ## Final Message
 It's my first command line application and the first project I'm uploading to PyPI, so if you find a bug or have a suggestion, please, post it on [issues](https://github.com/VictorioMaculan/internet-speed-tracker/issues).

 (By the way, I pretend to add more ways of outputting the data)