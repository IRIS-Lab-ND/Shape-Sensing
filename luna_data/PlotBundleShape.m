%% Written by Dr. Margaret Coad

%% This code reads in a file of strain data and plots 3D fiber bundle shape
clear all
close all

%% Variables
% Data handling
FILENAME1 = "ODiSI 6000 Test_2023-03-27_14-37-23_ch1_full.tsv"; % file for first sensor
FILETYPE1 = 'text'; % use 'spreadsheet' for .xlsx and 'text' for .tsv
FILENAME2 = "ODiSI 6000 Test_2023-03-27_14-37-23_ch3_full.tsv"; % file for second sensor
FILETYPE2 = 'text'; % use 'spreadsheet' for .xlsx and 'text' for .tsv
FILENAME3 = "ODiSI 6000 Test_2023-03-27_14-37-23_ch4_full.tsv"; % file for third sensor
FILETYPE3 = 'text'; % use 'spreadsheet' for .xlsx and 'text' for .tsv
FIRST_TIME = 32; % first row to plot data for
FIRST_GAGE = 1531; % first column to plot data for
LAST_GAGE = 1853; % last column to plot data for
DATA_RATE = 10.4167; % number of frames per second to play movie

x_vals_all = [];
y_vals_all = [];
z_vals_all = [];

frame_count = 0;

% Bundle
BUNDLE_RADIUS = 0.0895; % [mm] (Assumes perfect triangle and 0.155 mm fiber diameter)
GAGE_PITCH = 0.65; % [mm] (We should be able to read this in from data file; can change later)
PHI_12 = 2*pi/3; % angle that fiber 2 is clockwise from the negative y axis (fiber 1's location)
PHI_13 = 2*pi/3; % angle that fiber 3 is counterclockwise from the negative y axis (fiber 1's location)
%% Read in TSV files
data1 = readmatrix(FILENAME1, 'FileType', FILETYPE1);
data2 = readmatrix(FILENAME2, 'FileType', FILETYPE2);
data3 = readmatrix(FILENAME3, 'FileType', FILETYPE3);
% Note: Data seems to actually start on column three of data1, data2, and
% data3
data1size = size(data1); % 2x1 matrix with dimensions of data1
data2size = size(data2); % 2x1 matrix with dimensions of data2
data3size = size(data3); % 2x1 matrix with dimensions of data3
%% Preallocate space to store movie
last_time = min([data1size(1),data2size(1), data3size(1)]); % last row of data to read
num_times = last_time-FIRST_TIME+1; % number of rows to read
v = VideoWriter('bundle_bending_test_2.mp4','MPEG-4'); % video file
v.FrameRate = DATA_RATE;
open(v);
%% Loop through all timestamps
figure
for time = FIRST_TIME:last_time
    %% Calculate plot points
    strains1 = data1(time, FIRST_GAGE:LAST_GAGE); % vector of strains at each gage
    strains2 = data2(time, FIRST_GAGE:LAST_GAGE); % vector of strains at each gage
    strains3 = data3(time, FIRST_GAGE:LAST_GAGE); % vector of strains at each gage
    num_strains = length(strains1); % note, we assume strains1, strains2, and strains3 are same length
    plot_points = zeros(3,num_strains+1); % matrix to hold x,y,z coords to plot
    base_rot = eye(3); % rotation matrix from current segment base frame to world frame
%     strains1_prev = 0;
%     strains2_prev = 0;
%     strains3_prev = 0;
    eps_1_prev = 0;
    eps_2_prev = 0;
    eps_3_prev = 0;
    % Loop through all gages
    for i = 1:num_strains
        eps_1 = (10^-6)*strains1(i);
        eps_2 = (10^-6)*strains2(i);
        eps_3 = (10^-6)*strains3(i);
        % Avoid NaN plotting issue -- set NaN's to the previous timestep's
        % value for that sensor
        if (isnan(eps_1))
            eps_1 = eps_1_prev;
        end
        if (isnan(eps_2))
            eps_2 = eps_2_prev;
        end
        if (isnan(eps_3))
            eps_3 = eps_3_prev;
        end
        eps_1_prev = eps_1;
        eps_2_prev = eps_2;
        eps_3_prev = eps_3;
        % Calculate intermediate variables
        eps_12 = eps_2-eps_1; % differential strain
        eps_13 = eps_3-eps_1; % differential strain
        eps_23 = eps_3-eps_2; % differential strain
        sig_1 = 1 + eps_1; % fraction of initial length 
        sig_2 = 1 + eps_2; % fraction of initial length
        sig_3 = 1 + eps_3; % fraction of initial length
        a = BUNDLE_RADIUS; % distance from fiber bundle center to each fiber
        % Calculate bending plane angle
        if (eps_12 == 0) && (eps_13 == 0) % straight
            alpha = 0; % bending plane angle
        else
            alpha = atan((eps_13*sin(PHI_12)+eps_12*sin(PHI_13))/...
            (eps_23-eps_13*cos(PHI_12)+eps_12*cos(PHI_13))); % bending plane angle
        end
        % Calculate bend radius
        r = inf;
        if (eps_12 ~= 0)
            r = (a/eps_12)*(sig_1*sin(alpha+PHI_12)-sig_2*sin(alpha));
        elseif (eps_13 ~= 0)
            r = (a/eps_13)*(sig_1*sin(alpha-PHI_13)-sig_3*sin(alpha));
        end
        % Correct angle if bend radius is negative
        if (r < 0)
            r = -r;
            alpha = alpha + pi;
        end
        % Calculate coords of segment tip point (in coords of segment base
        % frame)
        s = GAGE_PITCH; % arc length of segment
        theta = s/r; % angle that segment curves through
        if (r ~= inf)
            x = r*(1-cos(theta))*cos(alpha);
            y = r*(1-cos(theta))*sin(alpha);
            z = r*sin(theta); % z coord of next point
        else
            x = 0;
            y = 0;
            z = s;
        end
        % Convert segment tip point to world coords:
        % First, rotate local displacement from segment frame to world frame
        xyz_world = base_rot*[x;y;z];
        % Then, add on coords of segment base point
        plot_points(:,i+1) = plot_points(:,i)+xyz_world;
        % Then, calculate rotation matrix for next segment's base:
        % First, calculate in frame of current segment base
        local_rot = axang2rotm([cos(alpha-0.5*pi),sin(alpha-0.5*pi),0,-theta]);
        % Then, rotate into world frame
        base_rot_next = base_rot*local_rot;
        % Set current base rotation matrix equal to next for next segment
        base_rot = base_rot_next;
    end
    %% Plot shape
    xlabel('x pos (mm)')
    ylabel('y pos (mm)')
    zlabel('z pos (mm)')
    plot3(plot_points(1,:), plot_points(2,:), plot_points(3,:), 'b-o', 'LineWidth', 1)
    axis equal
    xlim([-500 500])
    ylim([-500 500])
    zlim([0 1000])
    view(120,10) % azimuth, elevation
    camup([1 0 0])
    grid on
    drawnow
    frame = getframe(gcf);
    writeVideo(v,frame);

    frame_count = frame_count + 1;

    x_vals_all = [x_vals_all; plot_points(1,:)];
    y_vals_all = [y_vals_all; plot_points(2,:)];
    z_vals_all = [z_vals_all; plot_points(3,:)];

%     fprintf(file_ID_x, '%f,', x_vals_all(frame_count,:));
%     fprintf(file_ID_y, '%f,', y_vals_all(frame_count,:));
%     fprintf(file_ID_z, '%f,', z_vals_all(frame_count,:));



    disp(size(x_vals_all))



end

writematrix(x_vals_all,"x_luna.csv")
writematrix(y_vals_all,"y_luna.csv")
writematrix(z_vals_all,"z_luna.csv")

close(v);
disp(frame_count)