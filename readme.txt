~*~ CALMY JANE'S MICROGRANNY ORGANICER ~*~

This repostiory contains a tool written in python that can be used to update the samples and preset on a MicroGranny's SD-Card.

What is the MicroGranny?
https://bastl-instruments.com/instruments/microgranny/
I's an arduino-based sampler from Bastl Instruments. You can load samples to a microSD-Card and play them from the MG. The Samples are named A0.wav, A1.wav, AM.wav ...
On the MG you can also store your assignments for the 6 buttons (Sample, Attack for the Sample, Release ...) in a Preset. The presets are also stored on the microSC-Card and are named (P01.txt, P02.txt ...) and are (absolutely) not human readable.

This tool is should provide a nice UI to easily manage your samples, assign human-readable names linked to the A0,A1.. wav-files and edit all parameters in the preset files.

The pure code for decoding the preset-files can be found in the "Preset.py" File which contains a class that reads, parses and writes a presetfile. Feel free to use it for other projects!


IMPORTANT: Make a backup-copy of your SD card before using this tool in case anything goes wrong!