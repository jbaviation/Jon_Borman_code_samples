% DIAMOND STAR DA40 Performance

clc
clf

% Constants
W_Load = 20.2; % Wing Loading (W/S) units: lb/ft^2
W = 3600; % Max gross Weight, units: lbs
S_ref = 178.3; % Wing Planform Area, units: ft^2
S_wet = 178.3*2+12*2.5*2+2*pi*27.5*1.8; % Estimated Wetted Area, units: ft^2
b = 36.2; % Span, units: ft
AR = b^2/S_ref; % Aspect Ratio
c = b/AR; % Chord, units: ft
ep = 1.78*(1-0.045*AR^0.68)-0.65; % Oswald Efficiency Factor
rho_8k = 1.86e-3; % density at 8 kft, units: slug/ft^3
mu_8k = 3.575e-7; % viscosity at 8 kft, units: lb*s/ft^2
rho_sl = 2.378e-3; % density at sea level, units: slug/ft^3
P = 300 * 550; % max power, units: ft*lbf/s
eta = 0.8; % propeller efficiency
k = 1/(pi*AR*ep);

v_75 = 172 * 1.6867; % velocity at 75% power, units: ft/s
v_65 = 164 * 1.6867; % velocity at 65% power, units: ft/s
v_55 = 155 * 1.6867; % velocity at 55% power, units: ft/s

V_S0 = 57 * 1.6867; % Stall Speed in Landing Config, units: ft/s
V_S1 = 60 * 1.6867; % Stall Speed Clean, units: ft/s
V_x = 80 * 1.6867; % Best Angle of Climb, units: ft/s
V_y = 91 * 1.6867; % Best Rate of Climb, units: ft/s

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% CL = (W/S)*1/(1/2*rho*v^2)
% D = P*eta/V 
% CD = D / (1/2*rho*v^2*S_wet)
% CDi = CL^2/(pi*AR*ep)
% CDo = CD - CDi
% L/D = W / D

% Coefficient of Lift (CL) for each power setting (unitless)
CL_75 = W_Load / (1/2*rho_8k*v_75^2); % 75% power
CL_65 = W_Load / (1/2*rho_8k*v_65^2); % 65% power
CL_55 = W_Load / (1/2*rho_8k*v_55^2); % 55% power
CL_Vx = W_Load / (1/2*rho_sl*V_x^2); % CL at Vx
CL_Vy = W_Load / (1/2*rho_sl*V_y^2); % CL at Vy

% Drag Force for each power setting (units: lbf)
D_75 = 0.75*P * eta / v_75; % 75% power
D_65 = 0.65*P * eta / v_65; % 65% power
D_55 = 0.55*P * eta / v_55; % 55% power
D_Vx = P * eta / V_x;
D_Vy = P * eta / V_y;

% Coefficient of Drag (CD) for each power setting (unitless)
CD_75 = D_75 / (1/2*rho_8k*v_75^2*S_wet);
CD_65 = D_65 / (1/2*rho_8k*v_65^2*S_wet);
CD_55 = D_55 / (1/2*rho_8k*v_55^2*S_wet);
CD_Vx = D_Vx / (1/2*rho_sl*V_x^2*S_wet);
CD_Vy = D_Vy / (1/2*rho_sl*V_y^2*S_wet);

% Lift Induced Drag Coefficient (CDi = k*CL^2)
CDi_75 = k * CL_75^2;
CDi_65 = k * CL_65^2;
CDi_55 = k * CL_55^2;
CDi_Vx = k * CL_Vx^2;
CDi_Vy = k * CL_Vy^2;

% Parasitic Drag Coefficient (CDo)
CDo_75 = CD_75 - CDi_75;
CDo_65 = CD_65 - CDi_65;
CDo_55 = CD_55 - CDi_55;
CDo_Vx = CD_Vx - CDi_Vx;
CDo_Vy = CD_Vy - CDi_Vy;

% Lift to Drag Ratio (L_D)
L_D_75 = W / D_75;
L_D_65 = W / D_65;
L_D_55 = W / D_55;
L_D_Vx = W / D_Vx;
L_D_Vy = W / D_Vy;

% Max CL Values
CL_max = W_Load / (1/2*rho_sl*V_S1^2);
CDi_max = k * CL_max^2;
CDo_max = 1e-8; % Estimation, very small number
CD_max = CDi_max + CDo_max;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

CL = [CL_75,CL_65,CL_55,CL_Vy,CL_Vx,CL_max];
CD = [CD_75,CD_65,CD_55,CD_Vy,CD_Vx,CD_max];
CDi = [CDi_75,CDi_65,CDi_55,CDi_Vy,CDi_Vx,CDi_max];
CDo = [CDo_75,CDo_65,CDo_55,CDo_Vy,CDo_Vx,CDo_max];

Ctot = [CL;CD;CDi;CDo];

hold on
plot(CL,CDi,'b-o')
plot(CL,CDo,'r-o')
plot(CL,CD,'k-o')

title('C_L vs C_D')
ylabel('C_D')
xlabel('C_L')
legend('C_D_i','C_D_o','C_D')