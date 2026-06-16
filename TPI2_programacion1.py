import csv
import os

def cargar_desde_csv(ruta_archivo="paises.csv"):
    lista_paises = []
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "poblacion", "superficie", "continente"])
        return lista_paises

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                pais = {
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip()
                }
                lista_paises.append(pais)
    except (ValueError, KeyError):
        print("[ERROR] El archivo CSV contiene errores de formato o filas corruptas.")
    return lista_paises


def guardar_en_csv(lista_paises, ruta_archivo="paises.csv"):
    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for pais in lista_paises:
                writer.writerow(pais)
    except Exception as e:
        print(f"[ERROR] No se pudo escribir en el archivo: {e}")


def solicitar_entero_positivo(mensaje):
    while True:
        try:
            val = int(input(mensaje))
            if val > 0:
                return val
            print("[ERROR] El valor debe ser un numero positivo mayor a 0.")
        except ValueError:
            print("[ERROR] Entrada invalida. Por favor, ingrese un numero entero.")


def solicitar_texto_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("[ERROR] Este campo es obligatorio. No se permiten entradas vacias.")


def agregar_pais(lista_paises):
    print("\n--- AGREGAR NUEVO PAÍS ---")
    nombre = solicitar_texto_no_vacio("Ingrese el nombre del país: ")
    
    for p in lista_paises:
        if p["nombre"].lower() == nombre.lower():
            print(f"[ERROR] El país '{nombre}' ya se encuentra registrado.")
            return

    poblacion = solicitar_entero_positivo("Ingrese la cantidad de población: ")
    superficie = solicitar_entero_positivo("Ingrese la superficie en km2: ")
    continente = solicitar_texto_no_vacio("Ingrese el continente al que pertenece: ")

    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    lista_paises.append(nuevo_pais)
    guardar_en_csv(lista_paises)
    print(f"[ÉXITO] '{nombre}' ha sido agregado y guardado correctamente.")


def actualizar_pais(lista_paises):
    print("ACTUALIZAR DATOS DE UN PAÍS")
    nombre_buscar = solicitar_texto_no_vacio("Ingrese el nombre exacto del país a modificar: ")
    
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre_buscar.lower():
            print(f"Datos actuales -> Población: {pais['poblacion']} | Superficie: {pais['superficie']} km2")
            nueva_pob = solicitar_entero_positivo("Ingrese la nueva población: ")
            nueva_sup = solicitar_entero_positivo("Ingrese la nueva superficie en km2: ")
            
            pais["poblacion"] = nueva_pob
            pais["superficie"] = nueva_sup
            guardar_en_csv(lista_paises)
            print(f"[ÉXITO] Datos de '{pais['nombre']}' actualizados en el sistema.")
            return
            
    print("[AVISO] No se encontro ningun pais con ese nombre.")


def buscar_pais_por_nombre(lista_paises):
    print("BUSCAR PAÍS POR NOMBRE")
    criterio = solicitar_texto_no_vacio("Ingrese el nombre o parte del nombre a buscar: ").lower()
    encontrados = []

    for pais in lista_paises:
        if criterio in pais["nombre"].lower():
            encontrados.append(pais)

    if encontrados:
        print(f"\nSe encontraron {len(encontrados)} resultados:")
        mostrar_tabla_paises(encontrados)
    else:
        print("[AVISO] No se encontraron paises que coincidan con la busqueda.")


def filtrar_paises(lista_paises):
    print("OPCIONES DE FILTRADO")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    opcion = input("Seleccione una opcion de filtro (1-3): ")

    resultados = []
    if opcion == "1":
        continente = solicitar_texto_no_vacio("Ingrese el continente a filtrar: ").lower()
        resultados = [p for p in lista_paises if p["continente"].lower() == continente]
    elif opcion == "2":
        min_pob = solicitar_entero_positivo("Poblacion minima: ")
        max_pob = solicitar_entero_positivo("Poblacion maxima: ")
        if min_pob > max_pob:
            print("[ERROR] El minimo no puede superar al maximo.")
            return
        resultados = [p for p in lista_paises if min_pob <= p["poblacion"] <= max_pob]
    elif opcion == "3":
        min_sup = solicitar_entero_positivo("Superficie minima (km2): ")
        max_sup = solicitar_entero_positivo("Superficie maxima (km2): ")
        if min_sup > max_sup:
            print("[ERROR] El minimo no puede superar al maximo.")
            return
        resultados = [p for p in lista_paises if min_sup <= p["superficie"] <= max_sup]
    else:
        print("[ERROR] Opcion de filtro invalida.")
        return

    if resultados:
        print(f"\nResultados del filtro ({len(resultados)} paises):")
        mostrar_tabla_paises(resultados)
    else:
        print("[AVISO] Ningun pais cumple con los criterios del filtro especificado.")


def ordenar_paises(lista_paises):
    if not lista_paises:
        print("[AVISO] La lista esta vacia.")
        return

    print("\n--- ORDENAR PAÍSES ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Población")
    print("3. Ordenar por Superficie")
    op_campo = input("Seleccione el campo para ordenar (1-3): ")

    campo = ""
    if op_campo == "1": campo = "nombre"
    elif op_campo == "2": campo = "poblacion"
    elif op_campo == "3": campo = "superficie"
    else:
        print("[ERROR] Campo invalido.")
        return

    print("1. Ascendente")
    print("2. Descendente")
    op_sentido = input("Seleccione el sentido (1-2): ")
    if op_sentido != "1" and op_sentido != "2":
        print("[ERROR] Sentido invalido.")
        return

    lista_ordenada = list(lista_paises)
    n = len(lista_ordenada)

    for i in range(n):
        for j in range(0, n - i - 1):
            val_a = lista_ordenada[j][campo]
            val_b = lista_ordenada[j+1][campo]

            if isinstance(val_a, str):
                val_a = val_a.lower()
                val_b = val_b.lower()

            condicion_intercambio = val_a > val_b if op_sentido == "1" else val_a < val_b
            
            if condicion_intercambio:
                lista_ordenada[j], lista_ordenada[j+1] = lista_ordenada[j+1], lista_ordenada[j]

    print("\nLista ordenada correctamente:")
    mostrar_tabla_paises(lista_ordenada)


def mostrar_estadisticas(lista_paises):
    if not lista_paises:
        print("[AVISO] No hay datos cargados para generar estadisticas.")
        return
    print("INDICADORES Y ESTADÍSTICAS")

    pais_max_pob = lista_paises[0]
    pais_min_pob = lista_paises[0]
    suma_poblacion = 0
    suma_superficie = 0
    conteo_continentes = {}

    for pais in lista_paises:
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        if pais["poblacion"] > pais_max_pob["poblacion"]:
            pais_max_pob = pais
        if pais["poblacion"] < pais_min_pob["poblacion"]:
            pais_min_pob = pais

        cont = pais["continente"]
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1
        else:
            conteo_continentes[cont] = 1

    total_paises = len(lista_paises)
    prom_pob = suma_poblacion / total_paises
    prom_sup = suma_superficie / total_paises

    print(f"-> País con MAYOR población: {pais_max_pob['nombre']} ({pais_max_pob['poblacion']} hab.)")
    print(f"-> País con MENOR población: {pais_min_pob['nombre']} ({pais_min_pob['poblacion']} hab.)")
    print(f"-> Promedio de población general: {prom_pob:.2f} habitantes")
    print(f"-> Promedio de superficie general: {prom_sup:.2f} km2")
    print("\nDistribución geográfica (Cantidad de países por continente):")
    for cont, cant in conteo_continentes.items():
        print(f"   • {cont}: {cant}")


def mostrar_tabla_paises(lista):
    print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km2)':<18} | {'Continente':<15}")
    print("-" * 75)
    for p in lista:
        print(f"{p['nombre']:<20} | {p['poblacion']:<15} | {p['superficie']:<18} | {p['continente']:<15}")
    print("-" * 75)


def menu_principal():
    paises = cargar_desde_csv()
    
    while True:
        print("SISTEMA DE GESTIÓN DE PAÍSES")
        print("1. Mostrar todos los países")
        print("2. Agregar un país")
        print("3. Actualizar datos de un país")
        print("4. Buscar un país por nombre")
        print("5. Filtrar países (Continente / Rangos)")
        print("6. Ordenar países")
        print("7. Ver indicadores estadísticos")
        print("8. Salir del programa")
        
        opcion = input("Seleccione una opción (1-8): ").strip()
        
        if opcion == "1":
            if paises:
                print(f"\nListado General de Países ({len(paises)} cargados):")
                mostrar_tabla_paises(paises)
            else:
                print("[AVISO] El sistema no tiene países cargados actualmente.")
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_pais_por_nombre(paises)
        elif opcion == "5":
            filtrar_paises(paises)
        elif opcion == "6":
            ordenar_paises(paises)
        elif opcion == "7":
            mostrar_estadisticas(paises)
        elif opcion == "8":
            print("Guardando cambios... ¡Gracias por utilizar el sistema UTN!")
            break
        else:
            print("[ERROR] Opción inválida. Intente con un número del 1 al 8.")

if __name__ == "__main__":
    menu_principal()