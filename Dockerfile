# Implementar una imagen base oficial de Java (LTS)
FROM openjdk:17-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo .jar compilado de tu aplicación al contenedor
COPY target/*.jar app.jar

# Puerto de la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación cuando se inicie el contenedor
ENTRYPOINT ["java", "-jar", "app.jar"]
