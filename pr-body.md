Agrega tests para manejar errores en la función principal `scrape_ecommerce`.

### Cambios realizados:
- Se añadieron tests en `test_scraper.py` para cubrir los siguientes escenarios de error:
  - Error de conexión (`ConnectionError`)
  - Timeout (`Timeout`)
  - Límite de tasa (`429 Too Many Requests`)
  - Excepción inesperada (`Exception`)
  - Datos vacíos o no encontrados (`empty data`, `no data`, `no products found`)

### Verificación:
- Todos los tests pasan: `pytest test_scraper.py -v` (37/37 ✅)
- Se mantiene la cobertura existente y no se modificó el código productivo.

### Criterios de aceptación:
✅ Tests cubren todos los paths de error principales
✅ Los tests verifican que la función devuelve `False` en caso de error
✅ No se introdujeron nuevos bugs ni se alteró el comportamiento exitoso

Closes #<issue> (si hay un issue relacionado)