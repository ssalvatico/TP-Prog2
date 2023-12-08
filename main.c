#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int sanitizador(FILE* entrada, FILE* salida){
    if (entrada == NULL){
        printf("Error: el archivo de entrada es vacio");
        return 0;
    }
    int punto = 0;
    int carac = fgetc(entrada);

    while(carac != EOF){
        if(isalpha(carac)){
            fputc((tolower(carac)), salida);
                carac = fgetc(entrada);
        }
        else if(carac == '.'){
            fputc('\n', salida);
            carac = fgetc(entrada);
            punto = 1;
        }
        else if (isspace(carac)){
            if (punto == 0){
                fputc(' ', salida);
            }
            else if (punto == 1){
                punto = 0;
            }
            carac = fgetc(entrada);
        }

        else {
            carac = fgetc(entrada);
            }
    }
    return 1;
}

void creadorArchivos(char nombre[]){
    char ruta[100];
    snprintf(ruta, sizeof(ruta), "cd ./Textos/%s && ls > ../../textos.txt", nombre);
    system(ruta);
}

void creadorSalida(char nombre[]){

    char ruta[100];
    snprintf(ruta, sizeof(ruta), "textos.txt");
    
    FILE* archNombres = fopen(ruta, "r");
    if (archNombres == NULL){
        perror("Error al abrir el archivo\n");
        return;
    }
    char creador[100];
    snprintf(creador, sizeof(creador), "./Entradas/%s.txt", nombre);
    FILE* salida = fopen(creador, "w");

    char lineas[255];
    char* lineaArchivos = fgets(lineas, sizeof(lineas), archNombres);
    while(lineaArchivos != NULL){
        lineas[strlen(lineas) - 1] = '\0';

        char direccion[300];
        snprintf(direccion,sizeof(direccion),"./Textos/%s/%s",nombre,lineas);

        FILE* entrada = fopen(direccion, "r");
        if (entrada != NULL) {
            sanitizador(entrada, salida);
            fclose(entrada);
        } else {
            printf("Error: el archivo de entrada es vacio\n");
            break;
            fclose(entrada);
            fclose(salida);
            return;
        }
        lineaArchivos = fgets(lineas, sizeof(lineas), archNombres);
        
    }
    fclose(archNombres);
    fclose(salida);
    return;
}

void callPython(char nombre[]){
    char comando[100];
    snprintf(comando, sizeof(comando), "python3 programa.py %s", nombre);
    system(comando);
}

int main(int argc, char *argv[]){ //arg count , arg value

    creadorArchivos(argv[1]);
    creadorSalida(argv[1]);
    callPython(argv[1]);
    return 0;
}