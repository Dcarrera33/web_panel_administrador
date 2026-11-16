"""TEXTOS LEGALES: borradores redactados para lo que hace esta web (cursos informativos, formulario de
contacto, correo y cookies técnicas).

Los datos entre {llaves} se rellenan solos con lo que escribas en el panel (/gestion/ ->
«Textos y datos de la web» -> apartado «Datos legales»). Si falta alguno, sale como [CAMPO].
ANTES de publicar la web, que los revise una gestoría, abogado o consultor RGPD: no sustituyen el
asesoramiento profesional.

Formato: "## Título" = subtítulo · "- texto" = punto de lista · cualquier otra línea = párrafo.
"""

LEGAL = {
    # ------------------------------------------------------------------ AVISO LEGAL
    "aviso-legal": {
        "title": "Aviso legal",
        "paragraphs": [
            "Última actualización: {updated}.",
            "## 1. Titular del sitio web",
            "En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de que este sitio web es titularidad de:",
            "- Titular: {owner}",
            "- NIF/CIF: {cif}",
            "- Domicilio: {address}",
            "- Correo electrónico: {email}",
            "- Teléfono: {phone}",
            "## 2. Objeto y aceptación",
            "Este sitio web tiene por objeto dar a conocer los cursos de magia que imparte el titular y permitir a las personas usuarias ponerse en contacto para pedir información. El acceso y la navegación atribuyen la condición de persona usuaria e implican la aceptación de este aviso legal.",
            "## 3. Información sobre los cursos",
            "Los contenidos, duraciones, modalidades y precios de los cursos que se muestran en la web son informativos y pueden cambiar. La contratación de un curso, su precio final, fechas, forma de pago y condiciones de cancelación se acuerdan directamente con el titular antes de la inscripción. Este sitio web no es una tienda online ni realiza cobros.",
            "## 4. Condiciones de uso",
            "La persona usuaria se compromete a hacer un uso adecuado y lícito del sitio web, y en particular a no:",
            "- Facilitar datos falsos o de terceros sin su autorización en el formulario de contacto.",
            "- Enviar mensajes masivos, automatizados o con contenido ilícito, ofensivo o publicitario no solicitado.",
            "- Intentar acceder a zonas restringidas, alterar el funcionamiento del sitio o introducir contenidos o programas dañinos.",
            "## 5. Propiedad intelectual e industrial",
            "Los textos, fotografías, vídeos, logotipos, marcas, diseños y demás contenidos de este sitio web, así como el contenido y los materiales de los cursos, son propiedad del titular o de terceros que han autorizado su uso, y están protegidos por la normativa de propiedad intelectual e industrial. Queda prohibida su reproducción, distribución, comunicación pública o transformación sin autorización expresa y por escrito, salvo para uso personal y no comercial.",
            "## 6. Responsabilidad",
            "El titular procura que la información del sitio sea veraz y esté actualizada, pero no garantiza la ausencia de errores ni la disponibilidad continua del sitio, que puede interrumpirse por mantenimiento, fallos técnicos o causas ajenas a su control. Esto no limita los derechos que la normativa de consumidores reconoce a las personas usuarias.",
            "## 7. Enlaces",
            "Este sitio puede incluir enlaces a páginas de terceros, como Instagram. El titular no controla ni se responsabiliza de sus contenidos ni de sus políticas de privacidad. Si tienes conocimiento de que algún enlace conduce a contenidos ilícitos, puedes comunicarlo a {email}.",
            "## 8. Protección de datos y cookies",
            "El tratamiento de los datos personales se explica en la Política de privacidad, y el uso de cookies en la Política de cookies, ambas disponibles en el pie de esta página.",
            "## 9. Legislación aplicable y jurisdicción",
            "Este aviso legal se rige por la legislación española. Para cualquier controversia, serán competentes los juzgados y tribunales que correspondan conforme a la normativa vigente, respetando, en su caso, el fuero que la ley reconozca a las personas consumidoras y usuarias.",
        ],
    },

    # ------------------------------------------------------------------ PRIVACIDAD
    "privacidad": {
        "title": "Política de privacidad",
        "paragraphs": [
            "Última actualización: {updated}.",
            "En cumplimiento del Reglamento (UE) 2016/679 (RGPD) y de la Ley Orgánica 3/2018 (LOPDGDD), te explicamos de forma clara quién trata tus datos, para qué y cuáles son tus derechos.",
            "## 1. Responsable del tratamiento",
            "- Responsable: {owner}",
            "- NIF/CIF: {cif}",
            "- Domicilio: {address}",
            "- Correo electrónico: {email}",
            "- Teléfono: {phone}",
            "## 2. Qué datos tratamos y para qué",
            "Solo recogemos los datos que tú nos envías a través del formulario de contacto: nombre, correo electrónico, el curso por el que preguntas (si lo indicas) y el contenido de tu mensaje. Los usamos únicamente para atender tu consulta y responderte.",
            "No usamos tus datos para enviarte publicidad ni para elaborar perfiles, y no tomamos decisiones automatizadas sobre ti. Si nos escribes por Instagram, el tratamiento de esa conversación se rige también por las condiciones y la política de privacidad de esa plataforma.",
            "## 3. Base jurídica",
            "Tu consentimiento, que prestas al marcar la casilla y enviar el formulario (artículo 6.1.a del RGPD). Puedes retirarlo en cualquier momento escribiendo a {email}, sin que ello afecte a la licitud del tratamiento anterior.",
            "## 4. Plazo de conservación",
            "Conservamos tu mensaje durante {retention} desde que lo recibimos, o el tiempo necesario para atender tu consulta y, después, durante los plazos de prescripción de posibles responsabilidades. Pasado ese tiempo, los datos se suprimen o se anonimizan.",
            "## 5. Destinatarios",
            "No cedemos tus datos a terceros salvo obligación legal. Para prestar el servicio recurrimos a proveedores que actúan como encargados del tratamiento y solo tratan los datos siguiendo nuestras instrucciones:",
            "- Alojamiento web y base de datos: {hosting}.",
            "- Correo electrónico (recepción y respuesta de tus mensajes): Google (Gmail), con servidores que pueden estar fuera del Espacio Económico Europeo. Cuando ocurre, la transferencia se ampara en las garantías previstas por el RGPD (decisión de adecuación o cláusulas contractuales tipo).",
            "## 6. Seguridad",
            "Aplicamos medidas técnicas y organizativas razonables para proteger tus datos: conexión cifrada (HTTPS), acceso restringido al panel de gestión con usuario y contraseña, copias de seguridad y limitación del acceso a quien lo necesita.",
            "## 7. Tus derechos",
            "Puedes ejercer los derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar tu consentimiento. Escribe a {email} indicando el derecho que quieres ejercer y adjuntando una copia de tu documento de identidad, para poder verificar tu identidad. Responderemos en el plazo de un mes.",
            "Si consideras que tus derechos no han sido atendidos o que el tratamiento no se ajusta a la normativa, puedes presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es).",
            "## 8. Menores de edad",
            "Este sitio web se dirige a personas mayores de 14 años. Si eres menor de 14 años, el contacto debe hacerlo tu padre, madre o tutor legal.",
            "## 9. Veracidad y actualización",
            "Los datos que nos facilitas deben ser verdaderos. Podemos modificar esta política para adaptarla a cambios legales o del servicio; la versión vigente es siempre la publicada en esta página, con su fecha de actualización.",
        ],
    },

    # ------------------------------------------------------------------ COOKIES
    "cookies": {
        "title": "Política de cookies",
        "paragraphs": [
            "Última actualización: {updated}.",
            "## 1. Qué son las cookies",
            "Las cookies son pequeños archivos que un sitio web guarda en tu navegador para recordar información. Algunas son imprescindibles para que la web funcione; otras sirven para medir el uso o mostrar publicidad.",
            "## 2. Qué cookies usa este sitio",
            "Este sitio web utiliza únicamente cookies técnicas, estrictamente necesarias para prestarte el servicio que solicitas. Según el artículo 22.2 de la LSSI-CE, estas cookies están exentas del deber de obtener tu consentimiento, por lo que no mostramos un banner de cookies.",
            "- csrftoken (propia, de seguridad): protege el formulario de contacto frente a envíos no autorizados (ataques CSRF). Duración: hasta 1 año.",
            "- sessionid (propia, de sesión): mantiene iniciada la sesión de las personas autorizadas en el panel de gestión y muestra los avisos de la página. Duración: hasta 8 horas.",
            "Ambas cookies son propias, no se comparten con terceros y no almacenan datos que te identifiquen más allá de lo necesario para su función.",
            "## 3. Lo que no usamos",
            "No utilizamos cookies de analítica, publicidad, seguimiento ni perfilado. El enlace a Instagram te lleva a una página de un tercero, que puede utilizar sus propias cookies con su propia política; se aplican cuando entras en ella.",
            "Si en el futuro incorporamos otras cookies (por ejemplo, una herramienta de analítica), te lo comunicaremos, solicitaremos tu consentimiento previo con un panel de configuración y actualizaremos esta política.",
            "## 4. Cómo gestionar o eliminar las cookies",
            "Puedes permitir, bloquear o borrar las cookies desde la configuración de tu navegador (Chrome, Firefox, Safari, Edge...). Ten en cuenta que, si bloqueas las cookies técnicas, es posible que el formulario de contacto deje de funcionar.",
            "## 5. Más información",
            "Para cualquier duda sobre esta política, escríbenos a {email}. Puedes consultar más información sobre cookies en la web de la Agencia Española de Protección de Datos (www.aepd.es).",
        ],
    },
}
