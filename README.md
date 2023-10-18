# Converting MIDI segments to Instrument Rolls 

By using the ReaScript feature inside the REAPER DAW the midi_to_rolls.py file 
can be run to save a copy of the selected MIDI segment and then produce a piano 
roll representation for the Piano, Bass, Drums, Guitar and Reed.  

## To Use the Code

- Have REAPER downloaded  
Reaper will automatically support running ReaScripts so only need to install 
REAPER.  

- Enable ReaScript to run python  
Ensure python is installed along with the modules listed at the top of 
midi_to_rolls.py.  

To install SWS (for saving copy of midi segment) follow these instructions:
 https://www.sws-extension.org/  

Within REAPER:  
Get to the REAPER preferences (on mac select 'REAPER' from top menu bar then 
'Settings...').  

Within settings scroll to the 'Plug-ins' section and click on 'ReaScript'.  

Tick 'Enable Python for use with ReaScript', and set the 'Custom path to Python 
dll directroy' and 'Force ReaScript to use specifc Python .dylib' to the 
appropriate interpreter's dynamic library and python environment.  

- Using ReaScripts  
Once you have selected a midi file in a track in Reaper you can use the ReaScript
by going to Actions (is selected on mac from top menu bar).

Then search 'ReaScript' and select:  
ReaScript: Run ReaScript    - to only execute the code.  
ReaScript: Run/edit ReaScript    - to bring up and IDE to view & execute the code

After selecting either option then select the midi_to_rolls.py file to run / 
edit it

You will need to update the path where you would like to save the midi segment 
copy its piano rolls.


NOTE: Currently there are some issues generating the paino rolls including:
-producing rolls for short MIDI segments
-reproducing rolls for segments (will only work once when first opening REAPER)

