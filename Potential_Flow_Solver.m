%%% Potential Flow Solver Assignment %%%
% Jon Borman
% AEE 558
% 2011-10-10
clear;clc;clf

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Input data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

n = 100;                            % number of cells (r and theta)
tol = 1e-8;                         % convergence tolerance 
max_iter = 1e4;                     % max number of iterations

w = 2/(1+sqrt(1-cos(pi/(n+1))*cos(pi/(n+1))));  % omega optimum
M = n-1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

R_cyl = 0.5;                        % radius of the cylinder
R_max = 10;                         % max radius

u_inf = 1;                          % free-stream velocity

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Create Mesh %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dr = (R_max-R_cyl)/M;               % size of r
dth = 2*pi/M;                       % size of theta

r(1) = R_cyl;
r(n) = R_max;

th(1) = 0;
th(n) = 2*pi;

psi(1,1) = 0;                       % First streamline = 0
psi(n,1) = 0;                       % First streamline

for j=2:M
    
    r(j) = R_cyl+(j-1)*dr;
    th(j) = (j-1)*dth;
    psi(n,j) = u_inf*R_max*sin(th(j));
    
end

psi(n,n) = 0;                       % First Streamline

%%%%%%%%%%%%%%%%%%%%% Descritized Laplace Equation %%%%%%%%%%%%%%%%%%%%%%%%

iter = 1;                           % Begin iteration counter
res(1,1) = 1;                       % Create initial residual

while res > tol & iter < max_iter
    
    for j=2:M
        
        for k=2:M
            
            dpsi(j,k)=(1/r(j)*(psi(j+1,k)-psi(j-1,k))/(2*dr)+...
                (psi(j-1,k)+psi(j+1,k))/dr^2+1/r(j)^2*(psi(j,k+1)+...
                psi(j,k-1))/dth^2)/(2/dr^2+2/(r(j)^2*dth^2))-psi(j,k);
            
            psi(j,k)=psi(j,k)+w.*dpsi(j,k);
            
        end
    
    end
    
    p(1,1) = 0;
    p(:,iter+1) = norm(psi(:,:));           % p is psi at each iteration
      
    res(:,iter)=norm(p(:,iter+1)-p(:,iter),inf)/norm(p(:,iter+1),inf);

    iter = iter + 1;
      
end

%%%%%%%%%%%%%%%%%%%%%%%%%% Descritize Velocity %%%%%%%%%%%%%%%%%%%%%%%%%%%%

for j=1:n     % Angular Nodes
    
    for k=1:n          % Radial Nodes
        
        if j == 1
            u_th(j,k) = -(3*psi(j,k)-4*psi(j+1,k)+psi(j+2,k))/(2*dr);
        elseif j == n
            u_th(j,k) = -(-3*psi(j,k)+4*psi(j-1,k)-psi(j-2,k))/(2*dr);
        else
            u_th(j,k) = -(psi(j+1,k)-psi(j-1,k))/(2*dr);
        end
        
        if k == 1
            u_r(j,k) = 1/r(j)*(3*psi(j,k)-4*psi(j,k+1)+psi(j,k+2))...
                /(2*dth);
        elseif k == n
            u_r(j,k) = 1/r(j)*(-3*psi(j,k)+4*psi(j,k-1)-psi(j,k-2))...
                /(2*dth);
        else
            u_r(j,k) = 1/r(j)*(psi(j,k+1)-psi(j,k-1))/(2*dth);
        end
        
        u_1(j,k) = u_r(j,k)*cos(k*dth) - u_th(j,k)*sin(k*dth);
        u_2(j,k) = u_r(j,k)*sin(k*dth) + u_th(j,k)*cos(k*dth);
    
    end
    
end



%%%%%%%%%%%%%%%%%%%%%%%%%% Calculate Pressure %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[X,Y] = pol2cart(th,r);
[theta,rho] = meshgrid(th,r);
[x,y] = pol2cart(theta,rho);

Cp_num = 1-(u_1.^2+u_2.^2)/u_inf^2;
Cp_num_sfc = Cp_num(1,:);

Cp_ex = 1-4*sin(th).^2;

%%%%%%%%%%%%%%%%%%%%%%%% Prepare Data for Output %%%%%%%%%%%%%%%%%%%%%%%%%%

fprintf('%i iterations were required for a tolerance of %3.2e \n',iter,tol)

iterations = 1:iter-1;
 
E = norm(Cp_ex-Cp_num_sfc)/n;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Plots %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

figure(1)                       
semilogy(iterations,res)
xlabel('Number of Iterations')
ylabel('Residual')
title('Convergence History')

figure(2)
hold on
plot(th,Cp_num_sfc,'-b');
plot(th,Cp_ex,'-r');
legend('n = 50','exact');
xlabel('\theta');
ylabel('C_p');
title('C_p vs \theta');
set(gca,'XTick',0:pi/4:2*pi)
set(gca,'XTickLabel',{'0','pi/4','pi/2','3pi/4','pi','5pi/4','3pi/2',...
    '7pi/4','2pi'})
hold off

figure(3)
contourf(x,y,Cp_num);           


    
    