class DuplicateSampleItemError(Exception):
    """Ejemplo de excepcion de dominio propia (ver spec_estandares_modelo_datos.txt
    seccion 3, 'Manejo de errores'). Un exception handler central en
    app/main.py la traduce a HTTP 409, para que el router nunca necesite un
    try/except con logica de negocio.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Ya existe un sample item con name={name!r}")
