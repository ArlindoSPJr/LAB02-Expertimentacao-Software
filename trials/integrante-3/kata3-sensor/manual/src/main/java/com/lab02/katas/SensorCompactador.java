package com.lab02.katas;

import java.util.ArrayList;
import java.util.List;

public final class SensorCompactador {

    private SensorCompactador() {
    }

    public static List<String> compactar(int[] leituras, int tolerancia) {

        if (tolerancia < 0) {
            throw new IllegalArgumentException();
        }

        List<String> resultado = new ArrayList<>();

        if (leituras.length == 0) {
            return resultado;
        }

        int inicio = 0;
        int abertura = leituras[0];
        int min = leituras[0];
        int max = leituras[0];

        for (int i = 1; i < leituras.length; i++) {

            if (Math.abs(leituras[i] - abertura) <= tolerancia) {

                if (leituras[i] < min) {
                    min = leituras[i];
                }

                if (leituras[i] > max) {
                    max = leituras[i];
                }

            } else {

                resultado.add(inicio + "-" + (i - 1) + ":" + min + ".." + max);

                inicio = i;
                abertura = leituras[i];
                min = leituras[i];
                max = leituras[i];
            }
        }

        resultado.add(inicio + "-" + (leituras.length - 1) + ":" + min + ".." + max);

        return resultado;
    }
}
