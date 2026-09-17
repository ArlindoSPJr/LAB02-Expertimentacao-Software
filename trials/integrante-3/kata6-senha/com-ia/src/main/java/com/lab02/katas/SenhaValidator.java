package com.lab02.katas;

public final class SenhaValidator {

    private SenhaValidator() {
    }

    public static String classificar(String senha) {
        if (senha == null || senha.length() < 6 || senha.length() > 12) {
            return "INVALIDA";
        }
        for (char c : senha.toCharArray()) {
            boolean valido = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9');
            if (!valido) {
                return "INVALIDA";
            }
        }

        boolean temMinuscula = false;
        boolean temMaiuscula = false;
        boolean temDigito = false;
        for (char c : senha.toCharArray()) {
            if (c >= 'a' && c <= 'z') {
                temMinuscula = true;
            } else if (c >= 'A' && c <= 'Z') {
                temMaiuscula = true;
            } else {
                temDigito = true;
            }
        }
        int classes = (temMinuscula ? 1 : 0) + (temMaiuscula ? 1 : 0) + (temDigito ? 1 : 0);

        boolean repeticaoAdjacente = false;
        for (int i = 1; i < senha.length(); i++) {
            if (senha.charAt(i) == senha.charAt(i - 1)) {
                repeticaoAdjacente = true;
                break;
            }
        }

        int score = Math.max(1, classes - (repeticaoAdjacente ? 1 : 0));

        if (score == 3) {
            return "FORTE";
        }
        if (score == 2) {
            return "MEDIA";
        }
        return "FRACA";
    }
}
