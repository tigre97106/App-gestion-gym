async function cargarSocios() {
  const estado = document.getElementById("estado");
  const lista = document.getElementById("lista-socios");

  try {
    const respuesta = await fetch("http://127.0.0.1:8000/socios");

    if (!respuesta.ok) {
      throw new Error(`Error HTTP: ${respuesta.status}`);
    }

    const socios = await respuesta.json();
    lista.replaceChildren();

    for (const socio of socios) {
      const elemento = document.createElement("li");
      elemento.textContent = `${socio.nombre} ${socio.apellido}`;
      lista.appendChild(elemento);
    }

    estado.textContent = socios.length
      ? `${socios.length} socios encontrados`
      : "Todavía no hay socios";
  } catch (error) {
    estado.textContent = `No se pudieron cargar los socios: ${error.message}`;
  }
}

cargarSocios();