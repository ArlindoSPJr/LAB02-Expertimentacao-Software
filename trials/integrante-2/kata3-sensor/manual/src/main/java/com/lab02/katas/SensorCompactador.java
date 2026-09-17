package com.lab02.katas;

import java.util.ArrayList;
import java.util.List;

public final class SensorAgrupador {

    private SensorAgrupador() {
    }

    public static List<String> compactar(int[] leituras, int tolerancia) {

        if (tolerancia < 0) {
            throw new IllegalArgumentException();
        }

        List<String> resultado = new ArrayList<>();

        if (leituras.length == 0) {
            return resultado;
        }

        int inicioGrupo = 0;

        while (inicioGrupo < leituras.length) {

            int referencia = leituras[inicioGrupo];
            int menor = referencia;
            int maior = referencia;

            int fimGrupo = inicioGrupo;

            while (fimGrupo + 1 < leituras.length
                    && dentroDaTolerancia(leituras[fimGrupo + 1], referencia, tolerancia)) {

                fimGrupo++;

                menor = Math.min(menor, leituras[fimGrupo]);
                maior = Math.max(maior, leituras[fimGrupo]);
            }

            resultado.add(formatarGrupo(inicioGrupo, fimGrupo, menor, maior));

            inicioGrupo = fimGrupo + 1;
        }

        return resultado;
    }

    private static boolean dentroDaTolerancia(int valor, int referencia, int tolerancia) {
        return Math.abs(valor - referencia) <= tolerancia;
    }

    private static String formatarGrupo(int inicio, int fim, int min, int max) {
        return inicio + "-" + fim + ":" + min + ".." + max;
    }
}