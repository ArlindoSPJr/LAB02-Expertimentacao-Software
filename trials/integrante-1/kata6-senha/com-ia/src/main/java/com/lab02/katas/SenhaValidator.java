package com.lab02.katas;

public final class SenhaValidator {

    private SenhaValidator() {
    }

    public static String classificar(String senha) {
        if (senha == null || senha.length() < 6 || senha.length() > 12) {
            return "INVALIDA";
        }
        for (char c : senha.toCharArray()) {
            if (!Character.isLetterOrDigit(c) || c > 127) {
                return "INVALIDA";
            }
        }

        boolean temMinuscula = false;
        boolean temMaiuscula = false;
        boolean temDigito = false;
        boolean temRepeticaoAdjacente = false;

        for (int i = 0; i < senha.length(); i++) {
            char c = senha.charAt(i);
            if (Character.isLowerCase(c)) {
                temMinuscula = true;
            } else if (Character.isUpperCase(c)) {
                temMaiuscula = true;
            } else if (Character.isDigit(c)) {
                temDigito = true;
            }
            if (i > 0 && senha.charAt(i - 1) == c) {
                temRepeticaoAdjacente = true;
            }
        }

        int classes = (temMinuscula ? 1 : 0) + (temMaiuscula ? 1 : 0) + (temDigito ? 1 : 0);
        int score = Math.max(1, classes - (temRepeticaoAdjacente ? 1 : 0));

        switch (score) {
            case 3:
                return "FORTE";
            case 2:
                return "MEDIA";
            default:
                return "FRACA";
        }
    }
}
