package com.lab02.katas;

public final class SkuValidator {

    private static final String FORMATO = "FORMATO";
    private static final String DV_INVALIDO = "DV";
    private static final String OK = "OK";

    private SkuValidator() {
    }

    public static String validar(String codigo) {
        if (codigo == null || !bateLayout(codigo)) {
            return FORMATO;
        }

        String letras = codigo.substring(0, 3);
        String digitos = codigo.substring(4, 8);
        int digitoVerificador = codigo.charAt(9) - '0';

        int soma = 0;
        for (int k = 1; k <= 4; k++) {
            soma += (digitos.charAt(k - 1) - '0') * k;
        }
        for (int i = 0; i < letras.length(); i++) {
            soma += letras.charAt(i) - 'A' + 1;
        }

        int esperado = soma % 10;
        return digitoVerificador == esperado ? OK : DV_INVALIDO;
    }

    private static boolean bateLayout(String codigo) {
        if (codigo.length() != 10) {
            return false;
        }
        if (codigo.charAt(3) != '-' || codigo.charAt(8) != '-') {
            return false;
        }
        for (int i = 0; i < 3; i++) {
            char c = codigo.charAt(i);
            if (c < 'A' || c > 'Z') {
                return false;
            }
        }
        for (int i = 4; i < 8; i++) {
            char c = codigo.charAt(i);
            if (c < '0' || c > '9') {
                return false;
            }
        }
        char verificador = codigo.charAt(9);
        return verificador >= '0' && verificador <= '9';
    }
}
