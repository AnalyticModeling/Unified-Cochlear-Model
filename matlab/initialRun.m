%% Initialize
% clear; close all; clc;
set(0,'defaulttextfontsize',14);set(0,'DefaultAxesFontSize',14);

%% Library Bridge
% 1. Find the path to this file (.../Unified-Cochlear-Model/matlab/initialRun.m)
[currentDir, ~, ~] = fileparts(mfilename('fullpath'));

% 2. Going up to main MATLAB root folder
% (up from /matlab to /Unified-Cochlear-Model to /MATLAB)
parentDir = fileparts(fileparts(currentDir));

% 3. Define the deep path to FilterBank.m and other matlab files in the GEFs repo
gefsWrapperPath = fullfile(parentDir, 'GEFs', 'src', 'GEFs_core', 'matlab_wrappers');

% 4. Add to MATLAB path if it exists
if isfolder(gefsWrapperPath)
    addpath(gefsWrapperPath);
    disp(['Linked GEFs Wrappers at: ', gefsWrapperPath]);
else
    warning('Could not find GEFs wrappers. Check if GEFs folder is in: %s', parentDir);
end

%% GEFs Python Bridge
% 1. Pointing to the folder where Signal.py, Filter.py, etc. live
% they are in: GEFs/src/GEFs_core/
gefsPythonFolder = fullfile(parentDir, 'GEFs', 'src', 'GEFs_core');

% 2. Add it to the Python search path
if isfolder(gefsPythonFolder) && count(py.sys.path, gefsPythonFolder) == 0
    insert(py.sys.path, int32(0), gefsPythonFolder);
    disp('GEFs Python modules linked.');
end

%% Local Project Python Bridge
% 1. Find the 'python' folder inside your Unified-Cochlear-Model project
% currentDir is .../Unified-Cochlear-Model/matlab, so we go up one and into /python
localPythonFolder = fullfile(fileparts(currentDir), 'python');

% 2. Add it to the Python search path
if isfolder(localPythonFolder) && count(py.sys.path, localPythonFolder) == 0
    insert(py.sys.path, int32(0), localPythonFolder);
    disp('Local Cochlea Python module linked.');
end

%% Figure and Graphics Styling
set(0, 'DefaultFigureWindowStyle', 'docked'); % Groups all plots into one window
set(0, 'defaultFigurePosition', get(0, 'screensize')); % Makes figures full-screen
set(0, 'defaultLineLineWidth', 2);
set(0, 'DefaultLineMarkerSize', 8);
set(0, 'DefaultAxesTickLength', [0.03, 0.03]);
set(0, 'DefaultAxesLineWidth', 1);
set(0, 'DefaultAxesFontSize', 14);