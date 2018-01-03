#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#define MAXLINE 1024


main (int argc, char **argv)
{
  char filename[50],output_filename[50];
  double angle, sin_angle;
  int i;
  char line[MAXLINE];
  float numbers[5],sum;
  FILE *fp1,*fp2;
 

  if (argc == 2)
    {
      strcpy (filename, argv[1]);	/* 1st argument is input filename */
    }
  else
    {
      printf
	("Usage: test-input-files input-file-name \n Rerun and provide the input files name.\n");
      exit (-1);
    }
  

                 if ((fp1 = fopen(filename,"r")) ==0)
                 {
                     fprintf(stderr,"Error opening input file %s . exiting ... \n",filename);
                     exit(-1);
                 }
                  for (i=0; i<5; i++) {
                     fgets(line,MAXLINE,fp1);
                    // printf("i,line = %d %s \n",i,line);
                     sscanf(line,"%f", &numbers[i]);
                 }
                 fclose(fp1);
		 sum=0;
                  for (i=0; i<5; i++)
                    sum+=numbers[i];
		/* Open the output file for the results */
		sprintf(output_filename,"%s.output",filename);
		 if ((fp2 = fopen(output_filename,"w")) ==0)
                 {
                     fprintf(stderr,"Error opening output file %s . exiting ... \n",output_filename);
                     exit(-1);
                 }
                 fprintf(fp2,"The sum of the numbers in file: %s is %f \n",filename,sum);
                 fclose(fp2);
 }
