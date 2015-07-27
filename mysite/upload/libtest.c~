#include<stdio.h>
#include<stdlib.h>
#include<string.h>
  
    
int collectFile(char* filePath,char* fileSavePath,int chunkAmount)  
{
    int i;
    char path[100];

    FILE * outfile, *infile;
    for(i=1;i<=chunkAmount;i++)
    {       
            sprintf(path,"%s%d",filePath,i);
            infile = fopen(path,"rb");
            outfile = fopen(fileSavePath, "a+" );

            unsigned char buf[1024]; 
            int rc;
            while( (rc = fread(buf,sizeof(unsigned char), 1024,infile)) != 0 )
            {
                fwrite( buf, sizeof( unsigned char ), rc, outfile );
            }
            fclose(infile);  
            fclose(outfile);
    } 
return 100;
}
