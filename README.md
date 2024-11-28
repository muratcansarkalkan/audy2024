# Audy 2024

Audy 2024 is a Python-based CLI tool for importing PA calls for players.

As of now, you can import PA data for NBA Live 2005 and 06. More will be implemented in near future.

## Prerequisites

- Python 3.10
- SX

## Before Use

Make sure to have SX.EXE somewhere in C:\ and add the directory of SX.EXE to PATH variable. Otherwise the tool will not work. You can extract SX.EXE from SX.zip and place it anywhere in disk C. Don't forget where you placed it!

## How to Use

Open config.ini in notepad and change the path2005 and path06 values with the path that you installed the games.

Create folders with 4-digit IDs in either speeches2005 or speeches06 (depending on the game you want to import PA sounds) and place .wav files. For now, there are only 3 types of calls available.
Place .wav files into the folder as 0.wav, 1.wav and 2.wav.

0 - excited, long call
1 - excited call
2 - normal call

You can do it for as many IDs as you want, just make sure that speech ID is available and not in use. You can use IDs between 0000 and 9999.

Then, run import.bat to start the tool.

First, specify the game you want to import sound for. For NBA Live 2005, type 2005 and press Enter. For NBA Live 06, type 06 and press Enter.

Then, specify the operation you want to execute. To convert sounds to .asf files and creating HDR data, type I and press Enter. To convert import sound data to game, type A and press Enter.

To import data, first you need to convert sounds to .asf files and create HDR data. Once done, you can import HDR data into larger files the game use. 

So the correct use is running import.bat twice and here are the steps

- Run import.bat
- Type 2005 or 06, Enter, then type I
- After operation ends, press any key to exit
- Run import.bat again
- Type 2005 or 06, Enter, then type A
- After operation ends, press any key to exit