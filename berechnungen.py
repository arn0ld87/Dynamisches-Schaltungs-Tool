def berechne_reihenschaltung(ug: float, widerstaende: list[float]) -> dict:
    if not widerstaende:
        return {}
    rg = sum(widerstaende)
    ig = ug / rg if rg > 0 else 0
    teilspannungen = [ig * r for r in widerstaende]
    teilleistungen = [u * ig for u in teilspannungen]
    pg = sum(teilleistungen)
    return {
        "typ": "Reihenschaltung",
        "gesamtwiderstand": rg,
        "gesamtstrom": ig,
        "gesamtleistung": pg,
        "teilspannungen": teilspannungen,
        "teilströme": [ig] * len(widerstaende),
        "teilleistungen": teilleistungen,
        "widerstände": widerstaende,
    }


def berechne_parallelschaltung(ug: float, widerstaende: list[float]) -> dict:
    if not widerstaende or any(r <= 0 for r in widerstaende):
        return {}
    rg = 1 / sum(1 / r for r in widerstaende)
    ig = ug / rg if rg > 0 else 0
    teilströme = [ug / r for r in widerstaende]
    teilleistungen = [ug * i for i in teilströme]
    pg = sum(teilleistungen)
    return {
        "typ": "Parallelschaltung",
        "gesamtwiderstand": rg,
        "gesamtstrom": ig,
        "gesamtleistung": pg,
        "teilspannungen": [ug] * len(widerstaende),
        "teilströme": teilströme,
        "teilleistungen": teilleistungen,
        "widerstände": widerstaende,
    }


def berechne_schaltung_D(ug: float, widerstaende: list[float]) -> dict:
    if len(widerstaende) < 4:
        raise ValueError("Diese Schaltung erfordert mindestens 4 Widerstände.")

    lösungsweg = []
    r1, r2, r3, r4 = widerstaende[:4]

    r234 = 1 / (1 / r2 + 1 / r3 + 1 / r4)
    lösungsweg.append(f"1. Ersatzwiderstand des Parallel-Blocks (R2||R3||R4) berechnen: R_p = {r234:.2f} Ω")

    rg = r1 + r234
    lösungsweg.append(f"2. Gesamtwiderstand (R1 + R_p): Rg = {r1} Ω + {r234:.2f} Ω = {rg:.2f} Ω")

    ig = ug / rg if rg > 0 else 0
    lösungsweg.append(f"3. Gesamtstrom (Ug / Rg): Ig = {ug} V / {rg:.2f} Ω = {ig:.3f} A (fließt durch R1)")

    u1 = r1 * ig
    u234 = r234 * ig
    lösungsweg.append(f"4. Teilspannungen berechnen: U1 = {u1:.2f} V, U_parallel = {u234:.2f} V")

    i2 = u234 / r2
    i3 = u234 / r3
    i4 = u234 / r4
    lösungsweg.append(f"5. Teilströme im Parallel-Block: I2={i2:.3f}A, I3={i3:.3f}A, I4={i4:.3f}A")

    p1, p2, p3, p4 = u1 * ig, u234 * i2, u234 * i3, u234 * i4
    pg = ug * ig

    return {
        "typ": "Gemischteschaltung Reihe Reihe einzel --> Parallel",
        "gesamtwiderstand": rg,
        "gesamtstrom": ig,
        "gesamtleistung": pg,
        "teilspannungen": [u1, u234, u234, u234],
        "teilströme": [ig, i2, i3, i4],
        "teilleistungen": [p1, p2, p3, p4],
        "widerstände": widerstaende,
        "lösungsweg": lösungsweg,
    }


def berechne_schaltung_E(ug: float, widerstaende: list[float]) -> dict:
    if len(widerstaende) != 4:
        raise ValueError("Diese Schaltung erfordert genau 4 Widerstände.")

    lösungsweg = []
    r1, r2, r3, r4 = widerstaende

    r12 = (r1 * r2) / (r1 + r2)
    lösungsweg.append(f"1. Ersatzwiderstand Gruppe 1 (R1||R2): R12 = {r12:.2f} Ω")

    r34 = (r3 * r4) / (r3 + r4)
    lösungsweg.append(f"2. Ersatzwiderstand Gruppe 2 (R3||R4): R34 = {r34:.2f} Ω")

    rg = r12 + r34
    lösungsweg.append(f"3. Gesamtwiderstand (R12 + R34): Rg = {rg:.2f} Ω")

    ig = ug / rg if rg > 0 else 0
    lösungsweg.append(f"4. Gesamtstrom (Ug / Rg): Ig = {ig:.3f} A")

    u12 = r12 * ig
    u34 = r34 * ig
    lösungsweg.append(f"5. Spannung an Gruppe 1 (U1, U2): U12 = {u12:.2f} V")
    lösungsweg.append(f"6. Spannung an Gruppe 2 (U3, U4): U34 = {u34:.2f} V")

    i1 = u12 / r1
    i2 = u12 / r2
    i3 = u34 / r3
    i4 = u34 / r4
    lösungsweg.append(f"7. Teilströme: I1={i1:.3f}A, I2={i2:.3f}A, I3={i3:.3f}A, I4={i4:.3f}A")

    p1, p2, p3, p4 = u12 * i1, u12 * i2, u34 * i3, u34 * i4
    pg = ug * ig

    return {
        "typ": "Gemischte Schaltung Parallel --> Parallel",
        "gesamtwiderstand": rg,
        "gesamtstrom": ig,
        "gesamtleistung": pg,
        "teilspannungen": [u12, u12, u34, u34],
        "teilströme": [i1, i2, i3, i4],
        "teilleistungen": [p1, p2, p3, p4],
        "widerstände": widerstaende,
        "lösungsweg": lösungsweg,
    }


def berechne_schaltung_F(ug: float, widerstaende: list[float]) -> dict:
    if len(widerstaende) < 4:
        raise ValueError("Diese Schaltung erfordert mindestens 4 Widerstände.")

    lösungsweg = []
    r1, r2, r3, r4 = widerstaende[:4]

    r23 = (r2 * r3) / (r2 + r3)
    lösungsweg.append(f"1. Ersatzwiderstand des Parallel-Blocks (R2||R3): R23 = {r23:.2f} Ω")

    rg = r1 + r23 + r4
    lösungsweg.append(f"2. Gesamtwiderstand (R1 + R23 + R4): Rg = {rg:.2f} Ω")

    ig = ug / rg if rg > 0 else 0
    lösungsweg.append(f"3. Gesamtstrom (Ug / Rg): Ig = {ig:.3f} A (fließt durch R1, R4 und den Block R23)")

    u1 = r1 * ig
    u4 = r4 * ig
    u23 = r23 * ig
    lösungsweg.append(f"4. Teilspannungen: U1={u1:.2f}V, U4={u4:.2f}V, U_parallel(U2,U3)={u23:.2f}V")

    i2 = u23 / r2
    i3 = u23 / r3
    lösungsweg.append(f"5. Teilströme im Parallel-Block: I2={i2:.3f}A, I3={i3:.3f}A")

    p1, p2, p3, p4 = u1 * ig, u23 * i2, u23 * i3, u4 * ig
    pg = ug * ig

    return {
        "typ": "Gemischte Schaltung Reihe --> Parallel",
        "gesamtwiderstand": rg,
        "gesamtstrom": ig,
        "gesamtleistung": pg,
        "teilspannungen": [u1, u23, u23, u4],
        "teilströme": [ig, i2, i3, ig],
        "teilleistungen": [p1, p2, p3, p4],
        "widerstände": widerstaende,
        "lösungsweg": lösungsweg,
    }