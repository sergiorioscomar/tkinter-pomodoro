# 🍅 Pomodoro App

Aplicación de escritorio tipo **Pomodoro Timer**, desarrollada en Python con Tkinter. Basada en la técnica Pomodoro, te ayuda a mejorar tu productividad organizando el trabajo en intervalos de 25 minutos seguidos por descansos.

![Captura de la aplicación](./img/pomodoro.png)

## 🧠 ¿Qué es la técnica Pomodoro?

Es una técnica de gestión del tiempo que divide el trabajo en bloques:
- 25 minutos de trabajo
- 5 minutos de descanso corto
- Cada 4 bloques: 15 minutos de descanso largo

## ⚙️ Tecnologías utilizadas

- Python 3
- Tkinter (interfaz gráfica)
- `tkinter.PhotoImage` para imagen decorativa

## 📦 Instalación

### Requisitos

- Python 3
- pip
- tkinter (`sudo apt install python3-tk` en Ubuntu)

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/pomodoro-app.git
cd pomodoro-app

# Ejecutar la app
python3 pomodoro.py
```

💡 Asegurate de tener el archivo `img/pomodoro.png` en la misma carpeta para que se muestre la imagen correctamente.

## 🚀 Funcionalidades

- Cuenta regresiva de 25 min para trabajo
- Descansos automáticos (5 min o 15 min)
- Botones para iniciar o reiniciar el ciclo
- Indicadores visuales con ✔ para ciclos completados

## 📌 Mejoras futuras

- ✅ Sonidos de notificación al finalizar el tiempo
- ✅ Configuración de tiempos desde la interfaz
- ⏳ Minimizar a la bandeja del sistema
- 📈 Reporte de sesiones realizadas
- 🌙 Modo oscuro
- 🌐 Versión web con Flask o Django

## 🗃️ Organización del proyecto

Este proyecto está gestionado con tableros Kanban en GitHub Projects para priorizar mejoras y bugs.

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.
