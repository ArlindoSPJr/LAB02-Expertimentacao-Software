package com.lab02.katas;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.regex.Pattern;

public final class PlacaNormalizer {

    private static final Pattern PADRAO_ANTIGO = Pattern.compile("[A-Z]{3}[0-9]{4}");
    private static final Pattern PADRAO_MERCOSUL = Pattern.compile("[A-Z]{3}[0-9][A-Z][0-9]{2}");

    private PlacaNormalizer() {
    }

    public static List<String> normalizar(List<String> brutas) {
        LinkedHashSet<String> canonicas = new LinkedHashSet<>();
        for (String bruta : brutas) {
            if (bruta == null || bruta.isEmpty()) {
                continue;
            }
            String normalizada = bruta.replaceAll("[ \\-.]", "").toUpperCase();
            if (isCanonica(normalizada)) {
                canonicas.add(normalizada);
            }
        }
        return new ArrayList<>(canonicas);
    }

    private static boolean isCanonica(String placa) {
        return placa.length() == 7
            && (PADRAO_ANTIGO.matcher(placa).matches() || PADRAO_MERCOSUL.matcher(placa).matches());
    }
}
