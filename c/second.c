#include <stdio.h>
#include <stdlib.h>

void sort(int *list, int size){
  for(int i = 0; i < size; i++){
    for(int x = i+1; x < size; x++){
      if(list[x] < list[i]){
        int temp = list[x];
        list[x] = list[i];
        list[i] = temp;
      }
    }
  }
}

int min(int argc, char **argv){
  if(argc != 2){
    return 1;
  }

  FILE *file;
  int * listE, * listO;
  int eSize = 0, oSize = 0;

  file = fopen(argv[1], "r");
  int size;
  fscanf(file, "%d", &size);
  listE = malloc(sizeof(int) * size);
  listO = malloc(sizeof(int) * size);

  for(int i = 0; i < size; i++){
    int x;
    fscanf(file, "%d", &x);
    if(x%2 == 0){
      listE[eSize] = x;
      eSize++;
    }
    else{
      listO[oSize] = x;
      oSize++;
    }
  }
  sort(listE, eSize);
  sort(listO, oSize);

  for(int i = 0; i < eSize; i++){
    printf("%d\t", listE[i]);
  }
  for(int i = 0; i < oSize; i++){
    printf("%d", listO[i]);
    if(i+1 < oSize){
      printf("\t");
    }
  }

  free(listE);
  free(listO);
  fclose(file);

  return 0;
}
