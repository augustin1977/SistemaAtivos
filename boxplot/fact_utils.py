# fact_utils.py
import re
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
import json


def extrair_dados_generico(text):
    records = []
    current_temperature = None
    current_phase = None
    current_total_mass = None
    in_system_component = False

    regex_temp = re.compile(r"Page\s+\d+\s+\[(\d+)\s*C\]")
    phase_pattern_b = re.compile(r"^\s*\+\s*([\d.Ee+-]+)\s*gram\s+(\S+)")
    regex_phase_line = re.compile(r"PHASE:\s+(\S+)", re.IGNORECASE)
    regex_total_mass = re.compile(r"\(([\d.Ee+-]+)\s*gram,")
    regex_dado_sys = re.compile(r"^\s*(\S+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)")

    lines = text.splitlines()
    for line in lines:
        temp_match = regex_temp.search(line)
        if temp_match:
            current_temperature = int(temp_match.group(1))
            current_phase = None
            current_total_mass = None
            in_system_component = False

        m = phase_pattern_b.match(line)
        if m:
            try:
                current_total_mass = float(m.group(1))
            except:
                current_total_mass = None
            current_phase = m.group(2)
            in_system_component = False
            continue

        m2 = regex_phase_line.search(line)
        if m2:
            current_phase = m2.group(1)
            current_total_mass = None
            in_system_component = False
            continue

        if current_phase and current_phase.lower() == "gas_ideal" and current_total_mass is None:
            total_match = regex_total_mass.search(line)
            if total_match:
                try:
                    current_total_mass = float(total_match.group(1))
                except:
                    current_total_mass = None

        if current_phase and "System component" in line:
            in_system_component = True
            continue

        if in_system_component:
            if line.strip() == "":
                in_system_component = False
                continue
            m3 = regex_dado_sys.match(line)
            if not m3:
                in_system_component = False
                continue
            element = m3.group(1)
            try:
                amount_gram = float(m3.group(3))
                mass_fraction = float(m3.group(5))
            except:
                continue
            records.append({
                "temperature": current_temperature,
                "phase": current_phase,
                "element": element,
                "amount_gram": amount_gram,
                "mass_fraction": mass_fraction,
                "total_mass": current_total_mass
            })
    return records


def get_options(records):
    options = {}
    all_elements = set()
    for rec in records:
        phase = rec["phase"]
        total = rec["total_mass"]
        if phase.lower() == "gas_ideal" or (total is None or (total is not None and total > 0)):
            if phase not in options:
                options[phase] = set()
            options[phase].add(rec["element"])
            all_elements.add(rec["element"])
    options = {phase: sorted(list(elements)) for phase, elements in options.items()}
    all_elements = sorted(list(all_elements))
    return options, all_elements


def gerar_excel(records, elementos_selecionados, fases_selecionadas):
    filtered = [
        rec for rec in records
        if rec["phase"] in fases_selecionadas and rec["element"] in elementos_selecionados
    ]

    if not filtered:
        return HttpResponse("Nenhum registro corresponde à seleção.<br>Selecione pelo menos um elemento e uma fase.")

    df = pd.DataFrame(filtered)
    df = df[["temperature", "phase", "element", "amount_gram", "mass_fraction", "total_mass"]]
    df.rename(columns={
        "temperature": "Temperatura (C)",
        "phase": "Fase",
        "element": "Elemento",
        "amount_gram": "Amount/gram",
        "mass_fraction": "Mass fraction",
        "total_mass": "Total mass (g)"
    }, inplace=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Resultados", index=False)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="resultados_fact.xlsx"'
    return response
