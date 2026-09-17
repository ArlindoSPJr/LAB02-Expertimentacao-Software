package com.lab02.katas;

import java.util.ArrayList;
import java.util.List;

public final class SensorCompactador {

    private SensorCompactador() {
    }

    public static List<String> compactar(int[] leituras, int tolerancia) {
        if (tolerancia < 0) {
            throw new IllegalArgumentException("tolerancia nao pode ser negativa: " + tolerancia);
        }

        List<String> faixas = new ArrayList<>();
        if (leituras.length == 0) {
            return faixas;
        }

        int inicio = 0;
        int valorAbertura = leituras[0];
        int min = leituras[0];
        int max = leituras[0];

        for (int i = 1; i < leituras.length; i++) {
            int leitura = leituras[i];
            if (Math.abs(leitura - valorAbertura) <= tolerancia) {
                min = Math.min(min, leitura);
                max = Math.max(max, leitura);
                continue;
            }
            faixas.add(formatarFaixa(inicio, i - 1, min, max));
            inicio = i;
            valorAbertura = leitura;
            min = leitura;
            max = leitura;
        }
        faixas.add(formatarFaixa(inicio, leituras.length - 1, min, max));

        return faixas;
    }

    private static String formatarFaixa(int inicio, int fim, int min, int max) {
        return inicio + "-" + fim + ":" + min + ".." + max;
    }
}
