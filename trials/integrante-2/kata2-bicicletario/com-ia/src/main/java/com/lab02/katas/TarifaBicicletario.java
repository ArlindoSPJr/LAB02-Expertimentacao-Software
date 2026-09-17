package com.lab02.katas;

public final class TarifaBicicletario {

    private TarifaBicicletario() {
    }

    private static final int TETO_CENTAVOS = 2000;
    private static final int TARIFA_FIXA_CENTAVOS = 300;
    private static final int BLOCO_CENTAVOS = 150;
    private static final int BLOCO_MINUTOS = 30;

    public static int calcularCentavos(int minutos) {
        if (minutos < 0) {
            throw new IllegalArgumentException("minutos não pode ser negativo: " + minutos);
        }
        int centavos;
        if (minutos <= 20) {
            centavos = 0;
        } else if (minutos <= 60) {
            centavos = TARIFA_FIXA_CENTAVOS;
        } else {
            int blocos = (minutos - 60 + BLOCO_MINUTOS - 1) / BLOCO_MINUTOS;
            centavos = TARIFA_FIXA_CENTAVOS + blocos * BLOCO_CENTAVOS;
        }
        return Math.min(centavos, TETO_CENTAVOS);
    }
}
