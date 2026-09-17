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
        int digitoVerificador = codigo.charAt(9) - '0';

        int soma = 0;
        for (int i = 0; i < sequencial.length(); i++) {
            int digito = sequencial.charAt(i) - '0';
            soma += digito * (i + 1);
        }
        for (char letra : letras.toCharArray()) {
            soma += (letra - 'A' + 1);
        }

        int dvCorreto = soma % 10;
        return digitoVerificador == dvCorreto ? "OK" : "DV";
    }
}
