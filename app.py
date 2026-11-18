import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="EduPredict AI", page_icon="🎓", layout="centered")

st.title("🎓 EduPredict AI")
st.write("Predice si un alumno va bien, está en riesgo o puede darse de baja.")

# --- 1. DATOS DEL ALUMNO ---
st.header("1. Datos del alumno")
nombre = st.text_input("Nombre del alumno", placeholder="Ej: Juan Pérez")
grado = st.selectbox("Grado / Semestre", ["1° Secundaria", "2° Secundaria", "3° Secundaria", "1° Prepa", "2° Prepa", "3° Prepa", "1° Universidad", "2° Universidad", "Otro"])
fecha_ingreso = st.date_input("¿Cuándo ingresó / se reclutó en la escuela?", value=date(2025, 8, 18))

# --- 2. RENDIMIENTO ---
st.header("2. Rendimiento en la escuela")
promedio = st.slider("Promedio general (0 a 10)", 0.0, 10.0, 8.0, 0.1)
asistencia = st.slider("Asistencia (%)", 0, 100, 90)
reprobadas = st.number_input("Materias reprobadas este periodo", 0, 10, 0)
tareas = st.slider("¿Entrega tareas? (0 = nunca, 10 = siempre)", 0, 10, 7)
participa = st.selectbox("¿Participa en clase?", ["Sí, mucho", "A veces", "Casi nunca", "No"])
apoyo = st.selectbox("¿Tiene apoyo en casa?", ["Sí", "A veces", "No"])
motivo = st.selectbox("¿Por qué podría dejar la escuela?", ["Ninguno, va bien", "No le gustan las clases", "Problemas económicos", "Problemas familiares", "Se siente desmotivado/a", "Trabaja", "Otro"])

# --- 3. BOTÓN PARA PREDECIR ---
if st.button("🔮 Predecir riesgo", use_container_width=True):
    if nombre.strip() == "":
        st.warning("Escribe el nombre del alumno primero.")
    else:
        riesgo = 0
        if promedio < 6:
            riesgo += 40
        elif promedio < 7:
            riesgo += 25
        elif promedio < 8:
            riesgo += 10

        if asistencia < 60:
            riesgo += 35
        elif asistencia < 80:
            riesgo += 20
        elif asistencia < 90:
            riesgo += 5

        riesgo += reprobadas * 8

        if tareas < 4:
            riesgo += 15
        elif tareas < 7:
            riesgo += 5

        if participa == "Casi nunca":
            riesgo += 10
        elif participa == "No":
            riesgo += 15

        if apoyo == "No":
            riesgo += 10
        elif apoyo == "A veces":
            riesgo += 5

        if riesgo > 100:
            riesgo = 100

        st.divider()
        st.subheader(f"Resultado para: {nombre}")
        st.write(f"**Grado:** {grado}")
        st.write(f"**Fecha de ingreso / reclutamiento:** {fecha_ingreso}")
        st.write(f"**Promedio:** {promedio} | **Asistencia:** {asistencia}% | **Reprobadas:** {reprobadas}")

        if riesgo < 30:
            st.success(f"🟢 VA BIEN - Riesgo bajo: {riesgo}%")
            consejo = "Sigue así. Felicítalo/a, que mantenga su rutina de estudio y que siga participando."
        elif riesgo < 60:
            st.warning(f"🟡 EN RIESGO - Riesgo medio: {riesgo}%")
            consejo = "Habla con él/ella esta semana. Revisa qué materia le cuesta más, haz un plan de tareas y avisa a sus papás/tutores."
        else:
            st.error(f"🔴 ALTO RIESGO DE BAJA - Riesgo: {riesgo}%")
            consejo = "¡Actúa ya! Habla con el alumno, su familia y orientación escolar. Busca apoyo económico, psicológico o de regularización."

        st.info(f"💡 Consejo: {consejo}")
        st.write(f"**Motivo:** {motivo}")

        datos = pd.DataFrame([{
            "Nombre": nombre,
            "Grado": grado,
            "Fecha de ingreso": str(fecha_ingreso),
            "Promedio": promedio,
            "Asistencia %": asistencia,
            "Reprobadas": reprobadas,
            "Riesgo %": riesgo,
            "Estado": "VA BIEN" if riesgo < 30 else "EN RIESGO" if riesgo < 60 else "ALTO RIESGO DE BAJA",
            "Consejo": consejo
        }])
        st.dataframe(datos, use_container_width=True)
        st.download_button("⬇️ Descargar resultado en Excel (CSV)", datos.to_csv(index=False), file_name=f"{nombre}_edupredict.csv", mime="text/csv")

st.caption("EduPredict AI - Ayuda para maestros y alumnos, no es un diagnóstico oficial.")
