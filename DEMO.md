# 🧪 Demo End-to-End - API de Gestión de Franquicias

Este documento muestra cómo realizar pruebas end-to-end completas de la API de gestión de franquicias.

## 🚀 Pasos para Ejecutar las Pruebas

### Opción 1: Usando Docker (Recomendado)

1. **Compilar y ejecutar con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **En otra terminal, ejecutar las pruebas:**
   ```bash
   # En Windows
   test-end-to-end.bat
   
   # En Linux/Mac
   chmod +x test-end-to-end.sh
   ./test-end-to-end.sh
   ```

### Opción 2: Usando Maven

1. **Compilar la aplicación:**
   ```bash
   ./mvnw clean package -DskipTests
   ```

2. **Ejecutar la aplicación:**
   ```bash
   ./mvnw spring-boot:run
   ```

3. **En otra terminal, ejecutar las pruebas:**
   ```bash
   # En Windows
   test-end-to-end.bat
   
   # En Linux/Mac
   ./test-end-to-end.sh
   ```

### Opción 3: Ejecutar Tests Unitarios

```bash
./mvnw test
```

## 📋 Secuencia de Pruebas End-to-End

### 1. Crear Franquicia
```bash
curl -X POST http://localhost:8080/api/franquicias \
  -H "Content-Type: application/json" \
  -d '{"nombre": "McDonalds"}'
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "nombre": "McDonalds",
  "sucursales": []
}
```

### 2. Crear Sucursales
```bash
# Sucursal Centro
curl -X POST http://localhost:8080/api/franquicias/1/sucursales \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Sucursal Centro"}'

# Sucursal Norte
curl -X POST http://localhost:8080/api/franquicias/1/sucursales \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Sucursal Norte"}'
```

### 3. Agregar Productos a Sucursal Centro
```bash
# Big Mac
curl -X POST http://localhost:8080/api/sucursales/1/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Big Mac", "cantidadStock": 50}'

# McFlurry
curl -X POST http://localhost:8080/api/sucursales/1/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "McFlurry", "cantidadStock": 30}'

# Papas Fritas
curl -X POST http://localhost:8080/api/sucursales/1/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Papas Fritas", "cantidadStock": 100}'
```

### 4. Agregar Productos a Sucursal Norte
```bash
# Big Mac
curl -X POST http://localhost:8080/api/sucursales/2/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Big Mac", "cantidadStock": 25}'

# McFlurry
curl -X POST http://localhost:8080/api/sucursales/2/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "McFlurry", "cantidadStock": 15}'
```

### 5. Modificar Stock
```bash
curl -X PATCH http://localhost:8080/api/productos/1/stock \
  -H "Content-Type: application/json" \
  -d '{"stock": 75}'
```

### 6. Actualizar Nombres
```bash
# Actualizar franquicia
curl -X PATCH http://localhost:8080/api/franquicias/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "McDonalds Premium"}'

# Actualizar sucursal
curl -X PATCH http://localhost:8080/api/sucursales/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Sucursal Centro Premium"}'

# Actualizar producto
curl -X PATCH http://localhost:8080/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Big Mac Deluxe"}'
```

### 7. Obtener Reporte de Stock
```bash
curl -X GET http://localhost:8080/api/franquicias/1/reporte-stock
```

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "nombre": "Big Mac Deluxe",
    "cantidadStock": 75
  },
  {
    "id": 4,
    "nombre": "Big Mac",
    "cantidadStock": 25
  }
]
```

### 8. Eliminar Producto
```bash
curl -X DELETE http://localhost:8080/api/productos/2
```

### 9. Verificar Reporte Final
```bash
curl -X GET http://localhost:8080/api/franquicias/1/reporte-stock
```

## 🔍 Verificación de la Base de Datos

Puedes acceder a la consola H2 para verificar los datos:

1. Abrir navegador en: http://localhost:8080/h2-console
2. JDBC URL: `jdbc:h2:mem:franquiciasdb`
3. Username: `sa`
4. Password: (dejar en blanco)

## 📊 Resultados Esperados

Después de ejecutar todas las pruebas, deberías ver:

- ✅ 1 franquicia creada
- ✅ 2 sucursales creadas
- ✅ 5 productos creados inicialmente
- ✅ 1 producto eliminado
- ✅ 4 productos restantes
- ✅ Reporte de stock mostrando el producto con mayor stock por sucursal

## 🐛 Solución de Problemas

### Error: "Connection refused"
- Verificar que la aplicación esté ejecutándose en el puerto 8080
- Esperar unos segundos para que la aplicación inicie completamente

### Error: "404 Not Found"
- Verificar que la URL sea correcta: `http://localhost:8080/api/...`
- Verificar que el endpoint esté disponible

### Error: "500 Internal Server Error"
- Verificar que los IDs existan en la base de datos
- Revisar los logs de la aplicación para más detalles

## 🎯 Casos de Prueba Adicionales

### Prueba de Validación
```bash
# Intentar crear franquicia sin nombre
curl -X POST http://localhost:8080/api/franquicias \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Prueba de Recursos No Encontrados
```bash
# Intentar acceder a franquicia inexistente
curl -X GET http://localhost:8080/api/franquicias/999/reporte-stock
```

### Prueba de Eliminación de Producto Inexistente
```bash
# Intentar eliminar producto inexistente
curl -X DELETE http://localhost:8080/api/productos/999
```

¡Estas pruebas verifican que toda la funcionalidad de la API esté funcionando correctamente! 🎉

