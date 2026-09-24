package com.lab02.katas;

public final class TarifaBicicletario {

    private TarifaBicicletario() {
    }

    private static final int TETO_DIARIO_CENTAVOS = 2000;
    private static final int TARIFA_FIXA_CENTAVOS = 300;
    private static final int TARIFA_BLOCO_CENTAVOS = 150;
    private static final int BLOCO_MINUTOS = 30;

    public static int calcularCentavos(int minutos) {
        if (minutos < 0) {
            throw new IllegalArgumentException("minutos não pode ser negativo");
        }
        if (minutos <= 20) {
            return 0;
        }
        if (minutos <= 60) {
            return TARIFA_FIXA_CENTAVOS;
        }
        int minutosExtras = minutos - 60;
        int blocos = (minutosExtras + BLOCO_MINUTOS - 1) / BLOCO_MINUTOS;
        int total = TARIFA_FIXA_CENTAVOS + blocos * TARIFA_BLOCO_CENTAVOS;
        return Math.min(total, TETO_DIARIO_CENTAVOS);
    }
}
