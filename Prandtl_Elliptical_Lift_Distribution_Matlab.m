% Configure logging
logFile = 'lift_distribution.log';
diary(logFile);

% Define parameters in imperial units (inches)
span = 15 * 12;  % Total wingspan in inches
lift_coefficient = 1.165;  % Lift coefficient (CL)
rho = 0.0023769;  % Air density in slugs/ft³
velocity = 38.0;  % Flight velocity in feet per second
root_chord = 3 * 12;  % Root chord length in inches
tip_chord = 1 * 12;  % Tip chord length in inches

fprintf('Parameters: span=%d in, lift_coefficient=%.3f, rho=%.7f, velocity=%.1f ft/s, root_chord=%d in, tip_chord=%d in\n', ...
    span, lift_coefficient, rho, velocity, root_chord, tip_chord);

% Find lift per unit span and load at specific positions
positions = [0.166667, 0.5, 0.833333, 1.16667, 1.5, 1.83333, 2.16667, 2.5, 2.83333, 3.16667, 3.458333, 3.75, 4.08333, 4.41667, 4.75, 5.08333, 5.41667, 5.75, 6.08333, 6.41667, 6.75, 7.041667, 7.16667] * 12;  % Example positions in inches
lifts_and_chords = zeros(length(positions), 2);
for i = 1:length(positions)
    [lifts_and_chords(i, 1), lifts_and_chords(i, 2)] = lift_at_position(positions(i), span, lift_coefficient, rho, velocity, root_chord, tip_chord);
end

% Add zero lift at the wingtip
lifts_and_chords(end, 1) = 0;

% Calculate the load at each position
loads = zeros(length(positions), 1);
for i = 1:length(positions) - 1
    delta_pos = positions(i + 1) - positions(i);
    loads(i) = lifts_and_chords(i, 1) * delta_pos;
end
% For the last position, use the difference with the previous position
loads(end) = lifts_and_chords(end, 1) * (positions(end) - positions(end - 1));

% Calculate the shear force at each position
shear_forces = zeros(length(positions), 1);
for i = length(positions):-1:1
    if i == length(positions)
        shear_forces(i) = 0;  % Shear force at the wing tip is zero
    else
        shear_forces(i) = shear_forces(i + 1) + loads(i);
    end
end

% Calculate the bending moment at each position
bending_moments = zeros(length(positions), 1);
for i = length(positions):-1:1
    if i == length(positions)
        bending_moments(i) = 0;  % Bending moment at the wing tip is zero
    else
        delta_pos = positions(i + 1) - positions(i);
        bending_moments(i) = bending_moments(i + 1) + shear_forces(i) * delta_pos;
    end
end

% Plot the lift distribution
figure;
plot(positions, lifts_and_chords(:, 1), '-o');
xlabel('Spanwise Position (in)');
ylabel('Lift per Unit Span (lb/in)');
title('Figure 1: Elliptical Lift Distribution at Specific Positions');
grid on;

% Plot the load distribution
figure;
plot(positions, loads, '-o', 'Color', 'b');
xlabel('Spanwise Position (in)');
ylabel('Load (lb)');
title('Figure 2: Load Distribution at Specific Positions');
grid on;

% Plot the shear force distribution
figure;
plot(positions, shear_forces, '-o', 'Color', 'r');
xlabel('Spanwise Position (in)');
ylabel('Shear Force (lb)');
title('Figure 3: Shear Force Distribution at Specific Positions');
grid on;

% Plot the bending moment distribution
figure;
plot(positions, bending_moments, '-o', 'Color', 'g');
xlabel('Spanwise Position (in)');
ylabel('Bending Moment (lb-in)');
title('Figure 4: Bending Moment Distribution at Specific Positions');
grid on;

% Log the lift, chord length, load, shear force, and bending moment for each position
for i = 1:length(positions)
    fprintf('Lift per unit span at %.2f in: %.2f lb/in, Chord length: %.2f in, Load: %.2f lb, Shear force: %.2f lb, Bending moment: %.2f lb-in\n', ...
        positions(i), lifts_and_chords(i, 1), lifts_and_chords(i, 2), loads(i), shear_forces(i), bending_moments(i));
end

diary off;

% Function to find lift at a specific spanwise position
function [lift, chord_length] = lift_at_position(y_position, span, lift_coefficient, rho, velocity, root_chord, tip_chord)
    b = span / 2;  % Semi-span
    taper_ratio = tip_chord / root_chord;
    chord_length = root_chord * (1 - (1 - taper_ratio) * y_position / b);  % Linear taper
    lift = (4 * lift_coefficient * rho * velocity^2 * chord_length) / (pi * span) * sqrt(1 - (y_position / b)^2);
end