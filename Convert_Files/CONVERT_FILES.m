%% CONVERT_FILES.m
%   In conjunction with Tag2Matlab.jar, this file takes Escort data system 
%   files (.for, .tag) and converts them into Matlab code.  This program 
%   allows the data engineer to validate and verify Escort code before 
%   deployment to the facility.
%
% 2015/10/13 - J. Borman

%% Program Setup

%   Make sure all files are in the same folder and list the folder name
folder_name = 'B:\PSL4 COBRA Upgrade\DATA ENGINEER\Baseline\Subroutines';

%   List all the subroutines that you would like converted separated
%   by a comma and beginning and ending with the curly brackets {}.
%   NOTE: be sure to include the file extension
file={
    'NOZZLE_DATA.for',
    'AVGS_DP1_FACILITY.tag',
    'AVGS_DP1_MKS.tag', 
    'AVGS_PSL3_LAB_SEAL.tag',
    'AVGS_PSL4_LAB_SEAL.tag',
    'AVGS_REFS.tag',
    'AVGS_STATION2.tag',
    'AVGS_THRUST_FMS.tag',
    'AVGS_THRUST_ORMOND.tag',
    'CUSTOMER_CALCS.tag',
    'FACILITY_AIRFLOW.tag',
    'FACILITY_CALCS.tag',
    'FUEL_CALCS.tag',
    'MISC_AVGS.tag',
    'STATION1.tag',
    'STATION2.tag',
    'THRUST_FMS.tag',
    'THRUST_ORMOND.tag'
    };
%   For all the above listed tag files, if there are any subroutines or
%   functions with inputs and outputs, you must include a comment line
%   above the call listing each input and output, using the following format:
%       C   @inputs = INPUT1, INPUT2, INPUT3
%       C   @outputs= OUTPUT1, OUTPUT2
%           SUBROUTINE SUBROUTE(INPUT1,INPUT2,INPUT3,OUTPUT1,OUTPUT2)


%   Enter the folder location of the Tag2Matlab.jar file 
Tag2Matlab_file_folder = 'C:\Users\jborman\Documents\NetBeansProjects\Tag2Matlab\dist';

%   Enter the folder location of the FindVariables.jar file
FindVariables_file_folder = 'C:\Users\jborman\Documents\NetBeansProjects\FindVariables\dist';




%--------------------------------------------------------------------------------------
%% CHANGING ANYTHING BELOW THIS LINE CAN COMPROMISE THE ABILITY FOR THIS PROGRAM TO RUN
%--------------------------------------------------------------------------------------
%% Error check the Program Setup

% Check if this routine is called from SIMSCAN_TEST
try 
    if convert_call == 1 && ss == 1
        folder = file_folder_name;
    else
        folder = folder_name;
    end
catch errormessage
    folder = folder_name;
end

if strfind(lower(char(folder)),'.') > 0
    error('folder_name MUST NOT have an extension');
elseif folder(numel(folder)) ~= '\'
    folder = strcat(folder,'\');
end

if strfind(lower(char(Tag2Matlab_file_folder)),'.') > 0
    error('Tag2Matlab_file_folder MUST NOT have an extension');
elseif Tag2Matlab_file_folder(numel(Tag2Matlab_file_folder)) ~= '\'
    Tag2Matlab_file_folder = strcat(Tag2Matlab_file_folder,'\');
end

if strfind(lower(char(FindVariables_file_folder)),'.') > 0
    error('FindVariables_file_folder MUST NOT have an extension');
elseif FindVariables_file_folder(numel(FindVariables_file_folder)) ~= '\'
    FindVariables_file_folder = strcat(FindVariables_file_folder,'\');
end

for i=1:length(file)
    checkFile = char(file(i));
    if length(strfind(checkFile,'.')) ~= 1
        error('each file MUST include a proper extension (i.e. ".tag")');
    end
end


%% Combine folder_name and file for Fortran and Java files

for i=1:length(file)
    fileLocation(i) = strcat(folder,file(i));
end
% fileLocation = char(fileLocation); % name of file to be executed


javaFile = strcat(Tag2Matlab_file_folder,'Tag2Matlab.jar');
javaaddpath(javaFile);

% Future Capability***
javaFile = strcat(FindVariables_file_folder,'FindVariables.jar');
javaaddpath(javaFile);

%% Evaluate Tag2Matlab routine
convert = tag2matlab.Tag2Matlab;
for i=1:length(fileLocation)
    FL = char(fileLocation(i));
    convert.run(0,FL);
end


javarmpath(javaFile);  % must be last line executed



