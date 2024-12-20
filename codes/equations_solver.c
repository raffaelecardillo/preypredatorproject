#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Initial parameters 
double R, A, B, M;

// Function to read parameters from a file
void read_parameters(const char *filename, double *R, double *A, double *B, double *M) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Error: Could not open file %s\n", filename);
        exit(1);
    }
    fscanf(file, "%lf %lf %lf %lf", R, A, B, M);
    fclose(file);
    printf("Parameters loaded: R = %f, A = %f, B = %f, M = %f\n", *R, *A, *B, *M);
}

//Function creating a peak at a given t
double gaussian_peak(double t, double t0, double amplitude, double sigma) {
    return amplitude * exp(-pow(t - t0, 2) / (2 * pow(sigma, 2)));
}

// Differential equation for dx/dt (prey population)
double dxdt(double t, double x, double y, double amplitude, double t0) {
    double Sx = gaussian_peak(t, t0, amplitude, 1.0);
    return R * x - A * x * y + Sx; // Added environmental shock term Sx
}

// Differential equation for dy/dt (predator population)
double dydt(double t, double x, double y) {
    return B * x * y - M * y;
}

// Runge-Kutta 4th Order Method
void rk4(double (*dxdt)(double, double, double, double, double), double (*dydt)(double, double, double),
         double t, double *x, double *y, double h,double amplitude, double t0) {
    double k1x, k2x, k3x, k4x;
    double k1y, k2y, k3y, k4y;

    // Calculate k1
    k1x = h * dxdt(t, *x, *y, amplitude,t0);
    k1y = h * dydt(t, *x, *y);

    // Calculate k2
    k2x = h * dxdt(t + h / 2, *x + k1x / 2, *y + k1y / 2, amplitude, t0);
    k2y = h * dydt(t + h / 2, *x + k1x / 2, *y + k1y / 2);

    // Calculate k3
    k3x = h * dxdt(t + h / 2, *x + k2x / 2, *y + k2y / 2, amplitude, t0);
    k3y = h * dydt(t + h / 2, *x + k2x / 2, *y + k2y / 2);

    // Calculate k4
    k4x = h * dxdt(t + h, *x + k3x, *y + k3y, amplitude,t0);
    k4y = h * dydt(t + h, *x + k3x, *y + k3y);

    // Update values of x and y
    *x += (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0;
    *y += (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Usage: %s <t0> <amplitude>\n", argv[0]);
        return 1;
    }
    double t0 = atof(argv[1]); // Parse the time for the Gaussian peak
    double amplitude = atof(argv[2]);// Parse the time fot the Gaussian peak
    printf("%f,%f",t0,amplitude);
    read_parameters("parameters.txt", &R, &A, &B, &M);
    // Initial conditions
    double t = 1845.0;         // Start time
    double x = 70000;       // Initial prey population
    double y = 2600;        // Initial predator population
    double h = 0.25;        // Time for rk4 (3 month)
    double t_max = 1935.0;    // End time (90 years)
// Buffer for the dynamic file path
char filepath[100];

// Create the dynamic file path
if (t0 == 1845) {
    snprintf(filepath, sizeof(filepath), "model.csv");
} else {
    snprintf(filepath, sizeof(filepath), "model(with_peak_at_t=%.1f).csv", t0);
}
// Open the file using the dynamically created file path
FILE *fp = fopen(filepath, "w");
    if (!fp) {
        printf("Error opening file.\n");
        return 1;
    }
    fprintf(fp, "Time,Prey,Predator\n");

    // Time-stepping loop
    while (t < t_max) {
        if (x < 0) x = 0;
        if (y < 0) y = 0;
        fprintf(fp, "%f,%f,%f\n", t, x, y);
        rk4(dxdt, dydt, t, &x, &y, h, amplitude, t0);
        t += h;
    }

    fclose(fp);
    printf("Simulation complete. Results saved to '%s'.\n",filepath);
    return 0;
}


