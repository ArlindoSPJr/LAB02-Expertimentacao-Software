package com.lab02.katas;

import java.util.regex.Pattern;

public final class SkuValidator {

    private static final Pattern FORMATO = Pattern.compile("^[A-Z]{3}-[0-9]{4}-[0-9]$");

    private SkuValidator() {
    }

    public static String validar(String codigo) {
        if (codigo == null || !FORMATO.matcher(codigo).matches()) {
            return "FORMATO";
        }

        String letras = codigo.substring(0, 3);
        String sequencial = codigo.substring(4, 8);
        int digitoInformado = codigo.charAt(9) - '0';

        int soma = 0;
        for (int k = 1; k <= 4; k++) {
            int digito = sequencial.charAt(k - 1) - '0';
            soma += digito * k;
        }
        for (int i = 0; i < letras.length(); i++) {
            soma += letras.charAt(i) - 'A' + 1;
        }

        int digitoEsperado = soma % 10;
        if (digitoInformado != digitoEsperado) {
            return "DV";
        }
        return "OK";
    }
}
