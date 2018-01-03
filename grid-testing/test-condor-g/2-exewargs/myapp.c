#include <stdlib.h>
#include <math.h>

main (int argc, char **argv)
{
  char name[100];
  double angle, sin_angle;

  if (argc == 3)
    {
      strcpy (name, argv[1]);	/* 1st argument is may name */
      angle = atof (argv[2]);	/* second argument is an angle */
      //   printf(" name,angle = %s %g \n",name,angle);
    }
  else
    {
      printf
	("Usage: myapp name angle(degrees)  \n Rerun with the correct number of arguments.\n");
      exit (-1);
    }
  sin_angle = sin (angle / 180. * M_PI);
  printf ("Hi %s. The sine of %g is %g \n", name, angle, sin_angle);
}
