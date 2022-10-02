#include <stdio.h>
#include <math.h>

#define ANGLE_RESOLUTION 500    // Number of angle points to calculate

int main(void)
{
   int numElements = 4;         // Number of array elements
   double spacing = 0.2;        // Element separation in metres
   double freq = 1000.0;        // Signal frequency in Hz 
   double speedSound = 343.0;   // m/s

   int a;
   int i;

   // Iterate through arrival angle points
   for (a=0 ; a<ANGLE_RESOLUTION ; a++)
   {
      // Calculate the planewave arrival angle
      double angle = -90 + 180.0 * a / (ANGLE_RESOLUTION-1);
      double angleRad = M_PI * (double) angle / 180;

      double realSum = 0;
      double imagSum = 0;

      // Iterate through array elements
      for (i=0 ; i<numElements ; i++)
      {
         // Calculate element position and wavefront delay
         double position = i * spacing;
         double delay = position * sin(angleRad) / speedSound;
         double num1 = 2.0 * M_PI * freq * delay;
         // Add Wave
         realSum = realSum + cos(num1);
         imagSum = imagSum + sin(num1);
      }

      double output = sqrt(realSum * realSum + imagSum * imagSum) / numElements;
      double logOutput = 20 * log10(output);
      if (logOutput < -50) logOutput = -50;
      printf("%d %f %f %f %f\n", a, angle, angleRad, output, logOutput);
   }

   return 0;
}