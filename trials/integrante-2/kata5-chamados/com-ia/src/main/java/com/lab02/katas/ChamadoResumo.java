package com.lab02.katas;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ChamadoResumo {

    private static final List<String> ORDEM_PRIORIDADES = List.of("ALTA", "MEDIA", "BAIXA");

    private ChamadoResumo() {
    }

    public static List<String> resumir(List<String> chamados) {
        Map<String, Integer> contagens = new LinkedHashMap<>();
        for (String prioridade : ORDEM_PRIORIDADES) {
            contagens.put(prioridade, 0);
        }

        for (String chamado : chamados) {
            if (chamado == null) {
                continue;
            }
            int separador = chamado.indexOf(':');
            if (separador < 0 || chamado.indexOf(':', separador + 1) >= 0) {
                continue;
            }
            String prioridade = chamado.substring(0, separador).toUpperCase();
            String codigo = chamado.substring(separador + 1);
            if (codigo.isEmpty() || !contagens.containsKey(prioridade)) {
                continue;
            }
            contagens.merge(prioridade, 1, Integer::sum);
        }

        List<String> resultado = new ArrayList<>();
        for (String prioridade : ORDEM_PRIORIDADES) {
            int total = contagens.get(prioridade);
            if (total > 0) {
                resultado.add(prioridade + ":" + total);
            }
        }
        return resultado;
    }
}
