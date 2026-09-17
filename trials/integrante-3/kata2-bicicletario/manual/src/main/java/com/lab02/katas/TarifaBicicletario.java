package com.lab02.katas;

public final class TarifaBicicletario {

    private TarifaBicicletario() {
    }

    public static int calcularCentavos(int minutos) {

        if (minutos < 0) {
            throw new IllegalArgumentException();
        }

        if (minutos <= 20) {
            return 0;
        }

        if (minutos <= 60) {
            return 300;
        }

        int extra = minutos - 60;
        int blocos = (extra + 29) / 30;

        int valor = 300 + 150 * blocos;

        if (valor > 2000) {
            valor = 2000;
        }

        return valor;
    }
}
