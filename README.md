# Chainstore API

Esta aplicación está publicada en la nube de Azure:

**URL de producción:** [https://chainstore.orangebay-288b47f6.westus2.azurecontainerapps.io](https://chainstore.orangebay-288b47f6.westus2.azurecontainerapps.io)

**Documentación Swagger:** [https://chainstore.orangebay-288b47f6.westus2.azurecontainerapps.io/docs](https://chainstore.orangebay-288b47f6.westus2.azurecontainerapps.io/docs)

## Comandos de ejecución local

1. Instala las dependencias:

```powershell
pip install -r app/requirements.txt
```

2. Ejecuta la aplicación:

```powershell
python app/app.py
```

La API estará disponible localmente en `http://localhost:8000` (o el puerto configurado en tu código).

## Variables de entorno

Configura el archivo `.env` en la carpeta `app` con tus credenciales de base de datos:

```
USER_DB=myadmin
PASSWORD_DB=QJGp65ctPVPwWWc
HOST_DB=chainstoretest.mysql.database.azure.com
NAME_DB=chainstore
```

## Notas
- La documentación interactiva está disponible en `/docs` usando Swagger.
- El despliegue en Azure Container Apps permite acceso público a la API y la documentación.
