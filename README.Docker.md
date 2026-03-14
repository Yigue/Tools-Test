### Construyendo y ejecutando tu aplicación

INSTRUCCIÓN: Cuando estés listo, inicia tu aplicación ejecutando:
`docker compose up --build`.

REGLA: Tu aplicación estará disponible en http://localhost:8000.

### Desplegando tu aplicación en la nube

INSTRUCCIÓN: Primero, construye tu imagen, por ejemplo: `docker build -t myapp .`.
REGLA: Si tu nube usa una arquitectura de CPU diferente a la de tu máquina
de desarrollo (por ejemplo, estás en una Mac M1 y tu proveedor es amd64),
debes construir la imagen para esa plataforma, por ejemplo:
`docker build --platform=linux/amd64 -t myapp .`.

INSTRUCCIÓN: Luego, súbela a tu registro, por ejemplo: `docker push myregistry.com/myapp`.

REGLA: Consulta la [guía de inicio](https://docs.docker.com/go/get-started-sharing/)
de Docker para más detalles sobre cómo construir y subir imágenes.

### Referencias
* [Guía de Python de Docker](https://docs.docker.com/language/python/)