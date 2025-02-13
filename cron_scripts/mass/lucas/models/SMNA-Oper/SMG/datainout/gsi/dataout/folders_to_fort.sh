#!/bin/bash

origem="."

destino="./fort_files"

mkdir -p "$destino"

for pasta in "$origem"/*; do
    if [ -d "$pasta" ]; then
        
        data=$(basename "$pasta")
        
        
        if [ -f "$pasta/fort.220" ]; then
            
            cp "$pasta/fort.220" "$destino/$data.220"
            echo "Arquivo $data.220 copiado com sucesso!"
        else
            echo "Arquivo fort.220 não encontrado em $pasta"
        fi
    fi
done
