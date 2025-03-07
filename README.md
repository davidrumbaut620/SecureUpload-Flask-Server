
# **SecureUpload Flask Server 🚀🔒**

![Login Page](https://raw.githubusercontent.com/davidrumbaut620/SecureUpload-Flask-Server/refs/heads/main/shot_transparent.png)

## **Descripción General**  
**SecureUpload Flask Server** es un servidor ligero y seguro para la carga y gestión de archivos, especialmente imágenes, desarrollado con Flask. Diseñado para ser **rápido, seguro y fácil de usar**, este servidor proporciona un entorno confiable para manejar archivos sin comprometer la seguridad de las credenciales.

Aprovecha la flexibilidad de Flask para ofrecer una API simple pero robusta, protegiendo el acceso mediante autenticación basada en variables de entorno. Esto garantiza que las credenciales sensibles no se expongan en el código fuente, brindando una capa adicional de seguridad.

---

## **🛡️ Seguridad y Autenticación**  
Este servidor **protege el acceso a la subida de archivos mediante autenticación**. Para garantizar la seguridad, se utilizan variables de entorno para almacenar credenciales de administrador y una clave secreta.

🔑 **Variables de entorno necesarias:**  
```plaintext
ADMIN_USERNAME=tu_nombre
ADMIN_PASSWORD=tu_contraseña
SECRET_KEY=tu_clave
```
✅ **Protección con credenciales**: Solo los usuarios autenticados pueden acceder a la carga de archivos.  
✅ **Clave secreta**: Utilizada para gestionar sesiones y seguridad en Flask.  

> 💡 **Importante:** Nunca compartas tu `SECRET_KEY` ni tus credenciales de administrador públicamente.

---

![MockUP](https://raw.githubusercontent.com/davidrumbaut620/SecureUpload-Flask-Server/refs/heads/main/shot2_transparent.png)

## **📂 Funcionalidades Principales**  
🔥 **Carga Segura de Archivos**: Permite subir imágenes y otros archivos con autenticación.  
🔍 **Gestión de Archivos**: Organiza y almacena los archivos de manera eficiente en el servidor.  
⚡ **Flask como Backend Ligero**: Ideal para implementaciones rápidas y eficientes.  
🔐 **Variables de Entorno para Mayor Seguridad**: Evita exponer credenciales en el código fuente.  
🌗 **Diseño Moderno en Modo Oscuro**: Interfaz elegante estilo SaaS.  
🌍 **Acceso en Red Local**: Puedes ver y acceder al servidor desde otros dispositivos en la misma red local mediante la IP de la máquina que lo ejecuta.  
   - **Ejemplo**: Si la IP de tu máquina es `192.168.1.100`, podrás acceder al servidor en `http://192.168.1.100:8000`.


---

## **📌 Requisitos para Ejecutar la Aplicación**  
1️⃣ **Instalar dependencias**:  
```bash
pip install requirements.txt
```  
2️⃣ **Configurar las variables de entorno** en un archivo `.env` dentro del proyecto:  
```plaintext
ADMIN_USERNAME=tu_nombre
ADMIN_PASSWORD=tu_contraseña
SECRET_KEY=tu_clave
```  
3️⃣ **Ejecutar el servidor Flask**:  
```bash
python app.py
```  
4️⃣ **Acceder a la aplicación** en:  
```
http://127.0.0.1:8000
```

---

## **🚀 Ideal para**  
✔️ Desarrolladores que necesiten un backend seguro y simple para carga de archivos.  
✔️ Aplicaciones web que requieran almacenamiento de imágenes o documentos.  
✔️ Proyectos que buscan una solución minimalista pero efectiva para manejar archivos.  

Con **SecureUpload Flask Server**, obtienes una solución segura, fácil de usar y rápida de desplegar para la gestión de archivos. 🔥💡  

---

## **💻 Contribuciones y Mejoras**  
¡Este proyecto está abierto a mejoras! Si tienes sugerencias o quieres contribuir, no dudes en hacerlo. 📩✨  

## **📜 Licencia**  
Este proyecto está bajo la licencia **MIT**, lo que permite su libre uso y modificación. 🎯
